# syntax=docker/dockerfile:1

FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install python3.8 python3.8-dev python3-pip -y
RUN apt-get install -y python3-markupsafe
RUN python3.8 -m pip install Cython
WORKDIR /raga-detector
COPY requirements.txt requirements.txt
RUN python3.8 -m pip install -r requirements.txt

COPY . .

CMD [ "export", "FLASK_APP=app"]
EXPOSE 8080
EXPOSE 7000
CMD [ "python3.8", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]
