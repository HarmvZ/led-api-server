FROM resin/rpi-raspbian
COPY . /home/pi/app
RUN apt-get update && apt-get install -y make gcc python3 python3-dev python3-django python3-pip
RUN python3 -m pip install -U pip && python3 -m pip install -U django && python3 -m pip install numpy rpi-ws281x psutil python-crontab gTTS feedparser cron-descriptor