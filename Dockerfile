FROM python:3.9.1

COPY requirements.txt .

RUN pip install -r requirements.txt

