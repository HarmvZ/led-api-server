from rpi_ws281x import Color

def fill_colors(strip, color_matrix):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        color = Color(
            int(color_matrix[i][0]),
            int(color_matrix[i][1]),
            int(color_matrix[i][2]),
        )
        strip.setPixelColor(i, color)
    strip.show()

def color_wipe(strip, color):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

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
