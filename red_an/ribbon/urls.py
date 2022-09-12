from django.urls import path
from .views import redirectRibbon, ribbonView, postView


urlpatterns = [
    path('', redirectRibbon),
    path('ribbon/', ribbonView, name='ribbon'),
    path('ribbon/<str:section_title>/<post_id>/', postView, name='post'),
]
