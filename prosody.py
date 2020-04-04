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
    return render_template("<h1>hello prosody </h1>")

#*******************************************************************
import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds =6  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished
write('output.wav', fs, myrecording)  # Save as WAV file 

# # ******************************************************************
# # audio to text:
# import speech_recognition as sr 
# import os 
# from pydub import AudioSegment 
# from pydub.silence import split_on_silence 

# # a function that splits the audio file into chunks and applies speech recognition 
# def silence_based_conversion(path = "alice-medium.wav"): 

# 	# open the audio file stored in the local system as a wav file. 
# 	song = AudioSegment.from_wav(path) 

# 	# open a file where we will concatenate and store the recognized text 
# 	fh = open("recognized.txt", "w+") 
		
# 	# split track where silence is 0.or more and get chunks 
# 	chunks = split_on_silence(song, 
# 		# must be silent for at least 0.5 seconds or 500 ms. adjust this value based on user requirement. if the speaker stays silent for longer, increase this value. else, decrease it. 
# 		min_silence_len = 500, 

# 		# consider it silent if quieter than -16 dBFS adjust this per requirement 
# 		silence_thresh = -16
# 	) 

# 	# create a directory to store the audio chunks. 
# 	try: 
# 		os.mkdir('audio_chunks') 
# 	except(FileExistsError): 
# 		pass

# 	# move into the directory to store the audio files. 
# 	os.chdir('audio_chunks') 

# 	i = 0
# 	# process each chunk 
# 	for chunk in chunks: 
			
# 		# Create 0.5 seconds silence chunk 
# 		chunk_silent = AudioSegment.silent(duration = 10) 

# 		# add 0.5 sec silence to beginning and end of audio chunk. This is done so that it doesn't seem abruptly sliced. 
# 		audio_chunk = chunk_silent + chunk + chunk_silent 

# 		# export audio chunk and save it in the current directory. 
# 		print("saving chunk{0}.wav".format(i)) 
# 		# specify the bitrate to be 192 k 
# 		audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav") 

# 		# the name of the newly created chunk 
# 		filename = 'chunk'+str(i)+'.wav'

# 		print("Processing chunk "+str(i)) 

# 		# get the name of the newly created chunk in the AUDIO_FILE variable for later use. 
# 		file = filename 

# 		# create a speech recognition object 
# 		r = sr.Recognizer() 

# 		# recognize the chunk 
# 		with sr.AudioFile(file) as source: 
# 			# remove this if it is not working correctly. 
# 			r.adjust_for_ambient_noise(source) 
# 			audio_listened = r.listen(source) 

# 		try: 
# 			# try converting it to text 
# 			rec = r.recognize_google(audio_listened) 
# 			# write the output to the file. 
# 			fh.write(rec+". ") 

# 		# catch any errors. 
# 		except sr.UnknownValueError: 
# 			print("Could not understand audio") 

# 		except sr.RequestError as e: 
# 			print("Could not request results. check your internet connection") 

# 		i += 1

# 	os.chdir('..') 

# silence_based_conversion(path)