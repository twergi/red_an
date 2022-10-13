from django.urls import path
from . import views


urlpatterns = [
    path('', views.redirectRibbon),
    path('ribbon/', views.ribbonView, name='ribbon'),
    path('vote/', views.votePOST),
    path('sections/', views.sectionsView, name='sections'),
    path('sections/create/', views.SectionCreate, name='section_create'),
    path('sections/<str:section_title>/', views.sectionView, name='section'),
    path('sections/<str:section_title>/edit/', views.SectionEdit, name='section_edit'),
    path('sections/<str:section_title>/delete/', views.SectionDelete, name='section_delete'),
    path('sections/<str:section_title>/post/create/', views.postCreate, name='post_create'),
    path('sections/<str:section_title>/post/<post_id>/', views.postView, name='post'),
    path('sections/<str:section_title>/post/<post_id>/edit/', views.postEdit, name='post_edit'),
    path('sections/<str:section_title>/post/<post_id>/delete/', views.postDelete, name='post_delete'),
]
