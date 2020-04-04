from flask import Blueprint,render_template,Response
from real_time_video import Emotion
from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
from sklearn.metrics import confusion_matrix
video=Blueprint("video",__name__,static_folder="static",template_folder="templates")


def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield cv2.imencode('.jpg', frame)[1].tobytes()
        
        # yield (b'--frame\r\n'b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n\r\n')
    # while True:
    #     frame = camera.get_frame()
    #     yield cv2.imshow(b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n'+frame+b'\r\n')


@video.route('/video')
def videofile():
    return Response(gen(Emotion()),mimetype='multipart/x-mixed-replace; boundary=frame')


# method 1:calls the class Emotion and yields from there itself

#methos 2: calls Emotion returns frameClone and yields here


# @video.route('/video')
# def videofile():
#     return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    # return Response(gen(VideoCamera()), mimetype='multipart/x-fixed-replace;boundary-frame')
    # return "<h1> heeloo</h1>"

# def get_frame():
#     camera_port=0
#     camera=cv2.VideoCapture(camera_port) #this makes a web cam object

#     while True:
#         retval, im = camera.read()
#         imgencode=cv2.imencode('.jpg',im)[1]
#         stringData=imgencode.tostring()
#         yield (b'--frame\r\n'
#             b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

#     del(camera)

# @video.route('/video')
# def videofile():
#      return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

# import pickle

# pickle.dump(('video.pkl','wb'))
# video=pickle.load(open('video.pkl','rb'))

