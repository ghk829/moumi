FROM ubuntu:16.04

RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y git
RUN git clone https://github.com/ghk829/moumi.git
RUN apt install -y python3-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev
RUN pip3 install -r moumi/requirements.txt
ENTRYPOINT /moumi/start_app.sh