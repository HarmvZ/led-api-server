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