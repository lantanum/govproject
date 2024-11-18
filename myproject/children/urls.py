from django.urls import path
from . import views

urlpatterns = [
    path('add_child/', views.add_child, name='add_child'),
    path('', views.home, name='home'), 
]
