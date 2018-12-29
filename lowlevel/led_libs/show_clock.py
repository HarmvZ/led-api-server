import time
import datetime
import numpy as np
from rpi_ws281x import Adafruit_NeoPixel, Color
from . import settings
import argparse

BACKGROUND_COLOR = "0,0,30"
FOREGROUND_COLOR = "255,255,0"


class LedControl:
    def __init__(self, bg, fg):
        self.bg = bg
        self.fg = fg
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

    def write_matrix_to_strip(self, matrix):
        height, width = matrix.shape
        for h in range(height):
            for w in range(width):
                even = h % 2 == 0
                if even:
                    pixel_id = h * settings.MATRIX_WIDTH + w
                else:
                    pixel_id = (h + 1) * settings.MATRIX_WIDTH - w - 1
                if matrix[h, w] == 1:
                    self.strip.setPixelColor(pixel_id, self.fg)
                else:
                    self.strip.setPixelColor(pixel_id, self.bg)
        self.strip.show()

    @staticmethod
    def create_binary_time_matrix():
        now = datetime.datetime.now()
        characters = now.strftime("%H%M%S")
        matrix = np.zeros((settings.MATRIX_HEIGHT, settings.MATRIX_WIDTH))
        indices = ((2, 4), (6, 8), (12, 14), (16, 18), (22, 24), (26, 28))
        for h in range(2, 7):
            for w in range(settings.MATRIX_WIDTH):
                for i, (start, end) in enumerate(reversed(indices)):
                    if start <= w <= end:
                        # Place character
                        current_char = characters[i]
                        current_char_matrix = settings.NUMBERS[int(current_char)]
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
        action="store_const",
        help='set the background color, format "r,g,b"',
    )
    parser.add_argument(
        "-fg",
        "--foregroundcolor",
        action="store_const",
        help='set the foreground color, format "r,g,b"',
    )
    args = parser.parse_args()
    bg = args.backgroundcolor or BACKGROUND_COLOR
    fg = args.foregroundcolor or FOREGROUND_COLOR
    bg = bg.split(",")
    fg = fg.split(",")
    bg = Color(bg[0], bg[1], bg[2])
    fg = Color(fg[0], fg[1], fg[2])

    print("showing clock")
    lc = LedControl(bg, fg)
    while True:
        lc.set_time()
        time.sleep(.9)
