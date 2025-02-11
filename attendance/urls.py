from django.urls import path
from .views import home, video_feed
from .views import video_feed, capture_image, attendance_records, download_attendance_csv, start_camera, stop_camera


urlpatterns = [
    path('', home, name='home'),
    path('video_feed/', video_feed, name='video_feed'),
    path("start_camera/", start_camera, name="start_camera"),
    path("stop_camera/", stop_camera, name="stop_camera"),
    path('capture_image/', capture_image, name='capture_image'),
    path('records/', attendance_records, name='attendance_records'),
    path('download/', download_attendance_csv, name='download_csv'),
]
