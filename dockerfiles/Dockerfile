FROM balenalib/raspberrypi3-debian-python:latest
COPY . /home/pi/app
COPY dockerfiles/env /etc/environment
RUN apt-get update && apt-get install -y make gcc python3 python3-dev python3-django python3-pip git cron

# Install python dependencies
RUN python3 -m pip install -U pip && python3 -m pip install setuptools && python3 -m pip install -r /home/pi/app/requirements/local.txt 