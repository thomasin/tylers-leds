# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import random

from rpi_ws281x import PixelStrip, Color, ws
import RPi.GPIO as GPIO
import dht22

# LED strip configuration:
LED_COUNT      = 76      # Number of LED pixels.
LED1_PIN       = 12      # GPIO pin connected to the pixels (must support PWM!).
LED2_PIN       = 13      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED1_CHANNEL    = 0
LED2_CHANNEL    = 1
LED_STRIP      = ws.WS2812_STRIP

# Motion Sensor configuration:
MOTION_SENSOR_PIN = 17

# LED design configuration
BETWEEN_STRIP_CHANGES_SLOW = 250
BETWEEN_STRIP_CHANGES_FAST = 75
BETWEEN_LED_CHANGES_SLOW = 50
BETWEEN_LED_CHANGES_FAST = 25
BETWEEN_ITERATIONS = 750
BRIGHTNESS_DIM = 100

def color(r, g, b):
    """Create color from decimal values"""
    return Color(int(255 * r), int(255 * g), int(255 * b))

RED = Color(255, 0, 0)
LIME = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
PURPLE = Color(128, 0, 128)
YELLOW = Color(204, 204, 0) 
ORANGE = Color(255, 128, 0)
WHITE = Color(255, 255, 255, 255)
GOLD = color(1.00, 0.67, 0.00)
SPRING_GREEN = color(0.00, 1.00, 0.20)
TURQUOISE = color(0.25, 0.88, 0.82)
AQUA = color(0.00, 1.00, 1.00)
PINK = color(1.00, 0.00, 0.80)

LOW_BRIGHTNESS = 55
HIGH_BRIGHTNESS = 255
MID_BRIGHTNESS = 155


temperature_to_color = {
    6:  color(0.86, 0.16, 0.16),
    7:  color(0.93, 0.17, 0.17),
    8:  color(1.00, 0.00, 0.00),
    9:  color(1.00, 0.25, 0.25),
    10: color(0.99, 0.80, 0.00),
    11: color(1.00, 0.34, 0.13),
    12: color(0.97, 0.46, 0.19),
    13: color(1.00, 0.45, 0.90),
    14: color(1.00, 0.55, 0.00),
    15: color(1.00, 0.65, 0.00),
    16: color(1.00, 0.76, 0.15),
    17: color(0.99, 0.82, 0.90),
    18: color(1.00, 0.89, 1.00),
    19: color(1.00, 0.90, 0.00),
    20: color(1.00, 1.00, 0.00),
    21: color(0.78, 0.96, 0.15),
    22: color(0.75, 1.00, 0.24),
    23: color(0.46, 0.93, 0.00),
    24: color(0.00, 1.00, 0.00),
    25: color(0.00, 1.00, 0.20),
    26: color(0.25, 0.88, 0.82),
    27: color(0.00, 1.00, 1.00),
    28: color(0.20, 0.93, 1.00),
    29: color(0.00, 0.50, 1.00),
    30: color(0.00, 0.00, 1.00),
    31: color(0.50, 0.00, 1.00),
    32: color(0.60, 0.20, 0.80),
    33: color(0.58, 0.00, 0.83),
    34: color(0.80, 0.00, 0.80),
}


humidity_to_color = {
    51:  color(0.86, 0.16, 0.16),
    52:  color(0.93, 0.17, 0.17),
    53:  color(1.00, 0.00, 0.00),
    54:  color(1.00, 0.25, 0.25),
    55:  color(0.99, 0.80, 0.00),
    56:  color(1.00, 0.34, 0.13),
    57:  color(0.97, 0.46, 0.19),
    58:  color(1.00, 0.45, 0.90),
    59:  color(1.00, 0.55, 0.00),
    60:  color(1.00, 0.65, 0.00),
    61:  color(1.00, 0.76, 0.15),
    62:  color(1.00, 0.80, 0.70),
    63:  color(0.99, 0.82, 0.90),
    64:  color(0.99, 0.86, 0.23),
    65:  color(1.00, 0.89, 0.10),
    66:  color(0.98, 0.93, 0.36),
    67:  color(1.00, 0.90, 0.00),
    68:  color(0.93, 0.93, 0.00),
    69:  color(1.00, 1.00, 0.00),
    70:  color(0.78, 0.96, 0.15),
    71:  color(0.67, 0.87, 0.00),
    72:  color(0.61, 0.80, 0.10),
    73:  color(0.75, 1.00, 0.24),
    74:  color(0.68, 1.00, 0.18),
    75:  color(0.46, 0.93, 0.00),
    76:  color(0.49, 0.99, 0.00),
    77:  color(0.00, 1.00, 0.00),
    78:  color(0.20, 1.00, 0.20),
    79:  color(0.00, 1.00, 0.20),
    80:  color(0.00, 1.00, 0.80),
    81:  color(0.25, 0.88, 0.82),
    82:  color(0.22, 0.99, 0.99),
    83:  color(0.00, 1.00, 1.00),
    84:  color(0.00, 0.96, 1.00),
    85:  color(0.20, 0.93, 1.00),
    86:  color(0.40, 0.71, 1.00),
    87:  color(0.00, 0.50, 1.00),
    88:  color(0.00, 0.28, 0.98),
    89:  color(0.00, 0.00, 1.00),
    90:  color(0.20, 0.00, 1.00),
    91:  color(0.50, 0.00, 1.00),
    92:  color(0.61, 0.19, 1.00),
    93:  color(0.60, 0.20, 0.80),
    94:  color(0.67, 0.00, 1.00),
    95:  color(0.58, 0.00, 0.83),
    96:  color(0.80, 0.00, 1.00),
    97:  color(0.86, 0.44, 0.86),
    98:  color(0.80, 0.00, 0.80),
    99:  color(0.93, 0.00, 0.93),
    100: color(1.00, 0.00, 1.00),
}


def ms_to_s(ms):
    """Convert ms to s"""
    return ms/1000.0


def hue_to_rgb(h):
    """Convert a hue into an r, g, b color"""
    return [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]


# Define functions which animate LEDs in various ways.
def set_pixel(strip1, strip2, pixel, color):
    strip1.setPixelColor(pixel, color)
    strip2.setPixelColor(pixel, color)

def show(strip1, strip2):
    strip1.show()
    strip2.show()

def set_brightness(strip1, strip2, brightness):
    strip1.setBrightness(brightness)
    strip2.setBrightness(brightness)

def color_wipe(strip1, strip2, color, wait_ms=BETWEEN_LED_CHANGES_SLOW):
    """Wipe color across display a pixel at a time."""
    for i in range(strip1.numPixels()):
        set_pixel(strip1, strip2, i, color)
        show(strip1, strip2)
        time.sleep(ms_to_s(wait_ms))


def monochrome(strip1, strip2, color):
    for i in range(strip1.numPixels()):
        set_pixel(strip1, strip2, i, color)
    show(strip1, strip2)


def turn_off(strip1, strip2):
    monochrome(strip1, strip2, Color(0, 0, 0))


def flash(color, wait_ms=BETWEEN_STRIP_CHANGES_SLOW):
    def with_strip(strip1, strip2):
        set_brightness(strip1, strip2, 255)
        monochrome(strip1, strip2, color)
        time.sleep(ms_to_s(wait_ms))
        turn_off(strip1, strip2)

    return with_strip


def flash_then_on(from_color, flash_freq, to_color, to_brightness, to_seconds):
    def with_strip(strip1, strip2):
        set_brightness(strip1, strip2, 255)
        for i in range(flash_freq):
            flash(from_color)(strip1, strip2)
            time.sleep(ms_to_s(BETWEEN_STRIP_CHANGES_SLOW))

        set_brightness(strip1, strip2, to_brightness)
        monochrome(strip1, strip2, to_color)
        time.sleep(to_seconds)

    return with_strip


def flash_for_seconds(colors, seconds):
    def with_strip(strip1, strip2):
        set_brightness(strip1, strip2, 255)
        flicker_end = time.time() + seconds
        idx = 0

        while time.time() < flicker_end:
            flash(colors[idx % len(colors)], BETWEEN_STRIP_CHANGES_FAST)(strip1, strip2)
            time.sleep(ms_to_s(BETWEEN_STRIP_CHANGES_FAST))

    return with_strip


def flicker_then_on(from_color, flicker_seconds, to_color, to_brightness, to_seconds):
    def with_strip(strip1, strip2):
        set_brightness(strip1, strip2, 50)
        flicker_end = time.time() + 5
        while time.time() < flicker_end:
            flash(from_color, BETWEEN_LED_CHANGES_SLOW)(strip1, strip2)
            time.sleep(ms_to_s(BETWEEN_LED_CHANGES_SLOW))

        set_brightness(strip1, strip2, to_brightness)
        monochrome(strip1, strip2, to_color)
        time.sleep(to_seconds)

    return with_strip


def on(color, for_seconds):
    def with_strip(strip1, strip2):
        set_brightness(strip1, strip2, 255)
        monochrome(strip1, strip2, color)
        time.sleep(for_seconds)

    return with_strip


def color_swipe_to_color(start_color, start_seconds, swipe_color, swipe_speed, end_color, end_seconds):
    def with_strip(strip1, strip2):
        set_brightness(strip1, strip2, 255)
        monochrome(strip1, strip2, start_color)
        time.sleep(start_seconds)
        color_wipe(strip1, strip2, swipe_color, swipe_speed)
        monochrome(strip1, strip2, end_color)
        time.sleep(end_seconds)

    return with_strip


def low_to_high_brightness(color, start_brightness, start_seconds, end_brightness, end_seconds):
    def with_strip(strip1, strip2):
        set_brightness(strip1, strip2, start_brightness)
        monochrome(strip1, strip2, color)
        time.sleep(start_seconds)

        brightness = start_brightness
        while brightness <= end_brightness:
            set_brightness(strip1, strip2, brightness)
            show(strip1, strip2)
            time.sleep(ms_to_s(BETWEEN_LED_CHANGES_FAST))
            brightness += 10

        time.sleep(end_seconds)

    return with_strip


def low_to_high_flicker(color, low_brightness, high_brightness):
    def with_strip(strip1, strip2):
        set_brightness(strip1, strip2, low_brightness)
        monochrome(strip1, strip2, color)

        flicker_end = time.time() + 10
        brightness = low_brightness
        up = True
        while time.time() < flicker_end:
            if up:
                brightness = brightness + 10
                if brightness >= high_brightness:
                    up = False
            else:
                brightness = brightness - 10
                if brightness <= low_brightness:
                    up = True

            set_brightness(strip1, strip2, brightness)
            show(strip1, strip2)

            time.sleep(ms_to_s(BETWEEN_LED_CHANGES_FAST))

    return with_strip


def rainbow_wipe(colors, wait_ms=BETWEEN_LED_CHANGES_FAST):
    def with_strip(strip1, strip2):
        segment = strip1.numPixels() // len(colors)

        def color_from_i(i):
            selected_color = colors[0]
            for color_i, color in enumerate(colors):
                if i > segment * color_i:
                    selected_color = color

            return selected_color

        set_brightness(strip1, strip2, 255)
        for i in range(strip1.numPixels()):
            pixel_color = color_from_i(i)
            set_pixel(strip1, strip2, i, pixel_color)
            show(strip1, strip2)
            
            time.sleep(ms_to_s(wait_ms))

        for i in range(strip1.numPixels()):
            pixel_color = color_from_i(i)
            set_pixel(strip1, strip2, strip1.numPixels() - i, pixel_color)
            show(strip1, strip2)
            
            time.sleep(ms_to_s(wait_ms))

    return with_strip


def chain(functions):
    def with_strip(strip1, strip2):
        for function in functions:
            function(strip1, strip2)


iterations = {
    1:  flash_then_on(LIME, 3, LIME, MID_BRIGHTNESS, 10),
    2:  flash_then_on(BLUE, 3, BLUE, MID_BRIGHTNESS, 10),
    3:  flash_then_on(RED, 3, RED, MID_BRIGHTNESS, 10),
    4:  flash_then_on(PURPLE, 3, PURPLE, MID_BRIGHTNESS, 10),
    5:  flash_then_on(YELLOW, 3, YELLOW, MID_BRIGHTNESS, 10),
    6:  flash_then_on(ORANGE, 3, ORANGE, MID_BRIGHTNESS, 10),
    7:  flash_then_on(GOLD, 3, GOLD, MID_BRIGHTNESS, 10),
    8:  flash_then_on(SPRING_GREEN, 3, SPRING_GREEN, MID_BRIGHTNESS, 10),
    9:  flash_then_on(TURQUOISE, 3, TURQUOISE, MID_BRIGHTNESS, 10),
    10: flash_then_on(AQUA, 3, AQUA, MID_BRIGHTNESS, 10),
    11: flash_then_on(PINK, 3, PINK, MID_BRIGHTNESS, 10),

    12: on(LIME, 10),
    13: on(BLUE, 10),
    14: on(RED, 10),
    15: on(PURPLE, 10),
    16: on(YELLOW, 10),
    17: on(ORANGE, 10),
    18: on(WHITE, 10),
    19: on(GOLD, 10),
    20: on(SPRING_GREEN, 10),
    21: on(TURQUOISE, 10),
    22: on(AQUA, 10),
    23: on(PINK, 10),

    24: color_swipe_to_color(RED, 5, BLUE, BETWEEN_LED_CHANGES_SLOW, BLUE, 5),
    25: color_swipe_to_color(BLUE, 5, RED, BETWEEN_LED_CHANGES_SLOW, RED, 5),
    26: color_swipe_to_color(RED, 5, LIME, BETWEEN_LED_CHANGES_SLOW, SPRING_GREEN, 5),
    27: color_swipe_to_color(LIME, 5, RED, BETWEEN_LED_CHANGES_SLOW, RED, 5),
    28: color_swipe_to_color(YELLOW, 5, PURPLE, BETWEEN_LED_CHANGES_SLOW, PURPLE, 5),
    29: color_swipe_to_color(PURPLE, 5, ORANGE, BETWEEN_LED_CHANGES_SLOW, ORANGE, 5),
    30: color_swipe_to_color(ORANGE, 5, YELLOW, BETWEEN_LED_CHANGES_SLOW, YELLOW, 5),
    31: color_swipe_to_color(PURPLE, 5, YELLOW, BETWEEN_LED_CHANGES_SLOW, YELLOW, 5),

    32: flicker_then_on(LIME, 5, LIME, LOW_BRIGHTNESS, 5),
    33: flicker_then_on(BLUE, 5, BLUE, LOW_BRIGHTNESS, 5),
    34: flicker_then_on(RED, 5, RED, LOW_BRIGHTNESS, 5),
    35: flicker_then_on(PURPLE, 5, PURPLE, LOW_BRIGHTNESS, 5),
    36: flicker_then_on(YELLOW, 5, YELLOW, LOW_BRIGHTNESS, 5),
    37: flicker_then_on(ORANGE, 5, ORANGE, LOW_BRIGHTNESS, 5),
    39: flicker_then_on(WHITE, 5, WHITE, LOW_BRIGHTNESS, 5),
    40: flicker_then_on(GOLD, 5, GOLD, LOW_BRIGHTNESS, 5),
    41: flicker_then_on(SPRING_GREEN, 5, SPRING_GREEN, LOW_BRIGHTNESS, 5),
    42: flicker_then_on(TURQUOISE, 5, TURQUOISE, LOW_BRIGHTNESS, 5),
    43: flicker_then_on(AQUA, 5, AQUA, LOW_BRIGHTNESS, 5),
    44: flicker_then_on(PINK, 5, PINK, LOW_BRIGHTNESS, 5),

    45: flash_then_on(RED, 3, BLUE, HIGH_BRIGHTNESS, 10),
    46: flash_then_on(BLUE, 3, LIME, HIGH_BRIGHTNESS, 10),
    47: flash_then_on(LIME, 3, BLUE, HIGH_BRIGHTNESS, 10),
    48: flash_then_on(BLUE, 3, RED, HIGH_BRIGHTNESS, 10),
    49: flash_then_on(PURPLE, 3, YELLOW, HIGH_BRIGHTNESS, 10),
    50: flash_then_on(YELLOW, 3, ORANGE, HIGH_BRIGHTNESS, 10),
    51: flash_then_on(ORANGE, 3, YELLOW, HIGH_BRIGHTNESS, 10),
    52: flash_then_on(YELLOW, 3, PURPLE, HIGH_BRIGHTNESS, 10),

    53: chain([flash(LIME), low_to_high_flicker(LIME, LOW_BRIGHTNESS, 200)]),
    54: chain([flash(RED), low_to_high_flicker(RED, LOW_BRIGHTNESS, 200)]),
    55: chain([flash(BLUE), low_to_high_flicker(BLUE, LOW_BRIGHTNESS, 200)]),
    56: chain([flash(YELLOW), low_to_high_flicker(YELLOW, LOW_BRIGHTNESS, 200)]),
    57: chain([flash(PURPLE), low_to_high_flicker(PURPLE, LOW_BRIGHTNESS, 200)]),
    58: chain([flash(ORANGE), low_to_high_flicker(ORANGE, LOW_BRIGHTNESS, 200)]),
    59: chain([flash(WHITE), low_to_high_flicker(WHITE, LOW_BRIGHTNESS, 200)]),
    60: chain([flash(GOLD), low_to_high_flicker(GOLD, LOW_BRIGHTNESS, 200)]),
    61: chain([flash(SPRING_GREEN), low_to_high_flicker(SPRING_GREEN, LOW_BRIGHTNESS, 200)]),
    62: chain([flash(TURQUOISE), low_to_high_flicker(TURQUOISE, LOW_BRIGHTNESS, 200)]),
    63: chain([flash(AQUA), low_to_high_flicker(AQUA, LOW_BRIGHTNESS, 200)]),
    64: chain([flash(PINK), low_to_high_flicker(PINK, LOW_BRIGHTNESS, 200)]),

    65: low_to_high_brightness(LIME, LOW_BRIGHTNESS, 5, 100, 10),
    38: low_to_high_brightness(RED, LOW_BRIGHTNESS, 5, 100, 10),
    66: low_to_high_brightness(BLUE, LOW_BRIGHTNESS, 5, 100, 10),
    67: low_to_high_brightness(YELLOW, LOW_BRIGHTNESS, 5, 100, 10),
    68: low_to_high_brightness(PURPLE, LOW_BRIGHTNESS, 5, 100, 10),
    69: low_to_high_brightness(ORANGE, LOW_BRIGHTNESS, 5, 100, 10),
    70: low_to_high_brightness(WHITE, LOW_BRIGHTNESS, 5, 100, 10),
    71: low_to_high_brightness(GOLD, LOW_BRIGHTNESS, 5, 100, 10),
    72: low_to_high_brightness(SPRING_GREEN, LOW_BRIGHTNESS, 5, 100, 10),
    73: low_to_high_brightness(TURQUOISE, LOW_BRIGHTNESS, 5, 100, 10),
    74: low_to_high_brightness(AQUA, LOW_BRIGHTNESS, 5, 100, 10),
    75: low_to_high_brightness(PINK, LOW_BRIGHTNESS, 5, 100, 10),

    76: flash_then_on(WHITE, 2, WHITE, HIGH_BRIGHTNESS, 10),
    77: flash_then_on(WHITE, 2, WHITE, HIGH_BRIGHTNESS, 10),
    78: flash_then_on(WHITE, 2, WHITE, HIGH_BRIGHTNESS, 10),
    79: flash_then_on(WHITE, 2, WHITE, HIGH_BRIGHTNESS, 10),
    80: flash_then_on(WHITE, 2, WHITE, HIGH_BRIGHTNESS, 10),

    81: flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    82: flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    83: flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    84: flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    85: flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    86: flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    87: flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    88: flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    89: flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    90: flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),

    91: rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    92: rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    93: rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    94: rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    95: rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    96: rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    97: rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    98: rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    99: rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    100: rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
}

# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip1 = PixelStrip(LED_COUNT, LED1_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED1_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip1.begin()

    # Create NeoPixel object with appropriate configuration.
    strip2 = PixelStrip(LED_COUNT, LED2_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED2_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip2.begin()

    # Create PIR object
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)

    instance = dht22.DHT22(pin=26)

    print('Starting (:')

    # count = 1
    last_temperature = 25
    last_humidity = 70

    while True:
        moving = GPIO.input(MOTION_SENSOR_PIN)

        if moving:
            print('Motion detected')
            iteration = random.choice(list(iterations.values()))
            iteration(strip1, strip2)
            time.sleep(ms_to_s(BETWEEN_ITERATIONS))
            # count = 1 if count == 20 else count + 1
        else:
            result = instance.read()

            if result.is_valid():
                last_humidity = result.humidity
                last_temperature = result.temperature
                print(f'No motion: Humidity: {last_humidity} & temperature: {last_temperature}')

            if last_temperature <= 5:
                monochrome(strip1, strip1, color(0.65, 0.16, 0.16))
            elif last_temperature >= 35:
                monochrome(strip1, strip1, color(1.00, 0.00, 1.00))
            else:
                monochrome(strip1, strip1, temperature_to_color[int(last_temperature)])

            if last_humidity <= 50:
                monochrome(strip2, strip2, color(0.65, 0.16, 0.16))
            elif last_humidity >= 100:
                monochrome(strip2, strip2, color(1.00, 0.00, 1.00))
            else:
                monochrome(strip2, strip2, humidity_to_color[int(last_humidity)])

            time.sleep(ms_to_s(BETWEEN_ITERATIONS))

