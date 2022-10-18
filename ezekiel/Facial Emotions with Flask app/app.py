import sys
import os
from turtle import title
import numpy as np
from predictemt import pred, removeout, vidframe, ssimscore1
from flask import Flask, request, render_template, flash, redirect

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

# video to audio
import moviepy
from moviepy.editor import *

# audio to text
import speech_recognition as sr

# get audio attribute
from uploads.getMusicAttribute import *

# convert mp3 file to wav        
from pydub import AudioSegment



# transcribe audio file  


                                                       
# load face detection cascade file
facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

app = Flask(__name__)
app.secret_key = 'some secret key'

def mp4_to_mp3(mp4, mp3, path):     
                mp4_without_frames = AudioFileClip(mp4)     
                mp4_without_frames.write_audiofile(path + "\\uploads\\" +mp3)     
                mp4_without_frames.close() 

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


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
            

            # extract audio
            mp4_to_mp3(basepath + "\\uploads\\" + f.filename, "temptaudiofile.wav", basepath)

            # find music attributes of audio
            artist, title = (postRequest("temptaudiofile.wav"))
            # run model that takes in artist and title
            print(artist,title)
            musicStatus = "Positive"
            
            # audio to text
            r = sr.Recognizer()
            with sr.AudioFile("C:\\Users\\PM\\OneDrive\\Documents\\GitHub\\MLA-project\\ezekiel\\Facial Emotions with Flask app\\uploads\\temptaudiofile.wav") as source:
                # listen for the data (load audio to memory)
                audio_data = r.record(source)
                # recognize (convert from speech to text)
                text = r.recognize_google(audio_data)
                # print("audio to text: --- " + text)
            #  run model that takes in text
            print(text)
            textStatus = "Positive"
            # running vidframe with the uploaded video
            result, face = vidframe(file_path)
            




            
            # removing the video as we dont need it anymore
            os.remove(file_path)
            
            


            
    
        else:
            result, face = vidframe(0)
        try:
            smileindex = result.count('happy')/len(result)  # smileIndex
            smileindex = round(smileindex, 2)

        except:
            smileindex = 0

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
        print("count:" + str(temp_counts))
        #counts = [result.count('angry'),result.count('disgust'),result.count('fear'),result.count('happy'),result.count('sad')]
        ax.pie(temp_counts, labels=temp_emotions,
               autopct='%1.2f%%')  # adding pie chart
        img = io.BytesIO()
        plt.savefig(img, format='png')  # saving piechart
        img.seek(0)
        # piechart object that can be returned to the html
        plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode())
        # returning all the three variable that can be displayed in html
        return render_template("predict.html", posture=posture, smileindex=smileindex, plot_url=plot_data, musicStatus = musicStatus, textStatus = textStatus)
    return None


if __name__ == '__main__':
    app.run(debug=True)
    app.secret_key = 'some secret key'
