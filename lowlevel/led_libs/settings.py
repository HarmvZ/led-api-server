# Core LED strip settings
#########################
LED_COUNT = 300  # Number of LED pixels.
# LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN = 10  # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Clock settings
#########################
# Dictionary of numbers in 3x5 mirrored format
NUMBERS = {
    0: [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
    1: [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
    2: [[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
    3: [[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
    4: [[1, 0, 1], [1, 0, 1], [1, 1, 1], [1, 0, 0], [1, 0, 0]],
    5: [[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
    6: [[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
    7: [[1, 1, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]],
    8: [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
    9: [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
}
MATRIX_WIDTH = 30
MATRIX_HEIGHT = 10


# Spoken information settings
#########################
