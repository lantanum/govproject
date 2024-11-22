from django.contrib import admin
from django.urls import include, path
from myapp import views as myapp_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('myapp/', include('myapp.urls')),
    path('', myapp_views.main_view, name='main'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)