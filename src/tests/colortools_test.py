import colortools

import unittest
import colour


class TestRainbow(unittest.TestCase):
    def test_rainbow(self):
        rainbow = colortools.rainbow(6, [colour.Color("red"), colour.Color("blue"), colour.Color("green")])
        self.assertEqual(rainbow, [colour.Color("red"), colour.Color("red"), colour.Color("blue"), colour.Color("blue"), colour.Color("green"), colour.Color("green")])

    def test_longer_rainbow(self):
        rainbow = colortools.rainbow(4, [colour.Color("red"), colour.Color("blue"), colour.Color("green")])
        self.assertEqual(rainbow, [colour.Color("red"), colour.Color("red"), colour.Color("blue"), colour.Color("blue"), colour.Color("green"), colour.Color("green")])



class TestGradient(unittest.TestCase):
    def test_gradient(self):
        gradient = colortools.gradient(4, colour.Color("purple"), colour.Color("black"))
        self.assertEqual(gradient, [colour.Color("purple"), colour.Color("#505"), colour.Color("#2b002b"), colour.Color("black")])



class TestSimpleColorScale(unittest.TestCase):
    scale = colortools.Scale([ ( colour.Color("red"), 0 ), ( colour.Color("blue"), 4 ) ])

    def test_below_lower_bound(self):
        self.assertEqual(self.scale.choose(-2), colour.Color("red"))

    def test_above_upper_bound(self):
        self.assertEqual(self.scale.choose(20), colour.Color("blue"))

    def test_on_lower_bound(self):
        self.assertEqual(self.scale.choose(0), colour.Color("red"))

    def test_on_middle_values1(self):
        self.assertEqual(self.scale.choose(1), colour.Color("#BF0040"))

    def test_on_middle_values2(self):
        self.assertEqual(self.scale.choose(2), colour.Color("#7F007F"))

    def test_on_middle_values3(self):
        self.assertEqual(self.scale.choose(3), colour.Color("#4000BF"))

    def test_on_upper_bound(self):
        self.assertEqual(self.scale.choose(4), colour.Color("blue"))

    # def test_full_scale(self):
    #     hexes = list(map(lambda col: col.hex, self.scale.between(0, 4)))
    #     print(hexes)
    #     self.assertEqual(hexes, [])


class TestSmallColorScale(unittest.TestCase):
    scale = colortools.Scale([ ( colour.Color("red"), 0 ), ( colour.Color("blue"), 2 ) ])

    def test_on_lower_bound(self):
        self.assertEqual(self.scale.choose(0), colour.Color("red"))

    def test_on_middle(self):
        self.assertEqual(self.scale.choose(1), colour.Color("#7f007f"))

    def test_on_upper_bound(self):
        self.assertEqual(self.scale.choose(2), colour.Color("blue"))

    # def test_full_scale(self):
    #     hexes = list(map(lambda col: col.hex, self.scale.between(0, 2)))
    #     print(hexes)
    #     self.assertEqual(hexes, [])


# https://thomasin.github.io/palette/%23f00%2C%23ff5200%2C%23ffa500%2C%23ffd200%2C%23ff0%2C%237fbf00%2C%23008000
class TestMultiStopColorScale(unittest.TestCase):
    scale = colortools.Scale([ ( colour.Color("#ff0000"), 0 ), ( colour.Color("#ffa500"), 2 ), ( colour.Color("#ffff00"), 4 ), ( colour.Color("#008000"), 6 ) ])

    def test_on_lower_bound(self):
        self.assertEqual(self.scale.choose(0), colour.Color("#ff0000"))

    def test_on_middle1(self):
        self.assertEqual(self.scale.choose(1), colour.Color("#FF5200"))

    def test_on_middle2(self):
        self.assertEqual(self.scale.choose(2), colour.Color("#ffa500"))

    def test_on_middle3(self):
        self.assertEqual(self.scale.choose(3), colour.Color("#FFD200"))

    def test_on_middle4(self):
        self.assertEqual(self.scale.choose(4), colour.Color("#ffff00"))

    def test_on_middle5(self):
        self.assertEqual(self.scale.choose(5), colour.Color("#7FBF00"))

    def test_on_upper_bound(self):
        self.assertEqual(self.scale.choose(6), colour.Color("#008000"))

    # def test_full_scale(self):
    #     hexes = list(map(lambda col: col.hex, self.scale.between(0, 6)))
    #     print(hexes)
    #     self.assertEqual(hexes, [])


# https://thomasin.github.io/palette/%23f00%2C%23ff1b00%2C%23ff3700%2C%23ff5200%2C%23ff6e00%2C%23ff8900%2C%23ffa500%2C%23ffb700%2C%23ffc900%2C%23ffdb00%2C%23ffed00%2C%23ff0%2C%23eaf400%2C%23d4ea00%2C%23bfdf00%2C%23aad500%2C%2395ca00%2C%237fbf00%2C%236ab500%2C%235a0%2C%2340a000%2C%232a9500%2C%23158b00%2C%23008000
class TestHumidityScale(unittest.TestCase):
    scale = colortools.Scale([ ( colour.Color("red"), 50 ), ( colour.Color("orange"), 56 ), ( colour.Color("yellow"), 61 ), ( colour.Color("green"), 73 ) ])

    def test_on_lower_bound(self):
        self.assertEqual(self.scale.choose(50), colour.Color("red"))

    def test_on_upper_bound(self):
        self.assertEqual(self.scale.choose(73), colour.Color("green"))

    # def test_full_scale(self):
    #     hexes = list(map(lambda col: col.hex, self.scale.between(50, 73)))
    #     print(hexes)
    #     self.assertEqual(hexes, [])


# https://thomasin.github.io/palette/%23f00%2C%23ff1b00%2C%23ff3700%2C%23ff5200%2C%23ff6e00%2C%23ff8900%2C%23ffa500%2C%23ffb700%2C%23ffc900%2C%23ffdb00%2C%23ffed00%2C%23ff0%2C%23d4ea00%2C%23aad500%2C%237fbf00%2C%235a0%2C%232a9500%2C%23008000
class TestTempScale(unittest.TestCase):
    scale = colortools.Scale([ ( colour.Color("red"), 5 ), ( colour.Color("orange"), 11 ), ( colour.Color("yellow"), 16 ), ( colour.Color("green"), 22 ) ])

    def test_on_lower_bound(self):
        self.assertEqual(self.scale.choose(0), colour.Color("red"))

    def test_on_upper_bound(self):
        self.assertEqual(self.scale.choose(22), colour.Color("green"))

    # def test_full_scale(self):
    #     hexes = list(map(lambda col: col.hex, self.scale.between(5, 22)))
    #     print(hexes)
    #     self.assertEqual(hexes, [])


if __name__ == '__main__':
    unittest.main()

