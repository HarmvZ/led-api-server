from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from api.serializers import ColorSerializer
from lowlevel.led_libs.led_control import LedControl

# Create your views here.
@csrf_exempt
def base_view(request):
    return JsonResponse({"Bla":"bla"},status=200)

@api_view(["POST"])
def set_color(request):
    success = False
    serializer = ColorSerializer(data=request.data)
    if (serializer.is_valid()):
        lc = LedControl()
        lc.strip_action("fill", serializer.r, serializer.g, serializer.b)
        success = True
    status = 200 if success else 400
    return JsonResponse({ "success": success }, status=status)

@api_view(["POST"])
def transition_color(request):
    success = False
    serializer = ColorSerializer(data=request.data)
    if (serializer.is_valid()):
        lc = LedControl()
        lc.strip_action("transition_to_color", serializer.r, serializer.g, serializer.b)        
        success = True
    status = 200 if success else 400
    return JsonResponse({ "success": success }, status=status)
    