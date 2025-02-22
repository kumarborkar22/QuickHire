from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .views import attendance_view


urlpatterns = [
    path('', views.home, name='home'),
    path('attendance1/', views.attendance1, name='attendance1'),
    path('capture/', views.capture, name='capture'),
    path('attendance3/', views.attendance3, name='attendance3'),
    path('attendance4/', views.attendance4, name='attendance4'),
    
    path('video_feed/', views.video_feed, name='video_feed'),
    path('start_camera/', views.start_camera, name='start_camera'),
    path('stop_camera/', views.stop_camera, name='stop_camera'),
    path('capture_image/', views.capture_image, name='capture_image'),
    path('records/', views.attendance_records, name='attendance_records'),
    path('download/', views.download_attendance_csv, name='download_csv'),
    path('attendance/', attendance_view, name='attendance'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
