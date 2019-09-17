import time
import numpy as np
from rpi_ws281x import Adafruit_NeoPixel, Color
from subprocess import Popen
from . import settings
from pathlib import Path
from leds.settings import CLOCK_START_COMMAND
from lowlevel.led_libs.utils.stoppable_thread import StoppableThread
from lowlevel.led_libs.utils.strip_actions import StripActions

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
                issubclass(type(self.thread), StoppableThread) 
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
