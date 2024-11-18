from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('', views.main_view, name='main'),
    path('section/boxing/', views.boxing_view, name='boxing'),
]
