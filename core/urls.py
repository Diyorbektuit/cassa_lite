from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .schema import swagger_urlpatterns

v1_urls = [
    path('auth/', include('apps.user.urls.auth')),
    path('', include('apps.transactions.urls')),
    path('profile/', include('apps.user.urls.profile'))
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((v1_urls, 'v1'), namespace='v1')),
]


urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += [
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    ]