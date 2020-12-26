FROM python:3.9.1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip freeze > requirements.txt

COPY . /app/sneakers/
ENV PYTHONPATH "${PYTHONPATH}:/app/sneakers"