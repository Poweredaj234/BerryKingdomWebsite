from rest_framework import viewsets
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, TransferBalanceSerializer
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."})
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.data['username'],
                password=serializer.data['password']
            )
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})
            return Response({"error": "Invalid credentials"}, status=400)
        return Response(serializer.errors, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully."})

@api_view(['GET'])
def leaderboard(request):
    users = CustomUser.objects.order_by('-balance')[:10]
    leaderboard_data = [
        {"username": user.username, "balance": user.balance}
        for user in users
    ]
    return Response(leaderboard_data)


class TransferBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferBalanceSerializer(data=request.data)
        if serializer.is_valid():
            sender = request.user
            recipient = CustomUser.objects.filter(
                username=serializer.validated_data['recipient_username']
            ).first()
            if not recipient:
                return Response({"error": "Recipient not found"}, status=404)
            if sender.balance < serializer.validated_data['amount']:
                return Response({"error": "Insufficient balance"}, status=400)

            amount = serializer.validated_data['amount']
            sender.balance -= amount
            recipient.balance += amount
            sender.save()
            recipient.save()
            return Response({"message": "Transfer successful"})
        return Response(serializer.errors, status=400)

class UpdateHouseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        house = request.data.get('house')
        if not house:
            return Response({"error": "House name is required"}, status=400)
        request.user.house = house
        request.user.save()
        return Response({"message": "House updated successfully."})
    
@csrf_exempt
def register_user(request):
    """
    Self-registration endpoint for new users.
    """
    if request.method == "POST":
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            
            # Self-registration logic
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({"message": "User created successfully", "user_id": user.id})
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
@csrf_exempt
def create_user_by_duke(request):
    """
    Endpoint for Dukes or higher nobility to create new users.
    """
    if request.method == "POST":
        try:
            created_by = request.user
            
            # Verify nobility level
            if created_by.nobility > 3:  # Nobility +3
                return JsonResponse({"error": "Permission denied. Must be Duke or higher."}, status=403)

            # Gather data
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            nobility = int(request.POST.get('nobility', 7))  # Default to Citizen
            house = request.POST.get('house', None)

            # Check house validity
            if house and created_by.house != house:
                return JsonResponse({"error": "You can only assign users to your own house."}, status=403)

            # Create user
            user = CustomUser.objects.create_user(
                username=username, email=email, password=password,
                nobility=nobility, house=house, created_by=created_by
            )
            return JsonResponse({"message": "User created successfully", "user_id": user.id})
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def register_form(request):
    return render(request, 'register.html')

def create_user_by_duke_form(request):
    return render(request, 'create_by_duke.html')

