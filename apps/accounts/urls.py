from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterView, LoginView, LogoutView, leaderboard, TransferBalanceView, UpdateHouseView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('transfer/', TransferBalanceView.as_view(), name='transfer'),
    path('update-house/', UpdateHouseView.as_view(), name='update-house'),

]
