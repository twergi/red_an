from django.urls import path
from django.contrib.auth import views as auth_views
from .views import userView, loginUser, logoutUser, registerUser


urlpatterns = [
    path('<str:username>', userView, name='user'),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login_register.html'), name='login'),
    path('login/', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerUser, name='register'),
]
