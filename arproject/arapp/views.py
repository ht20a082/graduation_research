import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views import View


class Ar_camViews(View):
    def get(self, request):
        return render(request, 'arapp/ar_cam.html', {})

def video_feed_view():
    return lambda _: StreamingHttpResponse(generate_frame(), content_type='multipart/x-mixed-replace; boundary=frame')

def generate_frame():
    capture = cv2.VideoCapture(0) 

    while True:
        if not capture.isOpened():
            print("Capture is not opened.")
            break
        ret, frame = capture.read()
        if not ret:
            print("Failed to read frame.")
            break

        ret, jpeg = cv2.imencode('.jpg', frame)
        byte_frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')
    capture.release()