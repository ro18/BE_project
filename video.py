import cv2
from flask import Blueprint,render_template,Response
# from real_time_video import Emotion

from real_time_video import camera_stream
from keras.preprocessing.image import img_to_array
import imutils
from keras.models import load_model
import numpy as np
from sklearn.metrics import confusion_matrix
import time

video=Blueprint("video",__name__,static_folder="static",template_folder="templates")

def gen_frame():
    """Video streaming generator function."""
    while True:
        frame = camera_stream()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') # concate frame one by one and show result

@video.route('/videofile')
def videofile():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




# def gen():
#     detection_model_path = 'models/haarcascade_frontalface_default.xml'
#     emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5' 

#     face_detection = cv2.CascadeClassifier(detection_model_path)
#     emotion_classifier = load_model(emotion_model_path, compile=False)
#     EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised","neutral"]

#     cv2.namedWindow('your_face')
#     cap =cv2.VideoCapture(-1)
#     print("hello1")
#     # Read until video is completed
#     while(cap.isOpened()):
#       # Capture frame-by-frame
#         ret, img = cap.read()
#         if ret == True:
            
#             # img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
#             img = imutils.resize(frame,width=500) 
#             print("before gray")
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             faces = face_detection.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
#             canvas = np.zeros((250, 300, 3), dtype="uint8")
#             canvas.fill(255)

#             print("before clone")
#             frameClone = img.copy()
#             if len(faces) > 0:
#                 faces = sorted(faces, reverse=True,
#                 key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
#                 (fX, fY, fW, fH) = faces
#                 #ROI CALCULATED HERE
#                 roi = gray[fY:fY + fH, fX:fX + fW]
#                 roi = cv2.resize(roi, (64, 64))
#                 roi = roi.astype("float") / 255.0
#                 roi = img_to_array(roi)
#                 roi = np.expand_dims(roi, axis=0)


#                 preds = emotion_classifier.predict(roi)[0]
#                 emotion_probability = np.max(preds)
#                 label = EMOTIONS[preds.argmax()]
#                 print(label)
#             else: continue
#             cv2.putText(frameClone, label, (fX, fY - 10),
#             cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)
#             cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH),(0, 0, 0), 2)


#             cv2.imshow('your_face', frameClone)
#             frame = cv2.imencode('.jpg',  frameClone)[1].tobytes()
#             yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#             time.sleep(0.1)
#         else: 
#             break

# @video.route('/video')
# def videofile():
#     return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

