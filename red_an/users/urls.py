from django.urls import path
from .views import userView


urlpatterns = [
    path('<str:username>', userView, name='user'),
]
