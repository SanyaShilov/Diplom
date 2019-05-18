from fuzzy_logic import *


# понятие "мужчина среднего роста" в виде нечеткого множества
fs = FuzzySet(
    [
        FuzzyElement(155, 0),
        FuzzyElement(160, 0.1),
        FuzzyElement(165, 0.3),
        FuzzyElement(170, 0.8),
        FuzzyElement(175, 1),
        FuzzyElement(180, 1),
        FuzzyElement(185, 0.5),
        FuzzyElement(190, 0)
    ]
)

print('Нечеткое множество:', fs)
print('Элементы множества:', list(fs.values))
print('Соответствующие вероятности:', list(fs.probabilities))
print('Высота множества:', fs.height)
print('Является нормальным:', fs.is_normal())
print('Носитель множества:', fs.supp())
print('Ядро множества:', fs.core())
print('Альфа-сечение уровня 0.25:', fs.alpha_section(0.25))
print('Является выпуклым:', fs.is_convex())
print('Дефаззификация методом центра тяжести:', fs.defuzzification_centroid())
print('Дополнение множества:', fs.complement())
print(fs.discretization(2))
print(fs.discretization(3))
print(fs.discretization(4))
