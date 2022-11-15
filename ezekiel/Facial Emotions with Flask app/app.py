import sys
import os
from turtle import pos, title
import numpy as np
from predictemt import pred, removeout, vidframe, ssimscore1
from flask import Flask, request, render_template, flash, redirect
import pickle
from werkzeug.utils import secure_filename
import shutil
from tensorflow.keras.models import model_from_json
import cv2
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from matplotlib import pyplot as plt
import io
import base64
import urllib
from models.music_sentiment.music_mood_prediction import get_song
# video to audio
import moviepy
from moviepy.editor import *
# audio to text
import speech_recognition as sr
# get audio attribute
from uploads.getMusicAttribute import *
# convert mp3 file to wav        
from pydub import AudioSegment
# text analysis
from models.text_analysis.text_sentiment import predict



# transcribe audio file  


                                                       
# load face detection cascade file
facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

app = Flask(__name__)
app.secret_key = 'some secret key'

def mp4_to_mp3(mp4, mp3, path):     
                mp4_without_frames = AudioFileClip(mp4)     
                writePath = os.path.join(path,"uploads",mp3)
                mp4_without_frames.write_audiofile(writePath)     
                mp4_without_frames.close() 

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/loading', methods=['GET'])
def loading():
    return render_template('loading.html')

def getResults(result):
    for word in result:
        word = word.upper()
    posCount = result.count("POSITIVE")
    negCount = result.count("NEGATIVE")
    print(result)
    if "UNKNOWN" in result:
        if(posCount > negCount):
            return "POSITIVE"
        elif(negCount > posCount):
            return "NEGATIVE"
        else:
            return "MIXED"
    else:
        if posCount == 1:
            return "MIXED POSITIVE"
        elif negCount == 1:
            return "MIXED POSITIVE"
        elif posCount == 3:
            return "POSITIVE"
        else:
            return "NEGATIVE"


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' in request.files:
            
            f = request.files['file']  # getting uploaded video
            basepath = os.path.dirname(__file__)
            print("basepath:" + basepath)
            file_path = os.path.join(
                basepath, 'uploads', secure_filename(f.filename))
            f.save(file_path)  # saving uploaded video
            # positive, negative, mixed postive and mix negative
            overallResult = []

            # extract audio
            
            mp4_to_mp3(os.path.join(basepath,"uploads", f.filename), "temptaudiofile.wav", basepath)
            try:
            # find music attributes of audio
                artist, title = (postRequest("temptaudiofile.wav"))
            # run model that takes in artist and title

                model = pickle.load(open('./models/music_sentiment/LSVC_best.pkl', 'rb'))
           
                musicStatus = get_song(artist,title,model)
                musicDetails = [artist,title]
                overallResult.append(musicStatus.upper())
            except:
                musicStatus = "Unknown"
                musicDetails = ["Unknown","Unknown"]
                overallResult.append("UNKNOWN")
            
            # audio to text
            try:
                r = sr.Recognizer()
                pathToWav = os.path.join(basepath,"uploads","temptaudiofile.wav")
                with sr.AudioFile(pathToWav) as source:
                    # listen for the data (load audio to memory)
                    audio_data = r.record(source)
                    # recognize (convert from speech to text)
                    text = r.recognize_google(audio_data)
                    # print("audio to text: --- " + text)

                #  run model that takes in text
                # print(text)
                textDetails = text
                textStatus = predict(text)
                overallResult.append(textStatus.upper())
            except: 
                textStatus = "UNKNOWN"
                textDetails = "UNKNOWN"
                overallResult.append("UNKNOWN")
            # running vidframe with the uploaded video
            result, face = vidframe(file_path)
            # removing the video as we dont need it anymore
            # os.remove(file_path)
            
    
        else:
            result, face = vidframe(0)
        try:
            smileindex = result.count('happy')/len(result)  # smileIndex
            smileindex = round(smileindex, 2)

        except:
            smileindex = "UNKNOWN"
            overallResult.append("UNKNOWN")
        if (smileindex != "UNKNOWN"):
            if smileindex > 0.5:
                overallResult.append("POSITIVE")
            else:
                overallResult.append("NEGATIVE")

        # calculating similarityscore for images
        ssimscore = [ssimscore1(i, j) for i, j in zip(face[: -1], face[1:])]
        if np.mean(ssimscore) < 0.6:
            posture = "Not Good"
        else:
            posture = "Good"
        fig = plt.figure()  # matplotlib plot
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('equal')
        #emotion = ['angry','disgust','fear', 'happy', 'sad']
        temp_emotions = ['positive', 'negative']
        positive = result.count('happy')
        negative = (result.count('angry') + result.count('disgust') +
                    result.count('fear') + result.count('sad'))/4
        temp_counts = [positive, negative]
        # this is the result for emotion recognition
        # print("count:" + str(temp_counts))
        #counts = [result.count('angry'),result.count('disgust'),result.count('fear'),result.count('happy'),result.count('sad')]
        try: 
            ax.pie(temp_counts, labels=temp_emotions,
               autopct='%1.2f%%')  # adding pie chart
            img = io.BytesIO()
            plt.savefig(img, format='png')  # saving piechart
            img.seek(0)
            # piechart object that can be returned to the html
            plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode())
        except:
            smileindex = "UNKNOWN"
            posture ="UNKNOWN"
            plot_data="UNKNOWN"
        # returning all the three variable that can be displayed in html

        return render_template("predict.html", posture=posture, smileindex=smileindex, plot_url=plot_data, musicStatus = musicStatus, musicDetails=musicDetails, textStatus = textStatus, textDetails = textDetails, result = getResults(overallResult))
    return None


if __name__ == '__main__':
    app.run(debug=True)
    app.secret_key = 'some secret key'
