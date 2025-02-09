# AI-EMOtion Analysis Expert (Kernel Base) v0.5.2

A powerful AI-driven emotion recognition system integrating **Speech Emotion Recognition (SER)** and **Image Emotion Recognition (IER)**. This system enables real-time emotion detection using deep learning models, fully containerized for seamless deployment via **Docker**.

## ⚙️ System Requirements
- **Docker** installed on your local machine or server.
- **Docker Hub** access for pulling the latest image.
- **Sufficient computational resources** depending on operational scale.
![image](https://github.com/user-attachments/assets/b1b399fb-ca45-433a-a7af-629322aad469)
![image](https://github.com/user-attachments/assets/d2f69ff6-0099-479d-be96-bf1dac7896b7)

---

## 🚀 Deployment Guide

### **1️⃣ Pulling the Docker Image**
To start using **AI-EMO Expert**, pull the latest version from Docker Hub:
```bash
docker pull sammyfang/repository:v5
```

### **2️⃣ Running the Docker Container
Run the container in detached mode:

```bash
docker run -d --name sammyfang -p 8000:8000 sammyfang/repository:v5

-d runs the container in the background.
--name sammyfang assigns a name to the container.
-p 8000:8000 maps the port for external access.
```
### **3️⃣ Configuring the System
Mount a custom configuration file when starting the container:

```bash
docker run -d --name sammyfang \
  -v /path/to/your/config.cfg:/app/config.cfg \
  -p 8000:8000 sammyfang/repository:v5
```
Ensure that config.cfg includes:
```bash
ini
[Paths]
FACE = ./model/haarcascade_frontalface_default.xml
IER_MODEL = ./model/IER_CNN_Model.h5
SER_MODEL = ./model/SER_LSTM_Model.h5
VIDEO = ./VIDEO
AUDIO = ./AUDIO
OUTPUT_IER = ./output/IER.json
OUTPUT_SER = ./output/SER.json
[Settings]
READ_SEC = 60
```
### ** 4️⃣ Updating the System
To update to a newer version:

```bash
docker pull sammyfang/repository:new_version
docker stop sammyfang
docker rm sammyfang
docker run -d --name sammyfang -p 8000:8000 sammyfang/repository:new_version
```
📊 Result Output

▶ Speech Emotion Recognition (SER)
json
```bash
{
    "123.mp4": {
        "results": [
            {
                "Neutral": 0.1296,
                "Calm": 0.0047,
                "Happy": 0.7007,
                "Sad": 0.0200,
                "Angry": 0.0397,
                "Fear": 0.0021,
                "Disgust": 0.0948,
                "Surprise": 0.0080
            }
        ],
        "average_scores": {
            "Neutral": 0.5741,
            "Calm": 0.0060,
            "Happy": 0.2598,
            "Sad": 0.0084,
            "Angry": 0.1190,
            "Fear": 0.0029,
            "Disgust": 0.0206,
            "Surprise": 0.0088
        }
    }
}
```
🖼️ Image Emotion Recognition (IER)
json
```bash
{
    "123.mp4": {
        "samples": [
            [
                {
                    "Angry": 0.0258,
                    "Disgust": 0.0027,
                    "Fear": 0.0264,
                    "Happy": 0.7519,
                    "Neutral": 0.1316,
                    "Sad": 0.0525,
                    "Surprise": 0.0087
                },
                {
                    "Angry": 0.1729,
                    "Disgust": 0.0211,
                    "Fear": 0.1907,
                    "Happy": 0.1817,
                    "Neutral": 0.1420,
                    "Sad": 0.2401,
                    "Surprise": 0.0511
                }
            ]
        ],
        "FINAL": {
            "Angry": 0.0639,
            "Disgust": 0.0063,
            "Fear": 0.0802,
            "Happy": 0.4802,
            "Neutral": 0.3590,
            "Sad": 0.1119,
            "Surprise": 0.0574
        }
    }
}
```
### 📌 Key Features
* Real-time emotion analysis from speech & images.
* Pre-trained deep learning models for accurate predictions.
* Dockerized deployment for ease of use.
* Configurable settings for customizable execution.
* JSON-based output for integration with other applications.
### 🔥 Future Enhancements
* ✅ Improved Model Accuracy - Fine-tuning LSTM & CNN models.
* ✅ Real-time API Integration - Deploy as a RESTful API.
* ✅ GPU Acceleration - Optimize deep learning inference speed.
* ✅ Cloud Deployment - Support for AWS/GCP deployment.

### 📌 Useful Links
* Docker Hub Repository: sammyfang/repository
* Contact: 950154@gmail.com /Sammy Fang

### 📜 License
This project is for research usage only. Unauthorized distribution is prohibited.
