from utils.const import *


DEFAULT_N = 101


class Range:
    def __init__(self, a, b, *, n=None, h=None, include_b=True):
        self.a = a
        if h:
            if n:
                raise RuntimeError('Can\'t construct Range from both n and h')
            self.h = h
            self.n = int((b - a) / h) + include_b
        else:
            self.n = n or DEFAULT_N
            self.h = (b - a) / (self.n - include_b)

    def __iter__(self):
        return (round(self.a + i * self.h, DIGITS) for i in range(self.n))

    def closest(self, num):
        return self.a + ((num - self.a) // self.h) * self.h
