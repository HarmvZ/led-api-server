from django.db import models


class Alarm(models.Model):
    name = models.CharField(max_length=255, default="Naamloos alarm")
    activated = models.BooleanField(default=True)
    datetime = models.DateTimeField()
