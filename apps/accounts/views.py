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
