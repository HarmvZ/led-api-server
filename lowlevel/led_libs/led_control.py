import time
import numpy as np
import inspect
from rpi_ws281x import Adafruit_NeoPixel, Color
from subprocess import Popen
from . import settings
from pathlib import Path
import psutil
from leds.settings import CLOCK_START_COMMAND
from lowlevel.led_libs.utils.stoppable_thread import StoppableThread
from lowlevel.led_libs.utils.strip_actions import StripActions

def kill(proc_pid):
    """
    Helper function that kills a subprocess
    https://stackoverflow.com/a/25134985
    :param proc_pid:
    :return:
    """
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

# Singleton class as defined in:
# https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
class LedControl:
    class __LedControl:
        def __init__(self):
            # Create NeoPixel object with appropriate configuration.
            self.strip = Adafruit_NeoPixel(
                settings.LED_COUNT,
                settings.LED_PIN,
                settings.LED_FREQ_HZ,
                settings.LED_DMA,
                settings.LED_INVERT,
                settings.LED_BRIGHTNESS,
                settings.LED_CHANNEL,
            )
            # Intialize the library (must be called once before other functions).
            self.strip.begin()

            self.thread = None
            self.strip_actions = StripActions()

        def strip_action(self, name, *args, **kwargs):
            if (
                inspect.isclass(self.thread) 
                and issubclass(self.thread, StoppableThread) 
                and self.thread.is_alive() 
                and not self.thread.stopped()
            ):
                self.thread.stop()
                self.thread.join()
            self.thread = getattr(self.strip_actions, name)(self.strip, *args, **kwargs)

    instance = None

    def __init__(self):
        if not LedControl.instance:
            LedControl.instance = LedControl.__LedControl()

    def __getattr__(self, name):
        return getattr(self.instance, name)
