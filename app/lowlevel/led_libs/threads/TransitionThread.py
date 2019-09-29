import numpy as np
import time
from lowlevel.led_libs.utils.stoppable_thread import StoppableThread
from lowlevel.led_libs.utils.bit24_to_3_bit8 import bit24_to_3_bit8
from lowlevel.led_libs.utils.core_actions import fill_colors

class TransitionThread(StoppableThread):
    def __init__(self, strip, **kwargs):
        super().__init__(strip)
        self.r = kwargs["r"]
        self.g = kwargs["g"]
        self.b = kwargs["b"]
        self.steps = kwargs["steps"]
        self.timestep = kwargs["timestep"]

    def run(self):
        num_leds = self.strip.numPixels()
        # get current colors and calculate difference with new color
        current_colors = np.zeros((num_leds, 3))
        color_deltas = np.zeros((num_leds, 3))
        for i in range(num_leds):
            current_colors[i] = bit24_to_3_bit8(self.strip.getPixelColor(i))
            color_deltas[i] = current_colors[i] - np.array([self.r, self.g, self.b])
            if self.stopped():
                return

        for i in range(self.steps):
            new_colors = (current_colors - color_deltas / (self.steps - 1) * i).astype(
                int
            )
            fill_colors(self.strip, new_colors)
            time.sleep(self.timestep / 1000)
            if self.stopped():
                return