import functools

from utils.const import *


@functools.total_ordering
class FuzzyElement:
    """
    Элемент нечеткого множества.
    Порядок определяется значениями элементов.
    """
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
        return '{}/{}'.format(self.x, round(self.p, 12))

    def copy(self):
        return FuzzyElement(self.x, self.p)

    @staticmethod
    def interpolate(elements):
        """
        Часть создания верхней огибающей в принципе нечеткого обобщения Заде -
        устранение ступенчатости
        """
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
