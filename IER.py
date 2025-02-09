import os
import cv2
import numpy as np
import json
from keras.models import load_model
from tensorflow.keras.utils import img_to_array
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')
face_path = config['Paths']['FACE']
model_path = config['Paths']['IER_MODEL']
video_path = config['Paths']['VIDEO']
output_path = config['Paths']['OUTPUT_IER']
read_sec = int(config['Settings']['READ_SEC'])

face_classifier = cv2.CascadeClassifier(face_path)
classifier = load_model(model_path)
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

video_files = [f for f in os.listdir(video_path) if f.endswith('.mp4')]
video_emotions = {}

for video_file in video_files:
    video_data = []
    cap = cv2.VideoCapture(os.path.join(video_path, video_file))
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    max_frame_count = int(frame_rate * read_sec)

    frame_count = 0
    emotion_totals = {emotion: 0.0 for emotion in emotion_labels}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame_count >= max_frame_count:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        frame_emotions = []
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)
                prediction = classifier.predict(roi)[0]
                emotion_probabilities = {emotion: float(prob) for emotion, prob in zip(emotion_labels, prediction)}
                frame_emotions.append(emotion_probabilities)
                for emotion in emotion_labels:
                    emotion_totals[emotion] += emotion_probabilities[emotion]
        if frame_emotions:
            video_data.append(frame_emotions)
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    num_samples = len(video_data)
    if num_samples > 0:
        average_emotions = {emotion: total / num_samples for emotion, total in emotion_totals.items()}
    else:
        average_emotions = {emotion: 0 for emotion in emotion_labels}

    video_emotions[video_file] = {
        "samples": video_data,
        "FINAL": average_emotions
    }
with open(output_path, 'w') as fp:
    json.dump(video_emotions, fp, indent=4)

print(f" >> Results have been saved to {output_path}")
