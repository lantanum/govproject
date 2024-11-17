from django.urls import include, path

urlpatterns = [
    # Другие маршруты...
    path('accounts/', include('accounts.urls')),
]
