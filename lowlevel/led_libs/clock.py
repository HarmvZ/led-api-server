import time
from multiprocessing import Process
import datetime
import numpy as np
from rpi_ws281x import *
import argparse

# Dictionary of numbers in 3x5 mirrored format
NUMBERS = {
    0: [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
    1: [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
    2: [[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
    3: [[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
    4: [[1, 0, 1], [1, 0, 1], [1, 1, 1], [1, 0, 0], [1, 0, 0]],
    5: [[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
    6: [[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
    7: [[1, 1, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]],
    8: [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
    9: [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
}
BACKGROUD_COLOR = Color(0, 0, 30)
FOREGROUND_COLOR = Color(255, 255, 0)
MATRIX_WIDTH = 30
MATRIX_HEIGHT = 10

# LED strip configuration:
LED_COUNT      = 300      # Number of LED pixels.
# LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Singleton class as defined in:
# https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
class LedControl:
    class __LedControl:
        def __init__(self):
            # Create NeoPixel object with appropriate configuration.
            self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
            # Intialize the library (must be called once before other functions).
            self.strip.begin()

            self.thread = None

        def color_wipe(self, color):
            """Wipe color across display a pixel at a time."""
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, color)
            self.strip.show()

        def wipe_clear(self):
            self.color_wipe(Color(0, 0, 0))

        def write_matrix_to_strip(self, matrix):
            height, width = matrix.shape
            for h in range(height):
                for w in range(width):
                    even = h % 2 == 0
                    if even:
                        pixel_id = h * MATRIX_WIDTH + w
                    else:
                        pixel_id = (h + 1) * MATRIX_WIDTH - w - 1
                    if matrix[h, w] == 1:
                        self.strip.setPixelColor(pixel_id, FOREGROUND_COLOR)
                    else:
                        self.strip.setPixelColor(pixel_id, BACKGROUD_COLOR)
            self.strip.show()

        @staticmethod
        def create_binary_time_matrix():
            now = datetime.datetime.now()
            characters = now.strftime("%H%M%S")
            matrix = np.zeros((MATRIX_HEIGHT, MATRIX_WIDTH))
            indices = ((2, 4), (6, 8), (12, 14), (16, 18), (22, 24), (26, 28))
            for h in range(2,7):
                for w in range(MATRIX_WIDTH):
                    for i, (start, end) in enumerate(reversed(indices)):
                        if start <= w <= end:
                            # Place character
                            current_char = characters[i]
                            current_char_matrix = NUMBERS[int(current_char)]
                            matrix[h, w] = current_char_matrix[h-2][w - start]
                        if (w == 10 or w == 20) and (h == 3 or h == 5):
                            # Place delimiter
                            #matrix[h, w] = 1
                            pass

            return matrix

        def set_time(self):
            """Set time to current time on led pixels"""
            matrix = self.create_binary_time_matrix()
            self.write_matrix_to_strip(matrix)

        def start_clock(self):
            # show clock on leds, run never ending function in thread
            self.thread = Process(target=self.run_clock())
            self.thread.daemon = True
            self.thread.start()

        def run_clock(self):
            try:
                while True:
                    self.set_time()
                    time.sleep(1)
            except Exception:
                self.wipe_clear()

        def stop(self):
            if self.thread.is_alive():
                self.thread.terminate()
                self.wipe_clear()

    instance = None

    def __init__(self):
        if not LedControl.instance:
            LedControl.instance = LedControl.__LedControl()

    def __getattr__(self, name):
        return getattr(self.instance, name)
