FROM python:3.9.6-buster

WORKDIR /app-data
COPY . /app-data/

RUN mkdir /app-data/storage
RUN mkdir /app-data/temp

RUN apt-get -y update
RUN apt-get -y install ffmpeg libavcodec-extra

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "waitress_server.py"]
