import time
import datetime
import numpy as np
from rpi_ws281x import Color
from lowlevel.led_libs.settings import (
    LED_COUNT,
    LED_PIN,
    LED_FREQ_HZ,
    LED_DMA,
    LED_INVERT,
    LED_BRIGHTNESS,
    LED_CHANNEL,
    MATRIX_HEIGHT,
    MATRIX_WIDTH,
    NUMBERS,
)
from lowlevel.led_libs.utils.bit24_to_3_bit8 import bit24_to_3_bit8
from lowlevel.led_libs.utils.stoppable_thread import StoppableThread

CLOCK_BACKGROUND_COLOR = "0,0,1"
CLOCK_FOREGROUND_COLOR = "255,0,0"

class StripActions:
    @staticmethod
    def color_wipe(strip, color):
        """Wipe color across display a pixel at a time."""
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
        strip.show()

    def wipe_clear(self, strip):
        self.color_wipe(strip, Color(0, 0, 0))

    def fill(self, strip, r, g, b):
        self.color_wipe(strip, Color(r, g, b))

    @staticmethod
    def fill_colors(strip, color_matrix):
        """Wipe color across display a pixel at a time."""
        for i in range(strip.numPixels()):
            color = Color(
                int(color_matrix[i][0]),
                int(color_matrix[i][1]),
                int(color_matrix[i][2]),
            )
            strip.setPixelColor(i, color)
        strip.show()

    def transition_to_color(self, strip, r, g, b, steps=100, timestep=20):
        """
        Transition all leds to a color
        :param r: red value 8-bit int
        :param g: green value 8-bit int
        :param b: blue value 8-bit int
        :param steps: number of steps in transition
        :param timestep: time that one step takes in ms
        """
        this = self
        class TransitionThread(StoppableThread):
            def run(self):
                num_leds = strip.numPixels()
                # get current colors and calculate difference with new color
                current_colors = np.zeros((num_leds, 3))
                color_deltas = np.zeros((num_leds, 3))
                for i in range(num_leds):
                    current_colors[i] = bit24_to_3_bit8(strip.getPixelColor(i))
                    color_deltas[i] = current_colors[i] - np.array([r, g, b])
                    if self.stopped():
                        return

                for i in range(steps):
                    new_colors = (current_colors - color_deltas / (steps - 1) * i).astype(
                        int
                    )
                    this.fill_colors(strip, new_colors)
                    time.sleep(timestep / 1000)
                    if self.stopped():
                        return
        transition = TransitionThread()
        transition.start()
        return transition
            

    @staticmethod
    def write_matrix_to_strip(strip, matrix, fg, bg):
        height, width = matrix.shape
        for h in range(height):
            for w in range(width):
                even = h % 2 == 0
                if even:
                    pixel_id = h * MATRIX_WIDTH + w
                else:
                    pixel_id = (h + 1) * MATRIX_WIDTH - w - 1
                if matrix[h, w] == 1:
                    strip.setPixelColor(pixel_id, fg)
                else:
                    strip.setPixelColor(pixel_id, bg)
        strip.show()

    @staticmethod
    def create_binary_time_matrix():
        now = datetime.datetime.now()
        characters = now.strftime("%H%M%S")
        matrix = np.zeros((MATRIX_HEIGHT, MATRIX_WIDTH))
        indices = ((2, 4), (6, 8), (12, 14), (16, 18), (22, 24), (26, 28))
        for h in range(2, 7):
            for w in range(MATRIX_WIDTH):
                for i, (start, end) in enumerate(reversed(indices)):
                    if start <= w <= end:
                        # Place character
                        current_char = characters[i]
                        current_char_matrix = NUMBERS[int(current_char)]
                        matrix[h, w] = current_char_matrix[h - 2][w - start]
                    if (w == 10 or w == 20) and (h == 3 or h == 5):
                        # Place delimiter
                        # matrix[h, w] = 1
                        pass

        return matrix

    def show_time(self, strip, fg, bg):
        fg_color = Color(fg["r"], fg["g"], fg["b"])
        bg_color = Color(bg["r"], bg["g"], bg["b"])
        this = self
        class ClockThread(StoppableThread):
            def run(self):
                while not self.stopped():
                    matrix = this.create_binary_time_matrix()
                    this.write_matrix_to_strip(strip, matrix, fg_color, bg_color)
                    time.sleep(.9)
        clock = ClockThread()
        clock.start()
        return clock
