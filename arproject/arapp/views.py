import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views import View
from pyzbar.pyzbar import decode, ZBarSymbol
from mainapp.models import *
from django.conf import settings
import numpy as np

prm = 1 #デフォルトのプライマリーキー

# グローバル変数prmを更新する関数
def update_prm(pk):
    global prm
    prm = pk

# 絵画の画像のパスを返す関数
def create_path():
    obj = Image.objects.get(id = prm)
    input_path = str(settings.BASE_DIR) + str(obj.thumbnail.url)
    return input_path

# 絵画の実際の高さを返す関数
def acqu_size_h():
    obj = Image.objects.get(id = prm)
    r_size = obj.height
    return r_size

def Ar_camViews(request, pk):
    update_prm(pk)
    video_feed_view()
    return render(request, 'arapp/ar_cam.html', {})


def video_feed_view():
    return lambda _: StreamingHttpResponse(generate_frame(), content_type='multipart/x-mixed-replace; boundary=frame')

#アフィン変換行列による絵画の画像とカメラ映像を合成する関数
def overlay(img, frame, shift, h, size, r_size):
    qr_size = 200   # QRコードの高さ
    k = size / h
    mag = (r_size / qr_size) / k    # 変換倍率

    shift_x, shift_y = shift
 
    frame_h, frame_w = frame.shape[:2]
    
    dx = shift_x
    dy = shift_y
    m = np.float32([[mag, 0, dx],[0, mag, dy]])
    frame = cv2.warpAffine(img, m, (frame_w, frame_h), frame, borderMode=cv2.BORDER_TRANSPARENT)
 
    return frame

def generate_frame():
    input_path = create_path()
    r_size = acqu_size_h()
    img = cv2.imread(input_path)

    font = cv2.FONT_HERSHEY_SIMPLEX

    
    capture = cv2.VideoCapture(1)

    capture.set(cv2.CAP_PROP_FPS, 30)

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

                    size = img.shape[0]

                    overlay(img, frame, (x, y), h, size, r_size)

        ret, jpeg = cv2.imencode('.jpg', frame)
        byte_frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')
    capture.release()