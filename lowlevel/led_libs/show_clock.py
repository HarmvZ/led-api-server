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
import argparse

BACKGROUND_COLOR = "0,0,1"
FOREGROUND_COLOR = "255,0,0"


class LedControl:
    def __init__(self, bg, fg):
        self.bg = bg
        self.fg = fg
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




if __name__ == "__main__":
    # Process arguments
    parser = argparse.ArgumentParser(
        description="Show a digital clock on the led matrix"
    )
    parser.add_argument(
        "-bg",
        "--backgroundcolor",
        action="store",
        help='set the background color, format "r,g,b"',
    )
    parser.add_argument(
        "-fg",
        "--foregroundcolor",
        action="store",
        help='set the foreground color, format "r,g,b"',
    )
    args = parser.parse_args()
    bg = args.backgroundcolor or BACKGROUND_COLOR
    fg = args.foregroundcolor or FOREGROUND_COLOR
    bg = bg.split(",")
    fg = fg.split(",")
    bg = Color(int(bg[0]), int(bg[1]), int(bg[2]))
    fg = Color(int(fg[0]), int(fg[1]), int(fg[2]))

    lc = LedControl(bg, fg)
    while True:
        lc.set_time()
        time.sleep(.9)
