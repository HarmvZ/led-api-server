import locale
from uuid import uuid4
from django.db import models
from django.core.exceptions import ValidationError
from crontab import CronTab, CronSlices
from leds.settings import ALARM_CRONTAB_COMMAND
from cron_descriptor import get_description


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
                self.minute, self.hour, self.day, self.month, self.day_of_week
            )
        ):
            # Save cronjob and set uuid4
            self.cronjob = self.save_related_cronjob()
        else:
            raise ValidationError("Time values are not valid for a cronjob")

        return super(Alarm, self).full_clean(*args, **kwargs)

    def delete(self, *args, **kwargs):
        job, cron = self.get_related_cronjob()
        cron.remove(job)
        cron.write()
        super().delete(*args, **kwargs)

    def get_related_cronjob(self):
        cron = CronTab(user=True)
        job = None
        jobs = cron.find_comment(self.cronjob)
        for _job in jobs:
            job = _job
        if job is None:
            raise ValueError("No cronjob existing for model")

        return job, cron

    def save_related_cronjob(self):
        if self.pk is None:
            cron = CronTab(user=True)
            # New Alarm
            uuid = str(uuid4())
            job = cron.new(command=ALARM_CRONTAB_COMMAND, comment=uuid)
        else:
            # Existing alarm
            job, cron = self.get_related_cronjob()
            uuid = self.cronjob

        # Set times
        job.setall(self.minute, self.hour, self.day, self.month, self.day_of_week)

        # Set enabled
        job.enable(self.enabled)

        if job.is_valid():
            cron.write()
            return uuid
        else:
            # Delete instance?
            raise ValidationError("Cronjob is not valid")

    @property
    def human_readable_time(self):
        # Explicitly set locale to NL
        locale.setlocale(locale.LC_ALL, 'nl_NL.utf-8')
        return get_description(
            "{} {} {} {} {}".format(
                self.minute, self.hour, self.day, self.month, self.day_of_week
            )
        )
