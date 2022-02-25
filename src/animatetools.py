import colour
import colortools
import ledtools
import time
from math import ceil


# LED design configuration
BETWEEN_STRIP_CHANGES_SLOW = 250
BETWEEN_STRIP_CHANGES_FAST = 75
BETWEEN_LED_CHANGES_SLOW = 50
BETWEEN_LED_CHANGES_FAST = 25

RED = colour.Color(rgb=(1.00, 0.00, 0.00))
LIME = colour.Color(rgb=(0.00, 1.00, 0.00))
BLUE = colour.Color(rgb=(0.00, 0.00, 1.00))
PURPLE = colour.Color(rgb=(0.50, 0.00, 0.50))
YELLOW = colour.Color(rgb=(0.80, 0.80, 0.00))
ORANGE = colour.Color(rgb=(1.00, 0.50, 0.00))
WHITE = colour.Color(rgb=(1.00, 1.00, 1.00))
GOLD = colour.Color(rgb=(0.89, 0.67, 0.26))
SPRING_GREEN = colour.Color(rgb=(0.00, 1.00, 0.20))
TURQUOISE = colour.Color(rgb=(0.25, 0.88, 0.82))
AQUA = colour.Color(rgb=(0.00, 1.00, 1.00))
PINK = colour.Color(rgb=(1.00, 0.00, 0.80))
BLACK = colour.Color(rgb=(0.00, 0.00, 0.00))

LOW_BRIGHTNESS = 55
MED_BRIGHTNESS = 100
HIGH_BRIGHTNESS = 255
MID_BRIGHTNESS = 155


def chain(functions):
    def with_strip(strip):
        for function in functions:
            for x in function(strip):
                yield x

    return with_strip


def flash(color):
    def with_strip(strip):
        for x in strip.flash_for_n(color, 1, BETWEEN_STRIP_CHANGES_SLOW):
            yield x

    return with_strip


def flash_then_on(from_color, flash_freq, to_color, to_brightness, to_seconds):
    def with_strip(strip):
        for x in strip.flash_for_n(from_color, flash_freq, BETWEEN_STRIP_CHANGES_SLOW):
            yield x

        for x in strip.on(to_color, to_seconds, to_brightness):
            yield x

    return with_strip


def on(color, for_seconds):
    def with_strip(strip):
        for x in strip.on(color, for_seconds):
            yield x

    return with_strip


def color_swipe_to_color(start_color, start_seconds, swipe_color, swipe_speed, end_color, end_seconds):
    def with_strip(strip):
        for x in strip.on(start_color, start_seconds):
            yield x

        for x in strip.wipe([swipe_color] * strip.length, swipe_speed):
            yield x
        
        for x in strip.on(end_color, end_seconds):
            yield x

    return with_strip


def flicker_then_on(from_color, flicker_seconds, to_color, to_brightness, to_seconds):
    def with_strip(strip):
        for x in strip.flicker(from_color, flicker_seconds, BETWEEN_LED_CHANGES_FAST):
            yield x

        for x in strip.on(to_color, to_seconds, to_brightness):
            yield x

    return with_strip


def flash_for_seconds(colors, seconds):
    def with_strip(strip):
        for x in strip.flash_for_seconds(colors, seconds, BETWEEN_LED_CHANGES_FAST):
            yield x

    return with_strip


def low_to_high_brightness(color, start_brightness, start_seconds, end_brightness, end_seconds):
    def with_strip(strip):
        for x in strip.on(color, start_seconds, start_brightness):
            yield x

        for x in strip.fade_brightness(start_brightness, end_brightness, BETWEEN_LED_CHANGES_FAST):
            yield x

        for x in strip.on(color, end_seconds, end_brightness):
            yield x

    return with_strip


def low_to_high_flicker(color, low_brightness, high_brightness):
    def with_strip(strip):
        for x in strip.on(color, 0, low_brightness):
            yield x

        for x in strip.flicker_brightness(low_brightness, high_brightness, BETWEEN_LED_CHANGES_FAST):
            yield x

    return with_strip


def rainbow_wipe(colors):
    def with_strip(strip):
        pixels = colortools.rainbow(strip.length, colors)

        for x in strip.wipe(pixels, BETWEEN_LED_CHANGES_FAST):
            yield x

    return with_strip


def strip_length_cycle(pixels):
    def with_strip(strip):
        generator = strip.cycle(pixels(strip.length), BETWEEN_LED_CHANGES_FAST)

        for idx in range(strip.length * 2):
            yield next(generator)

    return with_strip


def cycle(pixels):
    def with_strip(strip):
        generator = strip.cycle(pixels, BETWEEN_LED_CHANGES_FAST)

        for idx in range(strip.length * 2):
            yield next(generator)

    return with_strip


# test
def gradient_expand(end_color, middle_color):
    def with_strip(strip):
        for idx in range(ceil(strip.length / 2)):
            pixels = colortools.Scale([
                (end_color, -1),
                (middle_color, (strip.length // 2) - idx),
                (middle_color, (strip.length // 2) + idx),
                (end_color, strip.length),
            ])

            for x in strip.gradient(pixels.between(0, strip.length), BETWEEN_LED_CHANGES_FAST):
                yield x

    return with_strip


animations = {
    1:   flash_then_on(LIME, 3, LIME, MID_BRIGHTNESS, 10),
    2:   flash_then_on(BLUE, 3, BLUE, MID_BRIGHTNESS, 10),
    3:   flash_then_on(RED, 3, RED, MID_BRIGHTNESS, 10),
    4:   flash_then_on(PURPLE, 3, PURPLE, MID_BRIGHTNESS, 10),
    5:   flash_then_on(YELLOW, 3, YELLOW, MID_BRIGHTNESS, 10),
    6:   flash_then_on(ORANGE, 3, ORANGE, MID_BRIGHTNESS, 10),
    7:   flash_then_on(GOLD, 3, GOLD, MID_BRIGHTNESS, 10),
    8:   flash_then_on(SPRING_GREEN, 3, SPRING_GREEN, MID_BRIGHTNESS, 10),
    9:   flash_then_on(TURQUOISE, 3, TURQUOISE, MID_BRIGHTNESS, 10),
    10:  flash_then_on(AQUA, 3, AQUA, MID_BRIGHTNESS, 10),
    11:  flash_then_on(PINK, 3, PINK, MID_BRIGHTNESS, 10),

    12:  on(LIME, 10),
    13:  on(BLUE, 10),
    14:  on(RED, 10),
    15:  on(PURPLE, 10),
    16:  on(YELLOW, 10),
    17:  on(ORANGE, 10),
    18:  on(WHITE, 10),
    19:  on(GOLD, 10),
    20:  on(SPRING_GREEN, 10),
    21:  on(TURQUOISE, 10),
    22:  on(AQUA, 10),
    23:  on(PINK, 10),

    24:  color_swipe_to_color(RED, 5, BLUE, BETWEEN_LED_CHANGES_SLOW, BLUE, 5),
    25:  color_swipe_to_color(BLUE, 5, RED, BETWEEN_LED_CHANGES_SLOW, RED, 5),
    26:  color_swipe_to_color(RED, 5, LIME, BETWEEN_LED_CHANGES_SLOW, SPRING_GREEN, 5),
    27:  color_swipe_to_color(LIME, 5, RED, BETWEEN_LED_CHANGES_SLOW, RED, 5),
    28:  color_swipe_to_color(YELLOW, 5, PURPLE, BETWEEN_LED_CHANGES_SLOW, PURPLE, 5),
    29:  color_swipe_to_color(PURPLE, 5, ORANGE, BETWEEN_LED_CHANGES_SLOW, ORANGE, 5),
    30:  color_swipe_to_color(ORANGE, 5, YELLOW, BETWEEN_LED_CHANGES_SLOW, YELLOW, 5),
    31:  color_swipe_to_color(PURPLE, 5, YELLOW, BETWEEN_LED_CHANGES_SLOW, YELLOW, 5),

    # Debug
    32:  flicker_then_on(LIME, 5, LIME, LOW_BRIGHTNESS, 5),
    33:  flicker_then_on(BLUE, 5, BLUE, LOW_BRIGHTNESS, 5),
    34:  flicker_then_on(RED, 5, RED, LOW_BRIGHTNESS, 5),
    35:  flicker_then_on(PURPLE, 5, PURPLE, LOW_BRIGHTNESS, 5),
    36:  flicker_then_on(YELLOW, 5, YELLOW, LOW_BRIGHTNESS, 5),
    37:  flicker_then_on(ORANGE, 5, ORANGE, LOW_BRIGHTNESS, 5),
    39:  flicker_then_on(WHITE, 5, WHITE, LOW_BRIGHTNESS, 5),
    40:  flicker_then_on(GOLD, 5, GOLD, LOW_BRIGHTNESS, 5),
    41:  flicker_then_on(SPRING_GREEN, 5, SPRING_GREEN, LOW_BRIGHTNESS, 5),
    42:  flicker_then_on(TURQUOISE, 5, TURQUOISE, LOW_BRIGHTNESS, 5),
    43:  flicker_then_on(AQUA, 5, AQUA, LOW_BRIGHTNESS, 5),
    44:  flicker_then_on(PINK, 5, PINK, LOW_BRIGHTNESS, 5),
    # --

    45:  flash_then_on(RED, 3, BLUE, HIGH_BRIGHTNESS, 10),
    46:  flash_then_on(BLUE, 3, LIME, HIGH_BRIGHTNESS, 10),
    47:  flash_then_on(LIME, 3, BLUE, HIGH_BRIGHTNESS, 10),
    48:  flash_then_on(BLUE, 3, RED, HIGH_BRIGHTNESS, 10),
    49:  flash_then_on(PURPLE, 3, YELLOW, HIGH_BRIGHTNESS, 10),
    50:  flash_then_on(YELLOW, 3, ORANGE, HIGH_BRIGHTNESS, 10),
    51:  flash_then_on(ORANGE, 3, YELLOW, HIGH_BRIGHTNESS, 10),
    52:  flash_then_on(YELLOW, 3, PURPLE, HIGH_BRIGHTNESS, 10),

    53:  chain([flash(LIME), low_to_high_flicker(LIME, LOW_BRIGHTNESS, 200)]),
    54:  chain([flash(RED), low_to_high_flicker(RED, LOW_BRIGHTNESS, 200)]),
    55:  chain([flash(BLUE), low_to_high_flicker(BLUE, LOW_BRIGHTNESS, 200)]),
    56:  chain([flash(YELLOW), low_to_high_flicker(YELLOW, LOW_BRIGHTNESS, 200)]),
    57:  chain([flash(PURPLE), low_to_high_flicker(PURPLE, LOW_BRIGHTNESS, 200)]),
    58:  chain([flash(ORANGE), low_to_high_flicker(ORANGE, LOW_BRIGHTNESS, 200)]),
    59:  chain([flash(WHITE), low_to_high_flicker(WHITE, LOW_BRIGHTNESS, 200)]),
    60:  chain([flash(GOLD), low_to_high_flicker(GOLD, LOW_BRIGHTNESS, 200)]),
    61:  chain([flash(SPRING_GREEN), low_to_high_flicker(SPRING_GREEN, LOW_BRIGHTNESS, 200)]),
    62:  chain([flash(TURQUOISE), low_to_high_flicker(TURQUOISE, LOW_BRIGHTNESS, 200)]),
    63:  chain([flash(AQUA), low_to_high_flicker(AQUA, LOW_BRIGHTNESS, 200)]),
    64:  chain([flash(PINK), low_to_high_flicker(PINK, LOW_BRIGHTNESS, 200)]),

    65:  low_to_high_brightness(LIME, LOW_BRIGHTNESS, 5, HIGH_BRIGHTNESS, 10),
    38:  low_to_high_brightness(RED, LOW_BRIGHTNESS, 5, HIGH_BRIGHTNESS, 10),
    66:  low_to_high_brightness(BLUE, LOW_BRIGHTNESS, 5, HIGH_BRIGHTNESS, 10),
    67:  low_to_high_brightness(YELLOW, LOW_BRIGHTNESS, 5, HIGH_BRIGHTNESS, 10),
    68:  low_to_high_brightness(PURPLE, LOW_BRIGHTNESS, 5, HIGH_BRIGHTNESS, 10),
    69:  low_to_high_brightness(ORANGE, LOW_BRIGHTNESS, 5, HIGH_BRIGHTNESS, 10),
    70:  low_to_high_brightness(WHITE, LOW_BRIGHTNESS, 5, HIGH_BRIGHTNESS, 10),
    71:  low_to_high_brightness(GOLD, LOW_BRIGHTNESS, 5, HIGH_BRIGHTNESS, 10),
    72:  low_to_high_brightness(SPRING_GREEN, LOW_BRIGHTNESS, 5, HIGH_BRIGHTNESS, 10),
    73:  low_to_high_brightness(TURQUOISE, LOW_BRIGHTNESS, 5, HIGH_BRIGHTNESS, 10),
    74:  low_to_high_brightness(AQUA, LOW_BRIGHTNESS, 5, HIGH_BRIGHTNESS, 10),
    75:  low_to_high_brightness(PINK, LOW_BRIGHTNESS, 5, HIGH_BRIGHTNESS, 10),

    76:  flash_then_on(WHITE, 2, WHITE, HIGH_BRIGHTNESS, 10),
    77:  flash_then_on(WHITE, 2, WHITE, HIGH_BRIGHTNESS, 10),
    78:  flash_then_on(WHITE, 2, WHITE, HIGH_BRIGHTNESS, 10),
    79:  flash_then_on(WHITE, 2, WHITE, HIGH_BRIGHTNESS, 10),
    80:  flash_then_on(WHITE, 2, WHITE, HIGH_BRIGHTNESS, 10),

    81:  flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    82:  flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    83:  flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    84:  flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    85:  flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    86:  flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    87:  flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    88:  flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    89:  flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),
    90:  flash_for_seconds([LIME, RED, BLUE, YELLOW, PURPLE, ORANGE, GOLD, SPRING_GREEN, TURQUOISE, AQUA, PINK], 10),

    91:  rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    92:  rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    93:  rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    94:  rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    95:  rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    96:  rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    97:  rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    98:  rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    99:  rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),
    100: rainbow_wipe([RED, YELLOW, PURPLE, BLUE, ORANGE, LIME]),

    101: strip_length_cycle(lambda n: colortools.gradient(n, LIME, BLACK)),
    102: strip_length_cycle(lambda n: colortools.gradient(n, RED, BLACK)),
    103: strip_length_cycle(lambda n: colortools.gradient(n, BLUE, BLACK)),
    104: strip_length_cycle(lambda n: colortools.gradient(n, YELLOW, BLACK)),
    105: strip_length_cycle(lambda n: colortools.gradient(n, ORANGE, BLACK)),
    106: strip_length_cycle(lambda n: colortools.gradient(n, WHITE, BLACK)),
    107: strip_length_cycle(lambda n: colortools.gradient(n, GOLD, BLACK)),
    108: strip_length_cycle(lambda n: colortools.gradient(n, SPRING_GREEN, BLACK)),
    109: strip_length_cycle(lambda n: colortools.gradient(n, TURQUOISE, BLACK)),
    110: strip_length_cycle(lambda n: colortools.gradient(n, AQUA, BLACK)),
    111: strip_length_cycle(lambda n: colortools.gradient(n, PINK, BLACK)),

    112: strip_length_cycle(lambda n: colortools.rainbow(n, [RED, YELLOW, PURPLE, BLUE, ORANGE, LIME])),
    113: strip_length_cycle(lambda n: colortools.rainbow(n, [RED, YELLOW, PURPLE, BLUE, ORANGE, LIME])),
    114: strip_length_cycle(lambda n: colortools.rainbow(n, [RED, YELLOW, PURPLE, BLUE, ORANGE, LIME])),
    115: strip_length_cycle(lambda n: colortools.rainbow(n, [RED, YELLOW, PURPLE, BLUE, ORANGE, LIME])),
    116: strip_length_cycle(lambda n: colortools.rainbow(n, [RED, YELLOW, PURPLE, BLUE, ORANGE, LIME])),
    117: strip_length_cycle(lambda n: colortools.rainbow(n, [RED, YELLOW, PURPLE, BLUE, ORANGE, LIME])),
    118: strip_length_cycle(lambda n: colortools.rainbow(n, [RED, YELLOW, PURPLE, BLUE, ORANGE, LIME])),
    119: strip_length_cycle(lambda n: colortools.rainbow(n, [RED, YELLOW, PURPLE, BLUE, ORANGE, LIME])),
    120: strip_length_cycle(lambda n: colortools.rainbow(n, [RED, YELLOW, PURPLE, BLUE, ORANGE, LIME])),

    121: cycle([PINK] * 10 + [LIME] * 10),
    122: cycle([BLUE] * 10 + [YELLOW] * 10),
    123: cycle([PURPLE] * 10 + [ORANGE] * 10),
    124: cycle([SPRING_GREEN] * 10 + [RED] * 10),
    125: cycle([GOLD] * 10 + [AQUA] * 10),

    126: cycle([BLACK] * 3 + [RED] * 2),
    127: cycle([BLACK] * 3 + [YELLOW] * 2),
    128: cycle([BLACK] * 3 + [PURPLE] * 2),
    129: cycle([BLACK] * 3 + [BLUE] * 2),
    130: cycle([BLACK] * 3 + [ORANGE] * 2),
    131: cycle([BLACK] * 3 + [LIME] * 2),

    132: cycle(colortools.Scale([(PINK, 0), (PURPLE, 10), (PINK, 20)]).between(0, 20)),
    133: cycle(colortools.Scale([(RED, 0), (YELLOW, 10), (RED, 20)]).between(0, 20)),
    134: cycle(colortools.Scale([(LIME, 0), (BLUE, 10), (LIME, 20)]).between(0, 20)),
    135: cycle(colortools.Scale([(LIME, 0), (BLUE, 10), (LIME, 20)]).between(0, 20)),
    136: cycle(colortools.Scale([(ORANGE, 0), (GOLD, 10), (ORANGE, 20)]).between(0, 20)),

    137: cycle([BLACK] * 5 + [RED] * 2 + [LIME] * 7 + [RED] * 2 + [BLACK] * 5),
    138: cycle([BLACK] * 5 + [YELLOW] * 2 + [BLUE] * 7 + [YELLOW] * 2 + [BLACK] * 5),
    139: cycle([BLACK] * 5 + [PURPLE] * 2 + [PINK] * 7 + [PURPLE] * 2 + [BLACK] * 5),
    140: cycle([BLACK] * 5 + [LIME] * 2 + [ORANGE] * 7 + [LIME] * 2 + [BLACK] * 5),
    141: cycle([BLACK] * 5 + [AQUA] * 2 + [TURQUOISE] * 7 + [AQUA] * 2 + [BLACK] * 5),

    142: strip_length_cycle(lambda n: colortools.gradient(n // 4, PINK, BLACK) + colortools.gradient(n // 4, LIME, BLACK)),
    143: strip_length_cycle(lambda n: colortools.gradient(n // 4, AQUA, BLACK) + colortools.gradient(n // 4, GOLD, BLACK)),
    144: strip_length_cycle(lambda n: colortools.gradient(n // 4, PURPLE, BLACK) + colortools.gradient(n // 4, BLUE, BLACK)),
    145: strip_length_cycle(lambda n: colortools.gradient(n // 4, ORANGE, BLACK) + colortools.gradient(n // 4, WHITE, BLACK)),

    150: gradient_expand(RED, YELLOW),
    151: gradient_expand(BLUE, LIME),
    152: gradient_expand(PURPLE, ORANGE),
    153: gradient_expand(PINK, BLACK),
}


RESET = '\033[0m'

def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)


if __name__ == '__main__':
    leds = ledtools.Strip(None, 290, PINK, 255)

    while True:
        cmd = input('✨ \033[94mNext:\033[0m ')
        print('', end='\r')

        animation = animations.get(int(cmd))

        if animation is not None:
            for ms in animation(leds):
                brightness = leds.brightness / 255
                output = ""

                for pixel in leds.pixels:
                    color = colour.Color(hsl=(pixel.hue, pixel.saturation, pixel.luminance * brightness))
                    output += get_color_escape(int(color.red * 255), int(color.green * 255), int(color.blue * 255), False)
                    output += "◼︎"
                    output += RESET

                print(output, end='\r')
                time.sleep(ms/1000)





