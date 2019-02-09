from subprocess import Popen, PIPE
from django.urls import reverse_lazy
from django.views import generic, View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Alarm
from .led_libs.led_control import LedControl
from .led_libs.wake_up_story import WakeUpStory
from leds.settings import ALARM_CRONTAB_COMMAND, CLOCK_STOP_COMMAND, STORY_STOP_COMMAND


class IndexView(generic.ListView):
    template_name = "lowlevel/index.html"
    model = Alarm
    context_object_name = "alarms"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add colors for buttons
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


class AlarmDetailView(generic.DetailView):
    model = Alarm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["crontime"] = " ".join(
            [
                self.object.minute,
                self.object.hour,
                self.object.day,
                self.object.month,
                self.object.day_of_week,
            ]
        )
        return context


class AlarmCreateView(generic.edit.CreateView):
    model = Alarm
    fields = ["name", "enabled", "minute", "hour", "day", "month", "day_of_week"]

    def get_success_url(self):
        return reverse_lazy("alarm-detail", args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(AlarmCreateView, self).get_context_data(**kwargs)
        context["time_val"] = ""
        context["dow_dict"] = [
            (0, "Sunday", False),
            (1, "Monday", False),
            (2, "Tuesday", False),
            (3, "Wednesday", False),
            (4, "Thursday", False),
            (5, "Friday", False),
            (6, "Saturday", False)
        ]
        return context


class AlarmUpdateView(generic.edit.UpdateView):
    model = Alarm
    fields = ["name", "enabled", "minute", "hour", "day", "month", "day_of_week"]

    def get_success_url(self):
        return reverse_lazy("alarm-detail", args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(AlarmUpdateView, self).get_context_data(**kwargs)
        context["time_val"] = "{}:{}".format(self.object.hour, self.object.minute)
        context["dow_dict"] = [
            (0, "Sunday", True if "0" in self.object.day_of_week else False),
            (1, "Monday", True if "1" in self.object.day_of_week else False),
            (2, "Tuesday", True if "2" in self.object.day_of_week else False),
            (3, "Wednesday", True if "3" in self.object.day_of_week else False),
            (4, "Thursday", True if "4" in self.object.day_of_week else False),
            (5, "Friday", True if "5" in self.object.day_of_week else False),
            (6, "Saturday", True if "6" in self.object.day_of_week else False)
        ]
        return context

class AlarmDeleteView(generic.edit.DeleteView):
    model = Alarm
    success_url = reverse_lazy("index")


class AlarmToggleView(generic.View):
    def get(self, request, pk):
        alarm = get_object_or_404(Alarm, pk=pk)
        alarm.enabled = not alarm.enabled
        alarm.save()
        return redirect("index")


@method_decorator(csrf_exempt, name="dispatch")
class ClockView(View):
    led_control = LedControl()

    def post(self, request, *args, **kwargs):
        action = request.POST["action"]
        if action == "start":
            self.led_control.start_clock()
        if action == "stop":
            self.led_control.stop_clock()

        return HttpResponse(action + " clock")


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


@method_decorator(csrf_exempt, name="dispatch")
class WakeUpLightView(View):
    def post(self, request, *args, **kwargs):
        action = request.POST["action"]
        if action == "start":
            # Execute wake up light scripts
            Popen(
                ALARM_CRONTAB_COMMAND + " --steps=30",
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE,
                shell=True,
            )
        if action == "stop":
            # Kill all start_alarm.py scripts
            Popen(CLOCK_STOP_COMMAND, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)

        return HttpResponse(action + " alarm")


@method_decorator(csrf_exempt, name="dispatch")
class WakeUpStoryView(View):
    def post(self, request, *args, **kwargs):
        action = request.POST["action"]
        if action == "start":
            # Execute wake up Story scripts
            ws = WakeUpStory()
            ws.play()
        if action == "stop":
            # Kill all start_alarm.py scripts
            Popen(STORY_STOP_COMMAND, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)

        return HttpResponse(action + " story")
