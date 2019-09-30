import time
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

DEFAULT_COLOR = "255,255,255"
DEFAULT_WAIT_MS = 50

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

    # Define functions which animate LEDs in various ways.
    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)


    def theaterChase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, color)
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    @staticmethod
    def wheel(pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)


    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)


    def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel(
                    (int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)


    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

if __name__ == "__main__":
    lc = LedControl()
    animationFuncs = {
        "colorWipe": lc.colorWipe,
        "theaterChase": lc.theaterChase,
        "rainbow": lc.rainbow,
        "rainbowCycle": lc.rainbowCycle,
        "theaterChaseRainbow": lc.theaterChaseRainbow,
    }
    # Process arguments
    parser = argparse.ArgumentParser(
        description="Display animations"
    )
    fn_list_text = ", ".join(list(animationFuncs.keys()))
    parser.add_argument(
        "animation",
        help="Choose animation ({})".format(fn_list_text),
    )
    parser.add_argument(
        "-wm",
        "--wait_ms",
        help='Milliseconds to wait in between frames (default: {})'.format(DEFAULT_WAIT_MS),
    )
    parser.add_argument(
        "-c",
        "--color",
        help='Color for method (default: {})'.format(DEFAULT_COLOR),
    )

    args = parser.parse_args()
    wait_ms = int(args.wait_ms) or 50
    c = args.color or DEFAULT_COLOR
    c = ",".split(c)
    color = Color(int(c[0]), int(c[1]), int(c[2]))

    #TODO handle different arguments for different methods
    #TODO implement in app
    animationFuncs[args.animation]()
