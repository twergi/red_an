from django.urls import path
from .views import userView, loginUser, logoutUser, registerUser, editUser


urlpatterns = [
    path('<str:username>', userView, name='user'),
    path('login/', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerUser, name='register'),
    path('edit/', editUser, name='edit_user'),
]
