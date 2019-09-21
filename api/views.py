from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from api.serializers import ColorSerializer, TransitionColorSerializer, ClockSerializer, AnimationSerializer
from lowlevel.led_libs.led_control import LedControl

# Create your views here.
@csrf_exempt
def base_view(request):
    return JsonResponse({"Bla":"bla"},status=200)

@api_view(["GET"])
def get_pixels(request):
    lc = LedControl()
    pixels = lc.strip_action("get_pixels")
    return JsonResponse({"pixels": pixels}, status=200)


def abstract_view(request, fn_name, Serializer, kwarg_keys=[]):
    success = False
    serializer = Serializer(data=request.data)
    if serializer.is_valid():
        kwargs = {}
        for kwarg_key in kwarg_keys:
            kwargs.update({
                kwarg_key: serializer.data[kwarg_key]
            })
        lc = LedControl()
        lc.strip_action(fn_name, **kwargs)
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
