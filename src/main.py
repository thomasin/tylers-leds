import time
import random
import sys

import rpi_ws281x as leds
import RPi.GPIO as GPIO
import dht22
import colour

import colortools
import ledtools
import animatetools



# LED strip configuration:
LED_COUNT           = 290     # Number of LED pixels.
LEDTEMP_PIN         = 12      # GPIO pin connected to the temperature pixels (must support PWM!).
LEDHUMIDITY_PIN     = 13      # GPIO pin connected to the humidity pixels (must support PWM!).
LED_FREQ_HZ         = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA             = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS      = 155     # Set to 0 for darkest and 255 for brightest
LED_INVERT          = False   # True to invert the signal (when using NPN transistor level shift)
LEDTEMP_CHANNEL     = 0
LEDHUMIDITY_CHANNEL = 1
LED_STRIP           = leds.ws.WS2812_STRIP


# Motion Sensor configuration:
MOTION_SENSOR_PIN = 17


# Animation configuration:
BETWEEN_ITERATIONS = 750

temperature_scale = colortools.Scale([
    (animatetools.RED, 5),
    (animatetools.ORANGE, 11),
    (animatetools.YELLOW, 16),
    (animatetools.LIME, 22)
])

humidity_scale = colortools.Scale([
    (animatetools.RED, 50),
    (animatetools.ORANGE, 56),
    (animatetools.YELLOW, 61),
    (animatetools.LIME, 73)
])



# Convert virtual led representations into physical output

def ms_to_s(ms):
    return ms/1000

def set_pixel(strip, pixel, color):
    if color == colour.Color("white"):
        strip.setPixelColor(pixel, leds.Color(255, 255, 255, 255))

    else:
        strip.setPixelColor(pixel, leds.Color(int(255 * color.red), int(255 * color.green), int(255 * color.blue), 0))


def update(strips):
    for leds in strips:
        leds.strip.setBrightness(leds.brightness)

        for idx, color in enumerate(leds.pixels):
            set_pixel(leds.strip, idx, color)

    for leds in strips:
        leds.strip.show()


def run(strips, animation):
    for ms in strips.animate(animation):
        update(list(strips))
        time.sleep(ms/1000.0)



# Main loop
if __name__ == '__main__':
    debug = sys.argv[1] == '--debug' if len(sys.argv) > 1 else False
    print(sys.argv)

    # HARDWARE SETUP
    temp_strip = leds.PixelStrip(LED_COUNT, LEDTEMP_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LEDTEMP_CHANNEL, LED_STRIP)
    temp_strip.begin()

    humidity_strip = leds.PixelStrip(LED_COUNT, LEDHUMIDITY_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LEDHUMIDITY_CHANNEL, LED_STRIP)
    humidity_strip.begin()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)

    temp_humidity_sensor = dht22.DHT22(pin=26)

    # PROGRAM SETUP
    temperature_leds = ledtools.Strip(temp_strip, temp_strip.numPixels(), animatetools.BLACK, LED_BRIGHTNESS)
    humidity_leds = ledtools.Strip(humidity_strip, humidity_strip.numPixels(), animatetools.BLACK, LED_BRIGHTNESS)
    both_led_strips = ledtools.Strips([temperature_leds, humidity_leds])

    last_temperature = 25
    last_humidity = 70


    # ALL GOOD
    if debug:
        print('Starting in debug mode (:')

    else:
        print('Starting (:')


    if debug:
        while True:
            cmd = input("🔧 \033[94m Type 'temp', 'humidity', 'all', or an animation number:\033[0m ")

            if cmd == 'temp':
                print('Running temperature from 0 to 50')

                for num in range (0, 50):
                    temperature_leds.monochrome_pixels(temperature_scale.choose(int(num)))
                    update([temperature_leds])
                    time.sleep(ms_to_s(500))

            elif cmd == 'humidity':
                print('Running humidity from 0 to 100')

                for num in range (0, 100):
                    humidity_leds.monochrome_pixels(humidity_scale.choose(int(num)))
                    update([humidity_leds])
                    time.sleep(ms_to_s(500))

            elif cmd == 'all':
                for num, animation in animatetools.animations.items():
                    print(f'Running animation {num}')
                    run(both_led_strips, animation)
                    time.sleep(ms_to_s(BETWEEN_ITERATIONS))

            else:
                try:
                    print(f'Looking for animation {cmd}.')
                    animation = animatetools.animations[int(cmd)]
                    print(f'Running animation {cmd}')
                    run(both_led_strips, animation)
                    time.sleep(ms_to_s(BETWEEN_ITERATIONS))
                except:
                    print('Invalid animation number')

    else:
        while True:
            moving = GPIO.input(MOTION_SENSOR_PIN)

            if moving:
                print('Motion detected')

                animation = random.choice(list(animatetools.animations.values()))
                run(both_led_strips, animation)
                time.sleep(ms_to_s(BETWEEN_ITERATIONS))
            else:
                print('No motion')

                result = temp_humidity_sensor.read()

                if result.is_valid():
                    last_humidity = result.humidity
                    last_temperature = result.temperature
                    print(f'Humidity: {last_humidity} & temperature: {last_temperature}')

                temperature_leds.monochrome_pixels(temperature_scale.choose(int(last_temperature)))
                update([temperature_leds])

                humidity_leds.monochrome_pixels(humidity_scale.choose(int(last_humidity)))
                update([humidity_leds])

                time.sleep(ms_to_s(BETWEEN_ITERATIONS))

