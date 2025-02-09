FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir opencv-python-headless numpy keras tensorflow configparser moviepy librosa pandas
RUN mkdir -p model output VIDEO AUDIO
EXPOSE 5000
CMD ["python", "sammy.py"]