import time
from lowlevel.led_libs.utils.stoppable_thread import StoppableThread
from lowlevel.led_libs.utils.core_actions import wheel

class AnimationThread(StoppableThread):
    def __init__(self, strip, animation, wait_ms):
        super().__init__(strip)
        self.animation = animation
        self.wait_ms = wait_ms

    def run(self):
        args = (self.strip, self.wait_ms)
        fn = {
            "rainbow": self.rainbow,
            "rainbowCycle": self.rainbowCycle,
            "theaterChaseRainbow": self.theaterChaseRainbow
        }
        j = 0
        while not self.stopped():
            fn[self.animation](j, *args)
            j += 1


    def rainbow(self, j, strip, wait_ms):
        """Draw rainbow that fades across all pixels at once."""
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


    def rainbowCycle(self, j, strip, wait_ms):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


    def theaterChaseRainbow(self, j, strip, wait_ms):
        """Rainbow movie theater light style chaser animation."""
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)
