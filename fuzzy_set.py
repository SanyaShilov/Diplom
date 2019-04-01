import bisect
import collections
import functools
import itertools

from const import *
from range import Range


@functools.total_ordering
class FuzzyElement:
    """
    Элемент нечеткого множества
    """
    # TODO: move to fuzzy_element.py
    def __init__(self, x, p):
        """
        :param x: значение элемента
        :param p: степень принадлежности элемента нечеткому множеству
        """
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
    """
    Часть создания верхней огибающей в принципе нечеткого обобщения Заде -
    устранение ступенчатости
    """
    # TODO: staticmethod of FuzzyElement
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
        return self.cls(values, lambda x: func(self, self.f, other.f, x))
    return wrapped


class FuzzySet:
    """
    Нечеткое множество.
    Реализовано на основе списка нечетких элементов, отсортированного по
    возрастанию значения элемента.
    """
    def __init__(self, elements, f=None):
        """
        :param elements: список элементов множества
        :param f: функция принадлежности, None для дискретных множеств
        """
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

    @property
    def cls(self):
        return self.__class__

    def plot(self):
        return list(self.values()), list(self.probabilities())

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
        """Последовательность значений элементов множества"""
        return (element.x for element in self)

    def probabilities(self):
        """Последовательность степеней принадлежностей элементов множества"""
        return (element.p for element in self)

    def height(self):
        """Высота множества"""
        return max(self.probabilities())

    def is_normal(self):
        """Является ли множество нормальным"""
        return self.height() >= 1 - EPS

    def is_subnormal(self):
        """Является ли множество субнормальным"""
        return not self.is_normal()

    def normalized(self):
        """Нормализованное множество"""
        height = self.height()
        f = self.f
        if not f:
            return self.cls(
                (FuzzyElement(element.x, element.p / height)
                 for element in self)
            )
        return self.cls(self.values(), lambda x: f(x) / height)

    def supp(self):
        """Носитель множества"""
        return self.alpha_section(EPS)

    def core(self):
        """Ядро множества"""
        return self.alpha_section(1 - EPS)

    def alpha_section(self, alpha):
        """альфа-сечение множества"""
        return [element.x for element in self if element.p >= alpha]

    def is_empty(self):
        """Является ли множество пустым"""
        return not self.supp()

    def is_convex(self):
        """Является ли множество выпуклым"""
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

    def defuzzification_centroid(self):
        """Дефаззификация методом центра тяжести"""
        return (
            sum(element.x * element.p for element in self) /
            sum(element.p for element in self)
        )

    def complement(self):
        """Дополнение множества"""
        f = self.f
        if not f:
            return self.cls(
                (FuzzyElement(element.x, 1 - element.p) for element in self)
            )
        return self.cls(self.values(), lambda x: 1 - f(x))

    @binary_operation
    def intersection_min(self, f1, f2, x):
        return min(f1(x), f2(x))

    @binary_operation
    def intersection_mult(self, f1, f2, x):
        return f1(x) * f2(x)

    @binary_operation
    def intersection_lucasevich(self, f1, f2, x):
        return max(f1(x) + f2(x) - 1, 0)

    @binary_operation
    def union_max(self, f1, f2, x):
        return max(f1(x), f2(x))

    @binary_operation
    def union_or(self, f1, f2, x):
        return f1(x) + f2(x) - f1(x) * f2(x)

    @binary_operation
    def union_lucasevich(self, f1, f2, x):
        return min(f1(x) + f2(x), 1)

    def discretization(self, k):
        """
        Дискретизация нечеткого множества
        :param k: количество дискрет > 1
        :return: нечеткое множество с k элементами
        """
        # TODO: need to override in FuzzyRelation?
        if self.f:
            return FuzzySet(Range(self[0].x, self[-1].x, n=k), self.f)
        step = (len(self) - 1) // (k - 1)
        return FuzzySet((element.copy() for element in self[::step]))

    def upper_circumflex(self):
        """Построение верхней огибающей в принципе нечеткого обобщения Заде"""
        # TODO: need to override in FuzzyRelation?
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
        """Принцип нечеткого обобщения Заде"""
        # TODO: need to override in FuzzyRelation?
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
        """альфа-уровневый принцип обобщения"""
        # TODO: need to override in FuzzyRelation?
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
