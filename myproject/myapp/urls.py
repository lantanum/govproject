from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('section/boxing/', views.boxing_view, name='boxing'),
    path('scan/', views.scan_view, name = 'scan'),
    path('profile/', views.profile_view, name = 'profile'),
]
