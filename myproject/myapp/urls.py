from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('section/boxing/', views.boxing_view, name='boxing'),
    path('scan/', views.scan_view, name = 'scan'),
    path('profile/', views.profile_view, name = 'profile'),
    path('add_section/', views.add_section, name='add_section'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('add_client/', views.add_client, name='add_client'),
    path('add_organization/', views.add_organization, name='add_organization'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('generate-qr/', views.generate_qr, name='generate_qr'),
]
