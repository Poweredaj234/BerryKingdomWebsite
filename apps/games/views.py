from rest_framework import viewsets
from .models import Game, GameSession
from .serializers import GameSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .logic import play_coin_toss, play_blackjack


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class CoinTossView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        stake = request.data.get('stake', 0)
        if stake <= 0:
            return Response({"error": "Invalid stake amount"}, status=400)

        if request.user.balance < stake:
            return Response({"error": "Insufficient balance"}, status=400)

        result = play_coin_toss(request.user, stake)
        if result['result'] == "Win":
            request.user.balance += result['earnings']
        else:
            request.user.balance -= stake
        request.user.save()

        # Log the game session
        game, _ = Game.objects.get_or_create(name="Coin Toss", is_multiplayer=False)
        GameSession.objects.create(
            game=game,
            user=request.user,
            result=result['result'],
            stake=stake
        )

        return Response(result)


class BlackjackView(APIView): #STUB
    permission_classes = [IsAuthenticated]

    def post(self, request):
        stake = request.data.get('stake', 0)
        user_action = request.data.get('action', None)

        if stake <= 0:
            return Response({"error": "Invalid stake amount"}, status=400)

        if request.user.balance < stake:
            return Response({"error": "Insufficient balance"}, status=400)

        result = play_blackjack(request.user, stake, user_action)
        if result['result'] == "Win":
            request.user.balance += result['earnings']
        else:
            request.user.balance -= stake
        request.user.save()

        # Log the game session
        game, _ = Game.objects.get_or_create(name="Blackjack", is_multiplayer=True)
        GameSession.objects.create(
            game=game,
            user=request.user,
            result=result['result'],
            stake=stake
        )

        return Response(result)
