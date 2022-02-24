import colour
from math import ceil


def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.

    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)



def rainbow(min_length, colors):
    segment = ceil(min_length / len(colors))
    # In cases where the colors don't divide perfectly into the strip, this
    # will be larger than the strip itself!
    elements = []

    for i in range(segment * len(colors)):
        current_segment = i // segment
        current_color = colors[current_segment]
        elements.append(current_color)

    return elements



def gradient(length, from_color, to_color):
    scale = Scale([(from_color, 0), (to_color, length - 1)])
    return scale.between(0, length - 1)



class Scale:
    """ stops: ( red, 5 ), ( orange, 11 ), ( yellow, 16 ), ( green, 22 ) """
    def __init__(self, stops):
        self.stops = sorted(stops, key=lambda tup: tup[1])

    def choose(self, num):
        lower_bound = first_true(reversed(self.stops), default=None, pred=lambda tup: num >= tup[1])
        upper_bound = first_true(self.stops, default=None, pred=lambda tup: num <= tup[1])

        if lower_bound is not None and upper_bound is not None:
            if lower_bound[1] == upper_bound[1]:
                return lower_bound[0]

            else:
                # print(f'upper bound: {upper_bound}, lower_bound: {lower_bound}')
                mult = (num - lower_bound[1]) / (upper_bound[1] - lower_bound[1])
                red = lower_bound[0].red + (mult * (upper_bound[0].red - lower_bound[0].red))
                green = lower_bound[0].green + (mult * (upper_bound[0].green - lower_bound[0].green))
                blue = lower_bound[0].blue + (mult * (upper_bound[0].blue - lower_bound[0].blue))
                return colour.Color(rgb=(red, green, blue))

        elif lower_bound:
            return lower_bound[0]

        elif upper_bound:
            return upper_bound[0]

        else:
            print(f'Error finding a colour for stop {num}')
            return RED # Error

    def between(self, begin_num, end_num):
        all_colors = []

        for num in range(begin_num, end_num + 1):
            all_colors.append(self.choose(num))

        return all_colors






