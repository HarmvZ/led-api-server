from rest_framework import serializers

from alarms.models import Alarm
from django.conf import settings

class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = [
            'pk', 
            'enabled', 
            'minute', 
            'hour', 
            'day_of_week',
            'name'
        ]

class ColorSerializer(serializers.Serializer):
    r = serializers.IntegerField(min_value=0, max_value=255)
    g = serializers.IntegerField(min_value=0, max_value=255)
    b = serializers.IntegerField(min_value=0, max_value=255)
    rgb = serializers.SerializerMethodField()
    
    def get_rgb(self, obj):
        """
        Returns a tuple of (r, g, b) color values.
        """
        r = obj.get('r', 0)
        g = obj.get('g', 0)
        b = obj.get('b', 0)
        return (r, g, b)

class TransitionColorSerializer(ColorSerializer):
    steps = serializers.IntegerField(min_value=1, required=False, default=100)
    timestep = serializers.IntegerField(min_value=1, required=False, default=20)


class ClockSerializer(serializers.Serializer):
    fg = ColorSerializer(required=False, default=settings.CLOCK_FOREGROUND_COLOR)
    bg = ColorSerializer(required=False, default=settings.CLOCK_BACKGROUND_COLOR)

class AnimationSerializer(serializers.Serializer):
    animation = serializers.ChoiceField(
        choices=["rainbow", "rainbowCycle", "theaterChaseRainbow"]
    )
    wait_ms = serializers.IntegerField(min_value=1, required=False, default=20)
