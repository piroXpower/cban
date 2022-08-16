FROM python:3.9.7-slim-buster
RUN apt-get update && apt-get upgrade -y
RUN pip3 install -U pip
COPY . /blaze/
WORKDIR /blaze/
RUN pip3 install -U -r requirements.txt
CMD python3 main.py
