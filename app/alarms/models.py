import locale
from uuid import uuid4
from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from crontab import CronTab, CronSlices
from croniter import croniter


class CronJobModel(models.Model):
    command = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    minute = models.CharField(max_length=255)
    hour = models.CharField(max_length=255)
    day = models.CharField(max_length=255, default="*")
    month = models.CharField(max_length=255, default="*")
    day_of_week = models.CharField(max_length=255)
    cronjob = models.CharField(max_length=36)

    @property
    def cron_time(self):
        """
        Returns cronjob time string
        """
        cron_components = (
            self.minute,
            self.hour,
            self.day,
            self.month,
            self.day_of_week,
        )
        return " ".join(cron_components)

    def save(self, *args, **kwargs):
        """
        Validates and saves the cronjob before saving the model
        """
        self.validate_cronjob_times()
        job, cron = self.get_related_cronjob()
        job = self.set_cronjob_values(job)
        self.validate_cronjob(job)
        cron.write()
        super().save(*args, **kwargs)

    def validate_cronjob_times(self):
        if not CronSlices.is_valid(self.cron_time):
            raise ValidationError("Time values are not valid for a cronjob.")

    def validate_cronjob(self, job):
        if not job.is_valid():
            raise ValidationError("Cronjob is invalid.")

    def get_related_cronjob(self):
        """
        Gets the cronjob that belongs to this model.
        Creates a new empty job if the model is new.
        """
        if self.pk is None:
            cron = CronTab(user=True)
            self.cronjob = str(uuid4())
            job = cron.new(command=self.command, comment=self.cronjob)
        else:
            cron = CronTab(user=True)
            job = None
            jobs = cron.find_comment(self.cronjob)
            for _job in jobs:
                job = _job
            if job is None:
                raise ValueError("Cronjob for this model does not exist.")
        return job, cron

    def set_cronjob_values(self, job):
        job.setall(self.minute, self.hour, self.day, self.month, self.day_of_week)
        job.enable(self.enabled)
        return job

    def delete(self, *args, **kwargs):
        job, cron = self.get_related_cronjob()
        cron.remove(job)
        cron.write()
        super().delete(*args, **kwargs)

    class Meta:
        abstract = True


class Alarm(CronJobModel):
    name = models.CharField(max_length=255, default="Naamloos alarm")

    def save(self, *args, **kwargs):
        """
        Sets correct command for cronjob on save
        """
        self.command = settings.ALARM_COMMAND
        super().save(*args, **kwargs)

    @property
    def first_upcoming_datetime(self):
        croni = croniter(self.cron_time)
        return croni.get_next(datetime)

