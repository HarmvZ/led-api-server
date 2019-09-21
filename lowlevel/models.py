import locale
from uuid import uuid4
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from crontab import CronTab, CronSlices
from cron_descriptor import get_description


class CronJobModel(models.Model):
    command = models.CharField(max_length=255, default=settings.CRONTAB_DEFAULT_COMMAND)
    enabled = models.BooleanField(default=True)
    minute = models.CharField(max_length=255)
    hour = models.CharField(max_length=255)
    day = models.CharField(max_length=255, default="*")
    month = models.CharField(max_length=255, default="*")
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

        return super(CronJobModel, self).full_clean(*args, **kwargs)

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
            job = cron.new(command=self.command, comment=uuid)
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

    class Meta:
        abstract = True

class Alarm(CronJobModel):
    name = models.CharField(max_length=255, default="Naamloos alarm")

    # @property
    # def human_readable_time(self):
    #     # Explicitly set locale
    #     locale.setlocale(locale.LC_ALL, settings.CRONTAB_TIME_LOCALE)
    #     return get_description(
    #         "{} {} {} {} {}".format(
    #             self.minute, self.hour, self.day, self.month, self.day_of_week
    #         )
    #     )
