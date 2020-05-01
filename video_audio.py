import time
from tensorflow.keras.preprocessing.image import img_to_array
from collections import Counter
import imutils
import cv2
from tensorflow.keras.models import load_model
import numpy as np
from sklearn.metrics import confusion_matrix
import cv2
import pyaudio
import wave
import operator
import speech_recognition as sr
import easygui

emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'
cascPath = 'models\haarcascade_frontalface_default.xml'  # dataset
faceCascade = cv2.CascadeClassifier(cascPath)
emotion_classifier = load_model(emotion_model_path, compile=False)
EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised", "neutral"]
video_capture = cv2.VideoCapture(0)  # 0 for web camera live stream
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 5
# filename = "output77.wav"
index=['./uploads/one.wav','./uploads/two.wav','./uploads/three.wav','./uploads/four.wav','./uploads/five.wav']

z={}
fee = "T"

def shutdown():
    global fee
    print("shutdown")
    fee = "F"
        
def audio_model():
    global fee
    filename = index.pop(0)
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    print('Recording')
    print(index)

    print(filename)
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    frames = []  # Initialize array to store frames
    for i in range(0, int(fs / chunk * seconds)):
        if( fee =="T"):
            data = stream.read(chunk)
            frames.append(data)
        else:
            print("End dabaya 1")
            break
    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
    
    print('Finished recording')
    
    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    index.insert(0, filename)
    fee = "T"
        
def check_audio():
    global z
    r = sr.Recognizer()
    filename = index.pop(0)
    with sr.AudioFile(filename) as source:
            audio_data = r.record(source)
    try:
        r.recognize_google(audio_data)
        print("ssup")
        key = "True"
        if (len(z)==0):
            print("inside Z")
            index.insert(0, filename)
            key = "False"
        z = {}
    except sr.RequestError:
        key = "False"
    except sr.UnknownValueError:
        print("Unknown value---")
        index.insert(0, filename)
        key = "False"
    return key

def camera_stream():
     # Capture frame-by-frame
    while(True):
        ret,frame = video_capture.read()
        frame = imutils.resize(frame,width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
        
        # else:continue

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
    # Display the resulting frame in browser
        return cv2.imencode('.jpg', frame)[1].tobytes()

def start_model():
    global fee,z
    print("video")
    val=[]
    t_end = time.time() + 10
    while time.time() < t_end:
        if(fee == "T"):
            ret ,frame = video_capture.read()
            canvas = np.zeros((250, 300, 3), dtype="uint8")
            canvas.fill(255)
            frame = imutils.resize(frame,width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            for (x, y, w, h) in faces:
                roi = gray[y:y + h, x:x + w]
                roi = cv2.resize(roi, (64, 64))
                roi = roi.astype("float") / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)
                preds = emotion_classifier.predict(roi)[0]
                emotion_probability = np.max(preds)
                label = EMOTIONS[preds.argmax()]
                val.append(preds.argmax())
                print(val)
        else:
            print("End dabaya 2")
            break
    (z)=dict(Counter(val))
    print(z)
    print(type(z))
    y=max(z.items(), key=operator.itemgetter(1))[0]
    print(y)
    emot=EMOTIONS[y]
    print(emot)
    with open("./uploads/emotions_coordinates.txt", "a") as text_file:
        text_file.write(str(z)+"\n")
    with open("./uploads/emotions.txt", "a") as text_file:
        text_file.write(str(emot)+"\n")
    fee = "T"

def destroy():
    cv2.destroyAllWindows()
    video_capture.release()
