# syntax=docker/dockerfile:experimental
FROM ubuntu:18.04

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV AM_I_IN_A_DOCKER_CONTAINER True
ENV CHROME_VERSION=79.0.3945.88-1

RUN apt-get update && apt-get install -y \
python3 \
python3-pip \
python3-dev \
vim \
build-essential

RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget

# download and install chrome
# stable install
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
# specific install
RUN wget --no-check-certificate https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb
RUN dpkg -i google-chrome-stable_${CHROME_VERSION}_amd64.deb; apt-get -y -f install

# install dependencies
RUN python3 -m pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt

# Install python requirements
# using no cache
#RUN python3 -m pip install -r requirements.txt
# using cache
RUN --mount=type=cache,target=/root/.cache/pip python3 -m pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

# Start from a Bash prompt
CMD [ "/bin/bash" ]
