from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Alarm
from crontab import CronTab
from leds.settings import ALARM_CRONTAB_COMMAND

# Crontab form:
# minute hour day month day_of_week command #pk


@receiver(post_save, sender=Alarm)
def save_cronjob(sender, instance, created, raw, using, update_fields):
    cron = CronTab(user=True)
    if created:
        # New Alarm
        job = cron.new(command=ALARM_CRONTAB_COMMAND, comment=instance.pk)
    else:
        # Existing alarm
        job = instance.get_related_cronjob()

    # Set times
    job.setall(instance.minute, instance.hour, instance.day, instance.month, instance.day_of_week)

    # Set enabled
    job.enable(instance.enabled)

    if job.is_valid():
        cron.write()
    else:
        # Delete instance?
        print("invalid cronjob")
        raise ValueError("Cronjob is not valid")


@receiver(post_delete, sender=Alarm)
def delete_cronjob(sender, instance, using):
    cron = CronTab(user=True)
    job = instance.get_related_cronjob()
    cron.remove(job)
