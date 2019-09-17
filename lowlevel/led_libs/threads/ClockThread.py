import time
import datetime
import numpy as np
from lowlevel.led_libs.utils.stoppable_thread import StoppableThread
from lowlevel.led_libs.settings import (
    MATRIX_HEIGHT,
    MATRIX_WIDTH,
    NUMBERS,
)

class ClockThread(StoppableThread):
    def __init__(self, strip, **kwargs):
        super().__init__(strip)
        self.fg_color = kwargs["fg_color"]
        self.bg_color = kwargs["bg_color"]

    def run(self):
        while not self.stopped():
            matrix = self.create_binary_time_matrix()
            self.write_matrix_to_strip(self.strip, matrix, self.fg_color, self.bg_color)
            time.sleep(.9)

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