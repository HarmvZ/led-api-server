from django.db import models
from django.core.exceptions import ValidationError
from crontab import CronTab, CronSlices


class Alarm(models.Model):
    name = models.CharField(max_length=255, default="Naamloos alarm")
    enabled = models.BooleanField(default=True)
    minute = models.CharField(max_length=255)
    hour = models.CharField(max_length=255)
    day = models.CharField(max_length=255)
    month = models.CharField(max_length=255)
    day_of_week = models.CharField(max_length=255)

    def full_clean(self, *args, **kwargs):
        if CronSlices.is_valid(
            "{} {} {} {} {}".format(
                self.minute,
                self.hour,
                self.day,
                self.month,
                self.day_of_week
            )
        ):
            pass
        else:
            print("cronjob invalid full_clean")
            raise ValidationError("Time values are not valid for a cronjob")

        return super(Alarm, self).full_clean(*args, **kwargs)

    def get_related_cronjob(self):
        cron = CronTab(user=True)
        job = cron.find_comment(self.pk)
        return job

