import bisect
import collections
import itertools

from utils.const import *
from fuzzy_logic.fuzzy_element import FuzzyElement
from utils.range import Range


def binary_operation(func):
    def wrapped(self: 'FuzzySet', other: 'FuzzySet'):
        values = set(itertools.chain(self.values, other.values))
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
        self.values = [element.x for element in self]
        self.probabilities = [element.p for element in self]
        self.height = max(self.probabilities)

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
        return self.values, self.probabilities

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

    def is_normal(self):
        """Является ли множество нормальным"""
        return self.height >= 1 - EPS

    def is_subnormal(self):
        """Является ли множество субнормальным"""
        return not self.is_normal()

    def normalized(self):
        """Нормализованное множество"""
        f = self.f
        if not f:
            return self.cls(
                (FuzzyElement(element.x, element.p / self.height)
                 for element in self)
            )
        return self.cls(self.values, lambda x: f(x) / self.height)

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
        return self.cls(self.values, lambda x: 1 - f(x))

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
        forward = FuzzyElement.interpolate(forward)
        backward = []
        p = self[-1].p
        for element in reversed(self):
            if element.p >= p:
                backward.append(element.copy())
                p = element.p
            else:
                backward.append(FuzzyElement(element.x, p))
        backward = FuzzyElement.interpolate(backward)
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

    def construct_relation(self, other):
        from fuzzy_logic.fuzzy_relation import FuzzyRelation
        return FuzzyRelation(
            ((x, y) for x in self.values for y in other.values),
            lambda t: min(self.f(t[0]), other.f(t[1]))
        ) if self.f and other.f else FuzzyRelation(
            (FuzzyElement((el1.x, el2.x), min(el1.p, el2.p))
             for el1 in self for el2 in other)
        )

    def as_relation(self):
        from fuzzy_logic.fuzzy_relation import FuzzyRelation
        return FuzzyRelation(
            (FuzzyElement((0, el.x), el.p) for el in self),
            lambda t: self.f(t[1]) if self.f else None
        )

    def composition_zade(self, rel):
        """Композиционное правило нечеткого вывода Заде"""
        # TODO: optimize?
        return self.as_relation().composition_max_min(rel).as_set()
