import ledtools
import colortools
import animatetools

import unittest
import colour
import itertools


# Really just testing that none of them have any program killing bugs
class TestAnimations(unittest.TestCase):
    leds = ledtools.Strip(None, 6, colour.Color("blue"), 255)

    def test_all_animations(self):
        for num, animation in animatetools.animations.items():
            try:
                for _ in animation(self.leds):
                    pass
            except:
                self.fail(f'Error running animation {num}')

    def test_specific(self):
        animation = animatetools.animations[112]

        for _ in animation(self.leds):
            pass




if __name__ == '__main__':
    unittest.main()

