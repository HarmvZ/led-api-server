from django.shortcuts import render
from django.http import HttpResponse
from .models import Alarm


def index(request):
    alarms = Alarm.all()

    return HttpResponse("Lowlevel")
