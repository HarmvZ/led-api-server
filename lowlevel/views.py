import threading
from django.views import generic, View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Alarm
from .led_libs import clock


class IndexView(generic.ListView):
    template_name = 'lowlevel/index.html'
    context_object_name = 'alarms'

    def get_queryset(self):
        """Return all alarms."""
        return Alarm.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class ClockView(View):
    def post(self, request, *args, **kwargs):
        # show clock on leds, run never ending function in thread
        clock_thread = threading.Thread(target=clock.start_clock())
        clock_thread.start()
