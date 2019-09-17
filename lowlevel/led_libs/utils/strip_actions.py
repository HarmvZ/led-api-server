import time
import datetime
import numpy as np
from rpi_ws281x import Color
from lowlevel.led_libs.settings import (
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
from lowlevel.led_libs.utils.bit24_to_3_bit8 import bit24_to_3_bit8
from lowlevel.led_libs.utils.stoppable_thread import StoppableThread
from lowlevel.led_libs.utils.core_actions import fill_colors, color_wipe
from lowlevel.led_libs.threads.ClockThread import ClockThread
from lowlevel.led_libs.threads.TransitionThread import TransitionThread

CLOCK_BACKGROUND_COLOR = "0,0,1"
CLOCK_FOREGROUND_COLOR = "255,0,0"

class StripActions:
    def wipe_clear(self, strip):
        color_wipe(strip, Color(0, 0, 0))

    def fill(self, strip, r, g, b):
        color_wipe(strip, Color(r, g, b))

    def transition_to_color(self, strip, r, g, b, steps=100, timestep=20):
        """
        Transition all leds to a color
        :param r: red value 8-bit int
        :param g: green value 8-bit int
        :param b: blue value 8-bit int
        :param steps: number of steps in transition
        :param timestep: time that one step takes in ms
        """
        transition = TransitionThread(
            strip,
            kwargs={
                r,
                g,
                b,
                steps,
                timestep
            }
                    )
        transition.start()
        return transition


    def show_time(self, strip, fg, bg):
        fg_color = Color(fg["r"], fg["g"], fg["b"])
        bg_color = Color(bg["r"], bg["g"], bg["b"])

        clock = ClockThread(strip, kwargs={
            "fg_color": fg_color,
            "bg_color": bg_color
        })
        clock.start()
        return clock

