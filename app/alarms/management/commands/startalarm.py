from django.core.management.base import BaseCommand, CommandError
from api.zmq_client import ZMQClient


class Command(BaseCommand):
    help = "Triggers alarm scripts on zmq server"

    def handle(self, *args, **options):
        try:
            zmqc = ZMQClient()
            zmqc.perform_request("start_alarm")
        except Exception as e:
            raise CommandError(str(e))

        self.stdout.write(self.style.SUCCESS("Successfully started"))

