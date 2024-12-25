from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterView, LoginView, LogoutView, leaderboard, TransferBalanceView, UpdateHouseView, create_user_by_duke, register_form, create_user_by_duke_form, validate_token, get_user_info
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
    path('create-by-duke/', create_user_by_duke, name='create_user_by_duke'),
    path('register-form/', register_form, name='register_form'),
    path('create-user-by-duke/', create_user_by_duke_form, name='create_user_by_duke_form'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('validate-token/', validate_token, name='validate_token'),
    path('users/', get_user_info, name='get_user_info'),
]
