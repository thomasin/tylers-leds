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


    def flash(self, color, wait_ms):
        self.monochrome_pixels(color)
        yield wait_ms
        self.off_pixels()
        yield wait_ms


    def flash_for_n(self, from_color, flash_freq, wait_ms):
        self.brightness = 255
        for i in range(flash_freq):
            for ms in self.flash(from_color, wait_ms):
                yield ms


    def flash_for_seconds(self, colors, seconds, wait_ms):
        self.brightness = 255
        flash_freq = (seconds * 1000) / wait_ms

        for idx in range(int(flash_freq)):
            for ms in self.flash(colors[idx % len(colors)], wait_ms):
                yield ms


    # DEBUG
    def flicker(self, color, flicker_seconds, wait_ms):
        self.brightness = 50
        flicker_freq = flicker_seconds / wait_ms

        # print(flicker_freq)

        for _ in range(int(flicker_freq)):
            for ms in self.flash(color, wait_ms):
                yield ms


    def on(self, color, seconds, brightness=255):
        self.brightness = brightness
        self.monochrome_pixels(color)
        yield seconds * 1000


    def gradient(self, pixels, wait_ms, brightness=255):
        self.brightness = brightness

        for i in range(self.length):
            if i < len(pixels):
                self.set_pixel(i, pixels[i])

        yield wait_ms


    def fade_brightness(self, start_brightness, end_brightness, wait_ms):
        self.brightness = start_brightness

        while self.brightness <= end_brightness:
            yield wait_ms
            self.brightness += 10


    def flicker_brightness(self, low_brightness, high_brightness, wait_ms):
        flicker_freq = (10*1000) / wait_ms
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
            yield wait_ms


    def wipe(self, pixels, wait_ms):
        """Wipe color across display a pixel at a time."""
        for i in range(self.length):
            if i < len(pixels):
                self.set_pixel(i, pixels[i])
                yield wait_ms


    def cycle(self, pixels, wait_ms):
        # In cases where the colors don't divide perfectly into the strip, this
        # will be larger than the strip length!
        elements = pixels * ceil(self.length / len(pixels))

        while True:
            for i, color in enumerate(elements):
                self.set_pixel(i, color)

            elements.append(elements.pop(0))
            yield wait_ms







