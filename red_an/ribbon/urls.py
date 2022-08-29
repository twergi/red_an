from django.urls import path
from .views import ribbonView


urlpatterns = [
    path('', ribbonView, name='ribbon'),
]
