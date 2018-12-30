from uuid import uuid4
from django.db import models
from django.core.exceptions import ValidationError
from crontab import CronTab, CronSlices
from leds.settings import ALARM_CRONTAB_COMMAND


class Alarm(models.Model):
    name = models.CharField(max_length=255, default="Naamloos alarm")
    enabled = models.BooleanField(default=True)
    minute = models.CharField(max_length=255)
    hour = models.CharField(max_length=255)
    day = models.CharField(max_length=255)
    month = models.CharField(max_length=255)
    day_of_week = models.CharField(max_length=255)
    cronjob = models.CharField(max_length=36)

    def full_clean(self, *args, **kwargs):
        """
        Check if valid and save cronjob
        """
        if CronSlices.is_valid(
            "{} {} {} {} {}".format(
                self.minute,
                self.hour,
                self.day,
                self.month,
                self.day_of_week
            )
        ):
            print("cronslices is valid")
            # Save cronjob and set uuid4
            self.cronjob = self.save_related_cronjob()
        else:
            print("cronjob invalid full_clean")
            raise ValidationError("Time values are not valid for a cronjob")

        return super(Alarm, self).full_clean(*args, **kwargs)

    def get_related_cronjob(self):
        cron = CronTab(user=True)
        job = cron.find_comment(self.cronjob)
        return job

    def save_related_cronjob(self):
        cron = CronTab(user=True)
        if self.pk is None:
            # New Alarm
            uuid = str(uuid4())
            job = cron.new(command=ALARM_CRONTAB_COMMAND, comment=uuid)
        else:
            # Existing alarm
            job = self.get_related_cronjob()
            uuid = self.cronjob

        # Set times
        job.setall(self.minute, self.hour, self.day, self.month, self.day_of_week)

        # Set enabled
        job.enable(self.enabled)

        if job.is_valid():
            print("cronjob valid, writing...")
            cron.write()
            return uuid
        else:
            # Delete instance?
            print("invalid cronjob")
            raise ValidationError("Cronjob is not valid")

