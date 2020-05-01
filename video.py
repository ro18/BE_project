import cv2
from flask import Blueprint,render_template,Response
from flask import jsonify, request, url_for,session,redirect
from video_audio import camera_stream
from video_audio import start_model
from video_audio import audio_model
from keras.preprocessing.image import img_to_array
import imutils
from keras.models import load_model
import numpy as np
from sklearn.metrics import confusion_matrix
import time
from multiprocessing import Process
from threading import Thread
import sys
from concurrent.futures import ThreadPoolExecutor
from video_audio import shutdown

index_counter=['emo1','emo2']

video=Blueprint("video",__name__,static_folder="static",template_folder="templates")

executor = ThreadPoolExecutor(2)

def gen_frame():
    """Video streaming generator function."""
    while True:
        frame = camera_stream()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') # concate frame one by one and show result

@video.route('/videofile')
def videofile():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@video.route('/start')
def start():
    # x=[[0 for i in range(2)] for j in range(2)] 
    # x=[3][]
    # global index_counter
    # x[index_counter][]=executor.submit(start_model)
    # val=index_counter.pop(0)
    # print( x[index_counter])
    # print("in start:{}".format(index_counter))
    # session['emotions']=['e_one','e_two','e_three']
    executor.submit(start_model)
    executor.submit(audio_model)
    print("start models")
    # return jsonify(description=d)
    # else:
    #     return render_template("student2.html")
    return '',204

@video.route('/end')
def end():
    shutdown()
    return '', 204


# https://stackoverflow.com/questions/22615475/flask-application-with-background-threads
