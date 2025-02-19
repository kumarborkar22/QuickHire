from django.urls import path
from .import views
from .views import home, video_feed
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from .views import attendance1 ,video_feed, capture_image, attendance_records, download_attendance_csv, start_camera, stop_camera


urlpatterns = [
    path('', home, name='home'),
    path('attendance1/', views.attendance1, name='attendance1'),  # Keep other pages
    path('video_feed/', video_feed, name='video_feed'),
    path("start_camera/", start_camera, name="start_camera"),
    path("stop_camera/", stop_camera, name="stop_camera"),
    path('capture_image/', capture_image, name='capture_image'),
    path('records/', attendance_records, name='attendance_records'),
    path('download/', download_attendance_csv, name='download_csv'),
    path('attendance3/', views.attendance3, name='attendance3'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
