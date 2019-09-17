import numpy as np
import time
from lowlevel.led_libs.utils.stoppable_thread import StoppableThread
from lowlevel.led_libs.utils.bit24_to_3_bit8 import bit24_to_3_bit8
from lowlevel.led_libs.utils.core_actions import fill_colors

class TransitionThread(StoppableThread):
    def run(self):
        r = self.kwargs["r"]
        g = self.kwargs["g"]
        b = self.kwargs["b"]
        steps = self.kwargs["steps"]
        timestep = self.kwargs["timestep"]
        num_leds = self.strip.numPixels()
        # get current colors and calculate difference with new color
        current_colors = np.zeros((num_leds, 3))
        color_deltas = np.zeros((num_leds, 3))
        for i in range(num_leds):
            current_colors[i] = bit24_to_3_bit8(self.strip.getPixelColor(i))
            color_deltas[i] = current_colors[i] - np.array([r, g, b])
            if self.stopped():
                return

        for i in range(steps):
            new_colors = (current_colors - color_deltas / (steps - 1) * i).astype(
                int
            )
            fill_colors(self.strip, new_colors)
            time.sleep(timestep / 1000)
            if self.stopped():
                return