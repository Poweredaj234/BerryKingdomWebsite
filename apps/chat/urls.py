from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatMessageViewSet, ChatMessageListView

router = DefaultRouter()
router.register(r'messages', ChatMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('list/', ChatMessageListView.as_view(), name='chat-list'),
]
