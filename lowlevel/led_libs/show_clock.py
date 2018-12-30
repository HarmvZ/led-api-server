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

BACKGROUND_COLOR = "0,0,30"
FOREGROUND_COLOR = "255,255,0"


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
                    self.strip.setPixelColor(pixel_id, self.fg)
                else:
                    self.strip.setPixelColor(pixel_id, self.bg)
        self.strip.show()

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

    def set_time(self):
        """Set time to current time on led pixels"""
        matrix = self.create_binary_time_matrix()
        self.write_matrix_to_strip(matrix)


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
