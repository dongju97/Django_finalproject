
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from topics import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('topics.urls')),
    path('detection/', include('detection.urls')),
    path('', views.main, name='main'),  # '/' 에 해당되는 path
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
