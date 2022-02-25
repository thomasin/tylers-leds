import colour
import time
from math import ceil
import itertools


class Strips:
    def __init__(self, led_strips):
        self.led_strips = led_strips


    def __iter__(self):
        return iter(self.led_strips)


    def animate(self, animation):
        for leds in self.led_strips:
            leds.brightness = 255

        for wait_ms in zip(*[animation(leds) for leds in self.led_strips]):
            yield wait_ms[0]



class Strip:
    def __init__(self, strip, length, color, brightness=255):
        self.strip = strip
        self.pixels = [color] * length
        self.brightness = brightness
        self.length = length


    def set_pixel(self, i, pixel_color):
        if i < self.length:
            self.pixels[i] = pixel_color


    def monochrome_pixels(self, color):
        for i in range(self.length):
            self.set_pixel(i, color)


    def off_pixels(self):
        self.monochrome_pixels(colour.Color(rgb=(0, 0, 0)))


    def flash(self, colors, speed):
        idx = 0

        while True:
            self.monochrome_pixels(colors[idx % len(colors)])
            yield speed
            self.off_pixels()
            yield speed
            idx += 1


    def flash_for(self, colors, speed, brightness=255, *, seconds=0, n=None):
        self.brightness = brightness
        flash_freq = n if n is not None else (seconds * 1000) / (speed * 2)
        flash = self.flash(colors, speed)

        for _ in range(int(flash_freq * 2)):
            yield next(flash)


    def on(self, color, seconds, brightness=255):
        self.brightness = brightness
        self.monochrome_pixels(color)
        yield seconds * 1000


    def gradient(self, pixels, speed, brightness=255):
        self.brightness = brightness

        for i in range(self.length):
            if i < len(pixels):
                self.set_pixel(i, pixels[i])

        yield speed


    def fade_brightness(self, start_brightness, end_brightness, speed):
        self.brightness = start_brightness

        while self.brightness <= end_brightness:
            yield speed
            self.brightness += 10


    def flicker_brightness(self, low_brightness, high_brightness, speed):
        flicker_freq = (10*1000) / speed
        brightness = low_brightness
        up = True

        for _ in range(int(flicker_freq)):
            if up:
                brightness = brightness + 10
                if brightness >= high_brightness:
                    up = False
            else:
                brightness = brightness - 10
                if brightness <= low_brightness:
                    up = True

            self.brightness = brightness
            yield speed


    def wipe(self, pixels, speed):
        """Wipe color across display a pixel at a time."""
        for i in range(self.length):
            if i < len(pixels):
                self.set_pixel(i, pixels[i])
                yield speed


    def cycle(self, pixels, speed):
        # In cases where the colors don't divide perfectly into the strip, this
        # will be larger than the strip length!
        elements = pixels * ceil(self.length / len(pixels))

        while True:
            for i, color in enumerate(elements):
                self.set_pixel(i, color)

            elements.append(elements.pop(0))
            yield speed







