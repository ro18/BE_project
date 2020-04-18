from flask import Blueprint,render_template
from sys import argv
import numpy as np
from pyAudioAnalysis import audioTrainTest as aT
import pydub
import glob, os
import speech_recognition as sr
import numpy as np
import soundfile as sf
import docx
# os.chdir("audio")




# prosody=Blueprint("prosody",__name__,static_folder="static",template_folder="templates")

# @prosody.route("/prosody")



def prosodyfile():
    for filename in glob.glob("./audio/*.wav"):
        isSignificant = 0.8 #try different values.
        # P: list of probabilities
        Result, P, classNames = aT.file_classification(filename, "svmModel1", "svm")
        print(("result is", Result))
        print(("classNames is", classNames))
        print(("P is", P))
        print(("result is", Result))
        winner = np.argmax(P) 
        #if P[winner] > isSignificant :
        with open("audio_emotions.txt", "a") as text_file:
            text_file.write("Your emotion for question no  " +filename + " is in category: " + classNames[winner] + ", with probability: " + str(P[winner])+"\n")
        # with open("audio_coordinates.txt", "a") as text_file:
        #     text_file.write(P+"\n")

        
        data, samplerate = sf.read(filename)
        # sf.write('last.flac', data, samplerate)
        # filename = "finaltest.wav"
        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data,language="en-IN")
            print(text)
            print(type(text))
            # with open("audio_text.docx", "a") as text_file:
            #     text_file.write(text+"\n")
            mydoc = docx.Document()
            mydoc.add_paragraph(text)
            mydoc.save("./audio_text.docx")
            print("after writing docx")   
            with open("audio_text.txt", "a") as text_file:
                text_file.write(text+"\n")
# print(())
#else :
    #print("Can't classify sound: " + str(P))
    # return render_template("<h1>hello prosody </h1>")
