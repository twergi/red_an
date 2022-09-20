from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name='api'),
    path('sections/', views.getSections),
    path('sections/<str:section_id>', views.getSection),
    path('sections/<str:section_id>/posts', views.getPosts),
    path('sections/<str:section_id>/posts/<str:post_id>', views.getPost),
    path('sections/<str:section_id>/posts/<str:post_id>/vote', views.postVote),
]
