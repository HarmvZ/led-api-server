from rest_framework import serializers

class ColorSerializer(serializers.Serializer):
    r = serializers.IntegerField(min_value=0, max_value=255)
    g = serializers.IntegerField(min_value=0, max_value=255)
    b = serializers.IntegerField(min_value=0, max_value=255)