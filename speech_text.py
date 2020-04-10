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