FROM resin/rpi-raspbian
COPY . /home/pi/app
RUN sudo apt-get update
#RUN sudo apt-get upgrade
RUN apt-get install python python-dev python-django python-pip
RUN cd /home/pi/app
CMD pip install rpi-ws812x
#CMD python manage.py runserver