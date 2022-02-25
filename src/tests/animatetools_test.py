import ledtools
import colortools
import animatetools

import unittest
import colour
import itertools



# Really just testing that none of them have any program killing bugs
class TestAnimations(unittest.TestCase):
    def test_all_animations(self):
        leds = ledtools.Strip(None, 6, colour.Color("blue"), 255)

        for num, animation in animatetools.animations.items():
            try:
                for _ in animation(leds):
                    continue
            except:
                self.fail(f'Error running animation {num}')

    def test_specific(self):
        leds = ledtools.Strip(None, 6, colour.Color("blue"), 255)
        animation = animatetools.animations[142]

        for _ in animation(leds):
            continue




if __name__ == '__main__':
    unittest.main()

