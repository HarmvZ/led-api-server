import time
import datetime
import numpy as np
import argparse
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
        final_color = np.array([128, 128, 128])
        start_color = np.array([0, 0, 0])
        color_delta = final_color - start_color
        for i in range(steps):
            # create linear i in range 0 to 100
            lin_range = i / (steps - 1) * 100
            # create exponential range from 1 to exp(100)
            log_range = np.exp(lin_range)
            # create exponential range from 0 to 1
            log_range = (log_range - 1) / (np.exp(100) - 1)
            color = start_color + color_delta * lin_range / 100  # log_range
            self.color_wipe(Color(int(color[0]), int(color[1]), int(color[2])))
            time.sleep(timestep / 1000)


if __name__ == "__main__":
    # Process arguments
    parser = argparse.ArgumentParser(
        description="Display wake up light and read spoken info"
    )
    parser.add_argument(
        "-s",
        "--steps",
        action="store",
        help="Set the number of steps to be taken in wake up transition (default: 18000)",
    )
    parser.add_argument(
        "-t",
        "--timestep",
        action="store",
        help="Set the number of ms one timestep is (default: 100)",
    )
    args = parser.parse_args()
    steps = args.steps or 18000
    timestep = args.timestep or 100

    lc = LedControl()
    lc.transition_to_white(steps=int(steps), timestep=int(timestep))
    ws = WakeUpStory()
    ws.play()
