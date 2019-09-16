from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from api.serializers import ColorSerializer

# Create your views here.
@csrf_exempt
def base_view(request):
    return JsonResponse({"Bla":"bla"},status=200)

@api_view(["POST"])
def set_color(request):
    success = False
    serializer = ColorSerializer(data=request.data)
    if (serializer.is_valid()):
        # TODO set color
        print("sets color")
        success = True
    status = 200 if success else 400
    return JsonResponse({ "success": success }, status=status)

@api_view(["POST"])
def transition_color(request):
    success = False
    serializer = ColorSerializer(data=request.data)
    if (serializer.is_valid()):
        # TODO transition color
        print("transition color")
        success = True
    status = 200 if success else 400
    return JsonResponse({ "success": success }, status=status)
    