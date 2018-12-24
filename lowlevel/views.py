from django.shortcuts import render
from .models import Alarm


def index(request):
    alarms = Alarm.objects.all()
    context = {
        'alarms': alarms,
    }
    return render(request, 'lowlevel/index.html', context)
