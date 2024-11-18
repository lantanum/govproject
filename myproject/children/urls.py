from django.urls import path
from . import views

urlpatterns = [
    path('add_child/', views.add_child, name='add_child'),
    path('', views.main_view, name='main'),
    path('section/boxing/', views.boxing_view, name='boxing'),
    path('scan/', views.scan_view, name = 'scan'),
    path('profile/', views.profile_view, name = 'profile'),
    path('identify_child/', views.identify_child, name='identify_child'),
]
