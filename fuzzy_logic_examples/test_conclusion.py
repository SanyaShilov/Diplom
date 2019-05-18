from matplotlib import pyplot as plt

from fuzzy_logic import *


r_18_80 = Range(18, 80, h=0.5)
r_0_1 = Range(0, 1)

f_young = lambda x: 1 / (1 + ((x - 18) / 8) ** 8)
f_middle = gaussian(40, 9)
f_old = lambda x: 1 / (1 + (abs(x - 90) / 28) ** 8)

f_very_old = f_very(f_old)

f_low = lambda x: lie_zade(x, 0.2)
f_high = lambda x: truth_zade(x, 0.2)

for func in [
    f_young, f_middle, f_old, f_very_old
]:
    fs = FuzzySet(r_18_80, func)
    plt.plot(*fs.plot())
plt.grid(True)
plt.show()

for func in [
    f_low, f_high
]:
    fs = FuzzySet(r_0_1, func)
    plt.plot(*fs.plot())
plt.grid(True)
plt.show()

input_28 = FuzzySet(r_18_80, singleton(28))
input_40 = FuzzySet(r_18_80, singleton(40))
input_young = FuzzySet(r_18_80, f_young)
input_middle = FuzzySet(r_18_80, f_middle)
input_old = FuzzySet(r_18_80, f_old)
input_very_old = FuzzySet(r_18_80, f_very_old)

base = FuzzyBase.from_parameters(
    conditions_ranges=[r_18_80],
    conclusion_range=r_0_1,
    rules_parameters=[
        {
            'conditions': [f_young],
            'conclusion': f_high
        },
        {
            'conditions': [f_middle],
            'conclusion': f_low
        },
        {
            'conditions': [f_old],
            'conclusion': f_high
        },
    ],
)

for input in [
    input_28, input_40, input_young, input_middle, input_old, input_very_old
]:
    print(base.evaluate([input]))
