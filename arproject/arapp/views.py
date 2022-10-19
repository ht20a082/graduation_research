import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views import View
from pyzbar.pyzbar import decode, ZBarSymbol
from mainapp.models import *


class Ar_camViews(View):
    model = Image
    def get(self, request, pk):
        return render(request, 'arapp/ar_cam.html', {})

def video_feed_view():
    return lambda _: StreamingHttpResponse(generate_frame(), content_type='multipart/x-mixed-replace; boundary=frame')

def generate_frame():
    font = cv2.FONT_HERSHEY_SIMPLEX
    capture = cv2.VideoCapture(0) 

    while True:
        if not capture.isOpened():
            print("Capture is not opened.")
            break
        ret, frame = capture.read()
        if not ret:
            print("Failed to read frame.")
            break

        if ret:
            value = decode(frame, symbols = [ZBarSymbol.QRCODE])
            if value:
                for qrcode in value:
                    x, y, w, h = qrcode.rect

                    dec_inf = qrcode.data.decode('utf-8')
                    print('dec:', dec_inf)
                    frame = cv2.putText(frame, dec_inf, (x, y-6), font, .3, (255,0,0), 1, cv2.LINE_AA)

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 1)

        ret, jpeg = cv2.imencode('.jpg', frame)
        byte_frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')
    capture.release()