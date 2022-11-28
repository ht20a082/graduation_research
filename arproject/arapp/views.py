import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views import View
from pyzbar.pyzbar import decode, ZBarSymbol
from mainapp.models import *
from django.conf import settings
import numpy as np

prm = 2

def Ar_camViews(request, pk):
    model = Image
    global prm
    prm = pk
    #prm = Image.objects.latest('id').id
    return render(request, 'arapp/ar_cam.html', {})


def video_feed_view():
    #max_id = Image.objects.latest('id').id
    #prm_obj = Ar_camViews()
    #print(prm_obj.prm)
    obj = Image.objects.get(id = prm)
    input_path = str(settings.BASE_DIR) + str(obj.thumbnail.url)
    r_size = obj.height
    #output_path = settings.BASE_DIR + "/media/output/output.jpg"
    return lambda _: StreamingHttpResponse(generate_frame(input_path, r_size), content_type='multipart/x-mixed-replace; boundary=frame')

def overlay(img, frame, shift, h, size, r_size):
    k = size / h
    mag = (r_size / 200) / k

    shift_x, shift_y = shift
 
    img_h, img_w = img.shape[:2]
    img_x_min, img_x_max = 0, img_w
    img_y_min, img_y_max = 0, img_h
 
    frame_h, frame_w = frame.shape[:2]
    frame_x_min, frame_x_max = shift_y, shift_y+img_h
    frame_y_min, frame_y_max = shift_x, shift_x+img_w
 
    if frame_x_min < 0:
        img_x_min = img_x_min - frame_x_min
        frame_x_min = 0
         
    if frame_x_max > frame_w:
        img_x_max = img_x_max - (frame_x_max - frame_w)
        frame_x_max = frame_w
 
    if frame_y_min < 0:
        img_y_min = img_y_min - frame_y_min
        frame_y_min = 0
         
    if frame_y_max > frame_h:
        img_y_max = img_y_max - (frame_y_max - frame_h)
        frame_y_max = frame_h        
 
    #frame[frame_y_min:frame_y_max, frame_x_min:frame_x_max] = img[img_y_min:img_y_max, img_x_min:img_x_max]
    dx = shift_x
    dy = shift_y
    m = np.float32([[mag, 0, dx],[0, mag, dy]])
    frame = cv2.warpAffine(img, m, (frame_w, frame_h), frame, borderMode=cv2.BORDER_TRANSPARENT)

    M = cv2.getRotationMatrix2D((int(dx), int(dy)), 0, mag)
    print(M)
    #frame = cv2.warpAffine(img, M, (frame_w, frame_h), frame, borderMode=cv2.BORDER_TRANSPARENT)
 
    return frame

def generate_frame(input_path, r_size):
    #img = cv2.imread('C:\\Users\\ht20a082\\Desktop\\graduation_research\\arproject\\media\\0001.jpg')
    img = cv2.imread(input_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

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

                    #img2 = cv2.resize(img , (int(width*0.05), int(height*0.05)))

                    #frame[y:y+img2.shape[0], x:x+img2.shape[1]] = img2

                    size = img.shape[0]

                    overlay(img, frame, (x, y), h, size, r_size)

        ret, jpeg = cv2.imencode('.jpg', frame)
        byte_frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')
    capture.release()