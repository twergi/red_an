from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name='api'),
    path('sections/', views.getSections),
    path('sections/<str:section_id>', views.getSection),
    path('sections/<str:section_id>/posts', views.getPosts),
    path('sections/<str:section_id>/posts/<str:post_id>', views.getPost),
    path('sections/<str:section_id>/posts/<str:post_id>/vote', views.postVote),
    path('sections/<str:section_id>/posts/<str:post_id>/comments/<str:comment_id>/vote', views.commentVote),
    path('users/<str:username>/voted_posts', views.getVotedPosts),
    path('users/<str:username>/posts/<str:post_id>/voted_comments', views.getVotedComments),
]
