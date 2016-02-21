from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'appls.app.views.index', name='index'),
    url(r'^api/login/', include('appls.login.urls')),
    url(r'^api/points/', include('appls.points.urls')),
    url(r'^api/message/', include('appls.message.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)