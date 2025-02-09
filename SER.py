import librosa
import numpy as np
import random
import os
import json
from moviepy.editor import VideoFileClip
from keras.models import load_model
import glob
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

SER_MODEL = config['Paths']['SER_MODEL']
VIDEO_DIR = config['Paths']['VIDEO']
AUDIO_DIR = config['Paths']['AUDIO']
OUTPUT_SER = config['Paths']['OUTPUT_SER']
READ_SEC = int(config['Settings']['READ_SEC'])

def noise(data):
    noise_amp = 0.035 * np.random.uniform() * np.amax(data)
    return data + noise_amp * np.random.normal(size=data.shape[0])

def stretch(data, rate=0.85):
    return librosa.effects.time_stretch(y=data, rate=rate)

def shift(data):
    shift_range = int(np.random.uniform(low=-5, high=5) * 1000)
    return np.roll(data, shift_range)

def pitch(data, sampling_rate, pitch_factor=0.7):
    return librosa.effects.pitch_shift(y=data, sr=sampling_rate, n_steps=pitch_factor)

def extract_features(data, sample_rate):
    mfcc = librosa.feature.mfcc(y=data, sr=sample_rate)
    return mfcc

def transform_audio(data, sample_rate, fns):
    fn = random.choice(fns)
    if fn == pitch:
        fn_data = fn(data, sample_rate)
    elif fn == "None":
        fn_data = data
    else:
        fn_data = fn(data)
    return fn_data

def get_features(path):
    data, sample_rate = librosa.load(path, duration=READ_SEC)
    fns = [noise, pitch, "None"]
    result = []
    for i in range(0, len(data) - 2 * sample_rate, 2 * sample_rate):
        audio_sample = data[i:i + 3 * sample_rate]
        transformed_audio = transform_audio(audio_sample, sample_rate, fns)
        features = extract_features(transformed_audio, sample_rate)
        result.append(features[:,:108])
    return result

model = load_model(SER_MODEL)

results = {}
video_files = glob.glob(f"{VIDEO_DIR}/*.mp4")
if not video_files:
    print("No video files found in the directory.")
for video_path in video_files:
    video_name = os.path.basename(video_path)
    audio_path = os.path.join(AUDIO_DIR, video_name.replace('.mp4', '.wav'))
    print(audio_path)
    
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        print(f"Audio extracted for {video_name} and saved to {audio_path}.")
    except Exception as e:
        print(f"Failed to extract audio from {video_name}: {str(e)}")
        continue

    features = get_features(audio_path)
    if not features:
        print(f"No features extracted for {video_name}, possibly due to an empty audio file.")
        continue

    X = np.swapaxes(np.array(features), 1, 2)
    X = np.expand_dims(X, axis=3)
    predictions = model.predict(X)

    emotion_mapping = {0: 'Neutral', 1: 'Calm', 2: 'Happy', 3: 'Sad', 4: 'Angry', 5: 'Fear', 6: 'Disgust', 7: 'Surprise'}
    emotion_sums = {emotion: 0.0 for emotion in emotion_mapping.values()}
    video_results = []
    for prediction in predictions:
        emotion_scores = {emotion_mapping[i]: float(score) for i, score in enumerate(prediction)}
        video_results.append(emotion_scores)
        for emotion, score in emotion_scores.items():
            emotion_sums[emotion] += score

    average_emotion_scores = {emotion: sum_score / len(features) for emotion, sum_score in emotion_sums.items()}
    results[video_name] = {
        "results": video_results,
        "FINAL": average_emotion_scores
    }

with open(OUTPUT_SER, 'w') as f:
    json.dump(results, f, indent=4)

print("Emotion recognition has been performed on all videos.")