from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action

from lowlevel.models import Alarm
from api.serializers import ColorSerializer, TransitionColorSerializer, ClockSerializer, AnimationSerializer, AlarmSerializer
from lowlevel.led_libs.led_control import LedControl
from lowlevel.led_libs.utils.bit24_to_3_bit8 import bit24_to_3_bit8
from api.zmq_client import ZMQClient

# Create your views here.
@csrf_exempt
def status_view(request):
    return HttpResponse("" ,status=200)


class AlarmViewSet(viewsets.ModelViewSet):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer

    @action(detail=False, methods=['get'])
    def first_upcoming_alarm(self, request):
        alarms = Alarm.objects.filter(enabled=True)
        if len(alarms) == 0:
            return Http404
        alarms = sorted(alarms, key=lambda m: m.first_upcoming_datetime)
        serializer = self.get_serializer(alarms[0])
        return JsonResponse(serializer.data)

@api_view(["GET"])
def get_pixels(request):
    zmqc = ZMQClient()
    pixels = zmqc.perform_request("get_pixels")
    pixels_rgb = [bit24_to_3_bit8(c) for c in pixels]
    return JsonResponse({"pixels": pixels_rgb}, status=200)


def abstract_view(request, fn_name, Serializer, kwarg_keys=[]):
    success = False
    serializer = Serializer(data=request.data)
    if serializer.is_valid():
        kwargs = {}
        for kwarg_key in kwarg_keys:
            kwargs.update({
                kwarg_key: serializer.data[kwarg_key]
            })
        zmqc = ZMQClient()
        zmqc.perform_request(fn_name, **kwargs)
        success = True
    status = 200 if success else 400
    return JsonResponse({ "success": success }, status=status)

@api_view(["POST"])
def set_color(request):
    return abstract_view(
        request, 
        "fill", 
        ColorSerializer, 
        ["r", "g", "b"]
    )

@api_view(["POST"])
def transition_color(request):
    return abstract_view(
        request, 
        "transition_to_color", 
        TransitionColorSerializer, 
        ["r", "g", "b", "steps", "timestep"]
    )
    
@api_view(["POST"])
def show_clock(request):
    return abstract_view(
        request, 
        "show_time", 
        ClockSerializer, 
        ["fg", "bg"]
    )
    
@api_view(["POST"])
def show_animation(request):
    return abstract_view(
        request, 
        "animation", 
        AnimationSerializer, 
        ["animation", "wait_ms"]
    )
