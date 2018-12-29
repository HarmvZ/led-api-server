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
            "5,5,0",
            "0,5,0",
            "0,5,5",
            "0,0,5",
            "5,0,5",
            "5,5,5",
            "50,0,0",
            "50,50,0",
            "0,50,50",
            "0,50,0",
            "0,0,50",
            "50,0,50",
            "50,50,50",
            "128,0,0",
            "128,128,0",
            "0,128,128",
            "0,128,0",
            "0,0,128",
            "128,0,128",
            "128,128,128",
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
            self.led_control.stop_clock()

        return HttpResponse(action)


@method_decorator(csrf_exempt, name="dispatch")
class ColorView(View):
    led_control = LedControl()

    def post(self, request):
        r = request.POST["r"]
        g = request.POST["g"]
        b = request.POST["b"]
        self.led_control.fill(int(r), int(g), int(b))
        return HttpResponse("New color set: ({}, {}, {}).".format(r, g, b))


@method_decorator(csrf_exempt, name="dispatch")
class TransitionColorView(View):
    led_control = LedControl()

    def post(self, request):
        r = request.POST["r"]
        g = request.POST["g"]
        b = request.POST["b"]
        steps = request.POST.get("steps", 100)
        timestep = request.POST.get("timestep", 50)
        self.led_control.transition_to_color(
            int(r), int(g), int(b), steps=int(steps), timestep=int(timestep)
        )
        return HttpResponse("New color transitioned: ({}, {}, {}).".format(r, g, b))
