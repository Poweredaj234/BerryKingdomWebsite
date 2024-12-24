from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, CoinTossView, BlackjackView

router = DefaultRouter()
router.register(r'games', GameViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('coin-toss/', CoinTossView.as_view(), name='coin-toss'),
    path('blackjack/', BlackjackView.as_view(), name='blackjack'),
]
