import threading
from django.views import generic, View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Alarm
from .led_libs.led_control import LedControl


class IndexView(generic.ListView):
    template_name = "lowlevel/index.html"
    model = Alarm
    context_object_name = "alarms"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["colors"] = [
            "0,0,0",
            "5,0,0",
            "0,5,0",
            "0,0,5",
            "255,0,0",
            "0,255,0",
            "0,0,255",
            "0,255,255",
            "255,0,255",
            "255,255,0",
            "255,255,255",
        ]
        return context


@method_decorator(csrf_exempt, name="dispatch")
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


class TransitionColorView(View):
    led_control = LedControl()

    def get(self, request):
        r = request.GET["r"]
        g = request.GET["g"]
        b = request.GET["b"]
        steps = request.GET.get("steps", 100)
        timestep = request.GET.get("timestep", 50)
        self.led_control.transition_to_color(
            int(r), int(g), int(b), steps=int(steps), timestep=int(timestep)
        )
        return HttpResponse("New color transitioned: ({}, {}, {}).".format(r, g, b))
