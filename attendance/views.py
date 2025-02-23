from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse, HttpResponse
import cv2
from django.conf import settings
import os
from .models import Attendance
import face_recognition
import csv
from django.utils.timezone import now

camera = cv2.VideoCapture(0)

def start_camera(request=None):
    """Start the camera if not already running."""
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
    return JsonResponse({"message": "Camera started"})

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def home(request):
    return render(request, 'attendance/attendance1.html')

def capture_image(request):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    success, frame = camera.read()
    
    if success:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(50, 50))

        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            image_path = os.path.join(settings.MEDIA_ROOT, "captured_face.jpg")
            cv2.imwrite(image_path, frame)

            return JsonResponse({
                "message": "Image saved successfully with face detection!",
                "image_url": settings.MEDIA_URL + "captured_face.jpg"
            })
        else:
            return JsonResponse({"error": "No face detected! Please position yourself in front of the camera."}, status=400)

    return JsonResponse({"error": "Failed to capture image"}, status=500)


def attendance_records(request):
    records = Attendance.objects.all().order_by('-timestamp')
    return render(request, 'attendance/records.html', {'records': records})

def capture_and_recognize(request):
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    camera.release()

    if ret:
        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            img_name = f"attendance_images/{now().strftime('%Y%m%d%H%M%S')}.jpg"
            img_path = os.path.join("media", img_name)
            cv2.imwrite(img_path, frame)

            attendance = Attendance(image=img_name)
            attendance.save()

            return JsonResponse({'image_url': f"/media/{img_name}", 'status': 'Face Detected'})
        else:
            return JsonResponse({'error': 'No Face Detected!'}, status=400)

    return JsonResponse({'error': 'Capture Failed!'}, status=400)

def download_attendance_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Timestamp', 'Image'])

    for record in Attendance.objects.all():
        writer.writerow([record.name, record.email, record.timestamp, record.image.url])

    return response

def stop_camera(request):
    global camera
    if camera is not None:
        camera.release()
        camera = None
    return JsonResponse({"message": "Camera stopped"})

def attendance1(request):
    return render(request, 'attendance/attendance1.html')

def capture(request):
    return render(request, 'attendance/capture.html')

def attendance3(request):
    timestamp = now().timestamp()
    image_url = settings.MEDIA_URL + "captured_face.jpg"
    return render(request, 'attendance/attendance3.html', {'image_url': image_url, 'timestamp': timestamp})


def attendance4(request):
    return render(request, 'attendance/attendance4.html')

def capture(request):
    return render(request, 'attendance/capture.html')

def attendance_view(request):
    return render(request, "attendance/attendance4.html")

from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def send_overtime_email(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email_subject = "Shift Completed - Overtime Request"
        email_message = data.get("message", "Your shift is completed. Do you want to do overtime?")
        recipient_email = "user@example.com"

        send_mail(
            email_subject,
            email_message,
            "kumarborkar403@gmail.com",
            [recipient_email],
            fail_silently=False,
        )

        return JsonResponse({"message": "Email sent successfully!"})

@csrf_exempt
def start_overtime(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("overtime_started"):
            return JsonResponse({"message": "Overtime started!"})
    
    return JsonResponse({"error": "Invalid request"}, status=400)

def attendance_view(request):
    return render(request, 'attendance/attendance1.html') #work nhi karat ahe...