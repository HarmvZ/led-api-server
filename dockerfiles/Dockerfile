FROM resin/rpi-raspbian
COPY . /home/pi/app
RUN apt-get update && apt-get install -y make gcc python3 python3-dev python3-django python3-pip
RUN python3 -m pip install -U pip
RUN python3 -m pip install rpi-ws281x
CMD python3 /home/pi/app/manage.py runserver 0.0.0.0:8000