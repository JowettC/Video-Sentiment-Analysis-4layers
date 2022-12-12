# Video-Sentiment-Analysis

## What the project is about?
![plot](./overview.jpg)

It is web appication that allows uploading of videos to perform sentiment anaylsis. The possible output labels are [positive, negative, mixed]. 

The video is split into 4 layers (can be reference from the picture above)
### Audio - music
1. LinearSVC Model was built using spotify api to get certain engineered features. Has an F1-score of 80%
2. Uses audd api to identify music before using the model

### Audio - text
1. Uses speech to text api
2. uses Voting classifer model. Has an F1-score of 85%~

### object detection
1. uses Yolov5, best opensource standard out there

### Emotion Analysis
1. Identify smiling index of face from video
2. CNN Facial Emotion Detection Model

For more details:
https://docs.google.com/presentation/d/1jLyBqeoLTSscScPBxedaUsNb95lAfZBWbvQHMSe2Q8c/edit?usp=sharing



## How to run the project
1. Create your python virtual environment - (Optional)
2.  Run Command `` pip install -r requirements.txt `` (Do note that it might take awhile as there are a lot of dependencies)
3. go into the directory ``integrated/webapp/``
4. Run Command ``python app.py``
5. Open your browser and go to http://localhost:5000/

## Important to note 
Some External modules/api require API token to access their services, they may have expired. List of modules that require API token are as follows:
- https://docs.audd.io/#api-methods - get music attributes (title & artist, etc)

- require env file to use spotify API (We included it in our files already for faster access)
CLIENT_ID=""
CLIENT_SECRET="""
