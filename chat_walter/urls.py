from django.urls import path
from .views import chat_api, speak

urlpatterns = [
    path('chat/', chat_api, name='chat_api'),
    path('speak/', speak, name='speak'),
]
