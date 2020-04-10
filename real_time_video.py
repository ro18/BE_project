# from keras.preprocessing.image import img_to_array

from tensorflow.keras.preprocessing.image import img_to_array
import imutils
import cv2
# from keras.models import load_model
from tensorflow.keras.models import load_model
import numpy as np
from sklearn.metrics import confusion_matrix
import cv2
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
# import keras.backend.tensorflow_backend as tb
# tb._SYMBOLIC_SCOPE.value = True

emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'
cascPath = 'models\haarcascade_frontalface_default.xml'  # dataset
faceCascade = cv2.CascadeClassifier(cascPath)
emotion_classifier = load_model(emotion_model_path, compile=False)
EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised", "neutral"]
video_capture = cv2.VideoCapture(0)  # 0 for web camera live stream
#  for cctv camera'rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp'
#  example of cctv or rtsp: 'rtsp://mamun:123456@101.134.16.117:554/user=mamun_password=123456_channel=1_stream=0.sdp'


def camera_stream():
     # Capture frame-by-frame
    ret, frame = video_capture.read()
    while(True):
        frame = imutils.resize(frame,width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        canvas = np.zeros((250, 300, 3), dtype="uint8")
        canvas.fill(255)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
            roi = gray[y:y + h, x:x + w]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            preds = emotion_classifier.predict(roi)[0]
            emotion_probability = np.max(preds)
            label = EMOTIONS[preds.argmax()]
            
            # print("{},{}".format(label,emotion_probability))
            print(preds.argmax())
        # else:continue

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
    # Display the resulting frame in browser
        return cv2.imencode('.jpg', frame)[1].tobytes()



#*******************************************************************************************************************************


# detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'
# emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'

# face_detection = cv2.CascadeClassifier(detection_model_path)
# emotion_classifier = load_model(emotion_model_path, compile=False)
# EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised",
#  "neutral"]


# cv2.namedWindow('your_face')
# camera = cv2.VideoCapture(0)
# while True:
#     frame = camera.read()[1]
#     frame = imutils.resize(frame,width=500)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_detection.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)

#     canvas = np.zeros((250, 300, 3), dtype="uint8")
#     canvas.fill(255)

#     frameClone = frame.copy()
#     if len(faces) > 0:
#         faces = sorted(faces, reverse=True,
#         key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
#         (fX, fY, fW, fH) = faces
#         #ROI CALCULATED HERE
#         roi = gray[fY:fY + fH, fX:fX + fW]
#         roi = cv2.resize(roi, (64, 64))
#         roi = roi.astype("float") / 255.0
#         roi = img_to_array(roi)
#         roi = np.expand_dims(roi, axis=0)


#         preds = emotion_classifier.predict(roi)[0]
#         emotion_probability = np.max(preds)
#         label = EMOTIONS[preds.argmax()]
#     else: continue


#     for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):

#                 text = "{}: {:.2f}%".format(emotion, prob * 100)
# #COLOURS IDHAR
#                 w = int(prob * 300)
#                 cv2.rectangle(canvas, (7, (i * 35) + 5),
#                 (w, (i * 35) + 35), (0, 0, 0), -1)
#                 cv2.putText(canvas, text, (10, (i * 35) + 23),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.45,
#                 (120, 120, 120), 2)
#                 cv2.putText(frameClone, label, (fX, fY - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)
#                 cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH),
#                               (0, 0, 0), 2)


#     cv2.imshow('your_face', frameClone)
#     cv2.imshow("Probabilities", canvas)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# camera.release()
# cv2.destroyAllWindows()







#************************************************************************************************************************************************************************

# detection_model_path = 'models/haarcascade_frontalface_default.xml'
# emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'

# face_detection = cv2.CascadeClassifier(detection_model_path)
# emotion_classifier = load_model(emotion_model_path, compile=False)
# EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised",
#  "neutral"]

# class Emotion(object):
#     def get_frame(self):
#         cv2.namedWindow('your_face')
#         camera = cv2.VideoCapture(0)
#         while True:
#             frame = camera.read()[1]
#             frame = imutils.resize(frame,width=500)
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = face_detection.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)

#             canvas = np.zeros((250, 300, 3), dtype="uint8")
#             canvas.fill(255)

#             frameClone = frame.copy()
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
#             else: continue


#             for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):

#                 text = "{}: {:.2f}%".format(emotion, prob * 100)
# #COLOURS IDHAR
#                 w = int(prob * 300)
#                 cv2.rectangle(canvas, (7, (i * 35) + 5),
#                 (w, (i * 35) + 35), (0, 0, 0), -1)
#                 cv2.putText(canvas, text, (10, (i * 35) + 23),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.45,
#                 (120, 120, 120), 2)
#                 cv2.putText(frameClone, label, (fX, fY - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)
#                 cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH),
#                             (0, 0, 0), 2)


#             cv2.imshow('your_face', frameClone)
#             cv2.imshow("Probabilities", canvas)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#             return frameClone
            
#     # get_frame()
#         camera.release()
#         cv2.destroyAllWindows()


