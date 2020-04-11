from flask import Blueprint,render_template
from sys import argv
import numpy as np
from pyAudioAnalysis import audioTrainTest as aT
import pydub

prosody=Blueprint("prosody",__name__,static_folder="static",template_folder="templates")

@prosody.route("/prosody")
def prosodyfile():
    script, filename = argv
    isSignificant = 0.8 #try different values.
    # P: list of probabilities
    Result, P, classNames = aT.file_classification(filename, "svmModel1", "svm")
    print(("result is", Result))
    print(("classNames is", classNames))
    print(("P is", P))
    print(("result is", Result))
    winner = np.argmax(P) #pick the result with the highest probability value.
    # is the highest value found above the isSignificant threshhold? 
    #if P[winner] > isSignificant :
    print(("File: " +filename + " is in category: " + classNames[winner] + ", with probability: " + str(P[winner])))
    #else :
    #print("Can't classify sound: " + str(P))
    # return render_template("<h1>hello prosody </h1>")

# **********************************************************************
# import pyaudio
# import wave

# chunk = 1024  # Record in chunks of 1024 samples
# sample_format = pyaudio.paInt16  # 16 bits per sample
# channels = 2
# fs = 44100  # Record at 44100 samples per second
# seconds = 3
# filename = "output.wav"

# 
# p = pyaudio.PyAudio()  # Create an interface to PortAudio

# print('Recording')

# stream = p.open(format=sample_format,
#                 channels=channels,
#                 rate=fs,
#                 frames_per_buffer=chunk,
#                 input=True)

# frames = []  # Initialize array to store frames

# # Store data in chunks for 3 seconds
# for i in range(0, int(fs / chunk * seconds)):
#     data = stream.read(chunk)
#     frames.append(data)

# # Stop and close the stream 
# stream.stop_stream()
# stream.close()
# # Terminate the PortAudio interface
# p.terminate()

# print('Finished recording')

# # Save the recorded data as a WAV file
# wf = wave.open(filename, 'wb')
# wf.setnchannels(channels)
# wf.setsampwidth(p.get_sample_size(sample_format))
# wf.setframerate(fs)
# wf.writeframes(b''.join(frames))
# wf.close()


import speech_recognition as sr
import numpy as np
import soundfile as sf

# data, samplerate = sf.read('output.wav')
# sf.write('last.flac', data, samplerate)
filename = "finaltest.wav"
r = sr.Recognizer()
with sr.AudioFile(filename) as source:
    audio_data = r.record(source)
    text = r.recognize_google(audio_data)
    print(text)