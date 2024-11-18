from django.contrib import admin
from django.urls import include, path
from children import views as children_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('children/', include('children.urls')),
    path('', children_view.main_view, name='main'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)