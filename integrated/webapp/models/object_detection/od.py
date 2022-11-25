import torch
from google.colab.patches import cv2_imshow
import cv2
import pandas as pd

def object_detection(video_path):
    temp = []
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n')

    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter('outputVideo.avi',cv2.VideoWriter_fourcc('M','J','P','G'), cap.get(5), (frame_width,frame_height))
    # Minor issue: original video 29 secs but the output video is 41 secs. The FPS of it affects the length.
    # I used cap.get(5) which is the video's FPS. If change to a higher fps e.g. 60, the video became shorter (20sec) 
    while True:
        img = cap.read()[1]
        cap.set(cv2.CAP_PROP_FPS, 60)
        #fps = int(cap.get(5))
        #print("fps:", fps)
        if img is None:
            break
        result = model(img)
        df = result.pandas().xyxy[0]
        temp.append(df)

        for ind in df.index:
            x1, y1 = int(df['xmin'][ind]), int(df['ymin'][ind])
            x2, y2 = int(df['xmax'][ind]), int(df['ymax'][ind])
            label = df['name'][ind]
            conf = df['confidence'][ind]
            text = label + ' ' + str(conf.round(decimals= 2))
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 2)
            cv2.putText(img, text, (x1, y1 - 5), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
            out.write(img)

    df_res = pd.concat(temp)
    df_res.to_csv('outputVideo.csv')
    return True
object_detection("../../uploads/happywithmusic2.mp4")