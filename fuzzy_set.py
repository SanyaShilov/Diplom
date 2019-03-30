import bisect
import collections
import functools
import itertools

from const import *
from range import Range


@functools.total_ordering
class FuzzyElement:
    def __init__(self, x, p):
        self.x = x
        self.p = p

    def __eq__(self, other):
        return self.x == other.x

    def __gt__(self, other):
        return self.x > other.x

    def __repr__(self):
        return '{}/{}'.format(self.x, self.p)

    def copy(self):
        return FuzzyElement(self.x, self.p)


def interpolate(elements):
    elements = [FuzzyElement(el.x, round(el.p, DIGITS)) for el in elements]
    last_element = elements[0]
    elements_to_interpolate = []
    for element in elements:
        if element.p == last_element.p:
            elements_to_interpolate.append(element)
        else:
            c = (element.p - last_element.p) / (element.x - last_element.x)
            for el in elements_to_interpolate:
                el.p += c * (el.x - last_element.x)
            elements_to_interpolate = []
            last_element = element
    return elements


def binary_operation(func):
    @functools.wraps(func)
    def wrapped(self: 'FuzzySet', other: 'FuzzySet'):
        values = set(itertools.chain(self.values(), other.values()))
        f = self.f
        other_f = other.f
        return func(self, values, f, other_f)
    return wrapped


class FuzzySet:
    def __init__(self, elements, f=None):
        self.f = f
        self.lst = []
        for x in elements:
            self.add(x)

    def __repr__(self):
        return repr(self.lst)

    def __iter__(self):
        return iter(self.lst)

    def __bool__(self):
        return bool(self.lst)

    def __len__(self):
        return len(self.lst)

    def __getitem__(self, item):
        return self.lst[item]

    def __setitem__(self, key, value):
        self.lst[key] = value

    def __reversed__(self):
        return reversed(self.lst)

    def add(self, element):
        if self.f:
            if isinstance(element, FuzzyElement):
                if abs(self.f(element.x) != element.p) > EPS:
                    raise RuntimeError(
                        'Error while adding fuzzy element '
                        'into set with function'
                    )
            else:
                element = FuzzyElement(element, self.f(element))
        else:
            if not isinstance(element, FuzzyElement):
                raise RuntimeError(
                    'Adding not fuzzy element into set without function'
                )
        index = bisect.bisect_left(self, element)
        if index < len(self) and self[index].x == element.x:
            self[index] = element
        else:
            self.lst.insert(index, element)

    def values(self):
        return (element.x for element in self)

    def probabilities(self):
        return (element.p for element in self)

    def height(self):
        return max(self.probabilities())

    def is_normal(self):
        return self.height() >= 1 - EPS

    def is_subnormal(self):
        return not self.is_normal()

    def normalized(self):
        height = self.height()
        f = self.f
        if not f:
            return FuzzySet((FuzzyElement(element.x, element.p / height) for element in self))
        return FuzzySet(self.values(), lambda x: f(x) / height)

    def defuzzification_centroid(self):
        return (
            sum(element.x * element.p for element in self) /
            sum(element.p for element in self)
        )

    def supp(self):
        return self.alpha_section(EPS)

    def core(self):
        return self.alpha_section(1 - EPS)

    def alpha_section(self, alpha):
        return [element.x for element in self if element.p >= alpha]

    def is_empty(self):
        return not self

    def is_convex(self):
        if not self:
            return True
        up = True
        tmp = self[0].p
        for element in self:
            nxt = element.p
            if nxt > tmp:
                if not up:
                    return False
            elif nxt < tmp:
                up = False
            tmp = nxt
        return True

    def complement(self):
        f = self.f
        if not f:
            return FuzzySet((FuzzyElement(element.x, 1 - element.p) for element in self))
        return FuzzySet(self.values(), lambda x: 1 - f(x))

    @binary_operation
    def intersection_min(self, values, f, other_f):
        return FuzzySet(values, lambda x: min(f(x), other_f(x)))

    @binary_operation
    def intersection_mult(self, values, f, other_f):
        return FuzzySet(values, lambda x: f(x) * other_f(x))

    @binary_operation
    def intersection_lucasevich(self, values, f, other_f):
        return FuzzySet(values, lambda x: max(f(x) + other_f(x) - 1, 0))

    @binary_operation
    def union_max(self, values, f, other_f):
        return FuzzySet(values, lambda x: max(f(x), other_f(x)))

    @binary_operation
    def union_or(self, values, f, other_f):
        return FuzzySet(values, lambda x: f(x) + other_f(x) - f(x) * other_f(x))

    @binary_operation
    def union_lucasevich(self, values, f, other_f):
        return FuzzySet(values, lambda x: min(f(x) + other_f(x), 1))

    def discretization(self, k):
        if self.f:
            return FuzzySet(Range(self[0].x, self[-1].x, n=k), self.f)
        step = (len(self) - 1) // (k - 1)
        return FuzzySet((element.copy() for element in self[::step]))

    def upper_circumflex(self):
        forward = []
        p = self[0].p
        for element in self:
            if element.p >= p:
                forward.append(element.copy())
                p = element.p
            else:
                forward.append(FuzzyElement(element.x, p))
        forward = interpolate(forward)
        backward = []
        p = self[-1].p
        for element in reversed(self):
            if element.p >= p:
                backward.append(element.copy())
                p = element.p
            else:
                backward.append(FuzzyElement(element.x, p))
        backward = interpolate(backward)
        backward.reverse()
        return FuzzySet(
            (
                min(element1, element2, key=lambda element: element.p)
                for element1, element2 in zip(forward, backward)
            )
        )

    @staticmethod
    def generalization_zade(*fsets, f, k):
        new = collections.defaultdict(float)
        for elements in itertools.product(
                *(fs.discretization(k) for fs in fsets)
        ):
            x = f(*(element.x for element in elements))
            p = min((element.p for element in elements))
            new[x] = max(new[x], p)
        result = FuzzySet((FuzzyElement(x, p) for x, p in new.items()))
        return result.upper_circumflex()

    @staticmethod
    def generalization_alpha(*fsets, f, k):
        new = collections.defaultdict(float)
        r = Range(0, 1, n=k)
        for alpha in r:
            alpha_sections = [fs.alpha_section(alpha) for fs in fsets]
            products = list(itertools.product(*alpha_sections))
            f_list = [f(*pr) for pr in products]
            ymin, ymax = min(f_list), max(f_list)
            new[ymin] = alpha
            new[ymax] = alpha
        return FuzzySet((FuzzyElement(x, p) for x, p in new.items()))
