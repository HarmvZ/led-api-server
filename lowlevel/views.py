import threading
from django.views import generic, View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Alarm
from .led_libs.clock import LedControl


class IndexView(generic.ListView):
    template_name = 'lowlevel/index.html'
    context_object_name = 'alarms'

    def get_queryset(self):
        """Return all alarms."""
        return Alarm.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class ClockView(View):
    led_control = LedControl()

    def post(self, request, *args, **kwargs):
        action = request.POST["action"]
        if action == "start":
            self.led_control.start_clock()
        if action == "stop":
            self.led_control.stop()

        return HttpResponse(action)


class ColorView(View):
    led_control = LedControl()

    def get(self, request):
        r = request.GET["r"]
        g = request.GET["g"]
        b = request.GET["b"]
        self.led_control.fill(int(r), int(g), int(b))
        return HttpResponse("New color set: ({}, {}, {}).".format(r, g, b))


