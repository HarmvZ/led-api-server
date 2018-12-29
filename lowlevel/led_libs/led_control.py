import time
import numpy as np
from rpi_ws281x import Adafruit_NeoPixel, Color
from subprocess import Popen
from . import settings
from pathlib import Path


def bit24_to_3_bit8(val):
    """
    Convert 24-bit value to a 3 component 8 bit value
    :param val: 24-bit value
    :return: list of 3 8-bit int components
    """
    # Get binary value without 0b prefix
    bin_val = bin(val)[2:]
    # Get binary value padded with zeros
    bin_val = "0" * (24 - len(bin_val)) + bin_val
    # Extract components as int
    red = int(bin_val[:8], 2)
    green = int(bin_val[8:16], 2)
    blue = int(bin_val[16:24], 2)
    return red, green, blue


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

            self.process = None

        def color_wipe(self, color):
            """Wipe color across display a pixel at a time."""
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, color)
            self.strip.show()

        def wipe_clear(self):
            self.color_wipe(Color(0, 0, 0))

        def fill(self, r, g, b):
            self.color_wipe(Color(r, g, b))

        def fill_colors(self, color_matrix):
            """Wipe color across display a pixel at a time."""
            for i in range(self.strip.numPixels()):
                color = Color(
                    int(color_matrix[i][0]),
                    int(color_matrix[i][1]),
                    int(color_matrix[i][2]),
                )
                self.strip.setPixelColor(i, color)
            self.strip.show()

        def transition_to_color(self, r, g, b, steps=100, timestep=20):
            """
            Transition all leds to a color
            :param r: red value 8-bit int
            :param g: green value 8-bit int
            :param b: blue value 8-bit int
            :param steps: number of steps in transition
            :param timestep: time that one step takes in ms
            """
            num_leds = self.strip.numPixels()
            # get current colors and calculate difference with new color
            current_colors = np.zeros((num_leds, 3))
            color_deltas = np.zeros((num_leds, 3))
            for i in range(num_leds):
                current_colors[i] = bit24_to_3_bit8(self.strip.getPixelColor(i))
                color_deltas[i] = current_colors[i] - np.array([r, g, b])

            for i in range(steps):
                new_colors = (current_colors - color_deltas / (steps - 1) * i).astype(
                    int
                )
                self.fill_colors(new_colors)
                time.sleep(timestep / 1000)

        def start_clock(self, bg=None, fg=None):
            cwd = str(Path("").resolve())
            self.process = Popen(
                "exec sudo python3 lowlevel/led_libs/show_clock.py",
                stderr=None,
                stdin=None,
                stdout=None,
                shell=True,
                cwd=cwd,
            )

        def stop_clock(self):
            if self.process is not None:
                self.process.kill()

    instance = None

    def __init__(self):
        if not LedControl.instance:
            LedControl.instance = LedControl.__LedControl()

    def __getattr__(self, name):
        return getattr(self.instance, name)
