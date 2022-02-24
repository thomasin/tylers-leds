import ledtools
import colortools
import animatetools

import unittest
import colour
import itertools


class TestStrips(unittest.TestCase):
    led1 = ledtools.Strip(None, 3, colour.Color("blue"), 255)
    led2 = ledtools.Strip(None, 3, colour.Color("green"), 255)
    both_leds = ledtools.Strips([led1, led2])

    def test_zipping(self):
        def test_wipe(strip):
            pixels = [colour.Color("orange")] * strip.length

            for x in strip.wipe(pixels, 0):
                yield x

            return with_strip

        wipe = self.both_leds.animate(test_wipe)

        self.assertEqual(self.led1.pixels, [colour.Color("blue"), colour.Color("blue"), colour.Color("blue")])
        self.assertEqual(self.led2.pixels, [colour.Color("green"), colour.Color("green"), colour.Color("green")])

        next(wipe)

        self.assertEqual(self.led1.pixels, [colour.Color("orange"), colour.Color("blue"), colour.Color("blue")])
        self.assertEqual(self.led2.pixels, [colour.Color("orange"), colour.Color("green"), colour.Color("green")])

        next(wipe)

        self.assertEqual(self.led1.pixels, [colour.Color("orange"), colour.Color("orange"), colour.Color("blue")])
        self.assertEqual(self.led2.pixels, [colour.Color("orange"), colour.Color("orange"), colour.Color("green")])

        next(wipe)

        self.assertEqual(self.led1.pixels, [colour.Color("orange"), colour.Color("orange"), colour.Color("orange")])
        self.assertEqual(self.led2.pixels, [colour.Color("orange"), colour.Color("orange"), colour.Color("orange")])



class TestStrip(unittest.TestCase):
    leds = ledtools.Strip(None, 6, colour.Color("blue"), 255)

    def test_init(self):
        self.assertEqual(self.leds.pixels, [colour.Color("blue"), colour.Color("blue"), colour.Color("blue"), colour.Color("blue"), colour.Color("blue"), colour.Color("blue")])


class TestCycle(unittest.TestCase):
    def test_initial_setup(self):
        leds = ledtools.Strip(None, 6, colour.Color("blue"), 255)
        cycle = leds.cycle(colortools.Scale([(colour.Color("purple"), 0), (colour.Color("black"), 3)]).between(0, 3), 0)
        next(cycle) # Initial pixel positions

        self.assertEqual(leds.pixels, [colour.Color("purple"), colour.Color("#505"), colour.Color("#2b002b"), colour.Color("black"), colour.Color("purple"), colour.Color("#505")])

    def test_iter1(self):
        leds = ledtools.Strip(None, 6, colour.Color("blue"), 255)
        cycle = leds.cycle(colortools.Scale([(colour.Color("purple"), 0), (colour.Color("black"), 3)]).between(0, 3), 0)
        next(cycle)
        next(cycle)

        self.assertEqual(leds.pixels, [colour.Color("#505"), colour.Color("#2b002b"), colour.Color("black"), colour.Color("purple"), colour.Color("#505"), colour.Color("#2b002b")])

    def test_longer_leds(self):
        leds = ledtools.Strip(None, 6, colour.Color("blue"), 255)
        cycle = leds.cycle(colortools.Scale([(colour.Color("purple"), 0), (colour.Color("black"), 8)]).between(0, 8), 0)
        next(cycle)

        self.assertEqual(leds.pixels, [colour.Color("purple"), colour.Color("#700070"), colour.Color("#600060"), colour.Color("#500050"), colour.Color("#400040"), colour.Color("#300030")])


if __name__ == '__main__':
    unittest.main()

