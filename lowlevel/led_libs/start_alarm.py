import time
import datetime
import numpy as np
from rpi_ws281x import Adafruit_NeoPixel, Color
from settings import (
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
from wake_up_story import WakeUpStory

BACKGROUND_COLOR = "0,0,30"
FOREGROUND_COLOR = "255,255,0"


class LedControl:
    def __init__(self):
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(
            LED_COUNT,
            LED_PIN,
            LED_FREQ_HZ,
            LED_DMA,
            LED_INVERT,
            LED_BRIGHTNESS,
            LED_CHANNEL,
        )
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    def color_wipe(self, color):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def transition_to_white(self, steps=18000, timestep=100):
        """
        Transition all leds to white
        :param steps: number of steps in transition
        :param timestep: time that one step takes in ms
        """
        final_color = np.array([255, 255, 255])
        color_delta = final_color / (steps - 1)
        color = -color_delta
        for i in range(steps):
            color = color + color_delta
            self.color_wipe(Color(int(color[0]), int(color[1]), int(color[2])))
            time.sleep(timestep / 1000)


if __name__ == "__main__":
    lc = LedControl()
    lc.transition_to_white(steps=1800)  # TODO change to 30 min (18000)
    ws = WakeUpStory()
    ws.play()
