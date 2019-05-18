from math import sin

import numpy as np
from mpl_toolkits.mplot3d import axes3d
from matplotlib import pyplot as plt

from fuzzy_logic import *


f = lambda x1, x2: x1 ** 2 * sin(x2 - 1)

r_x1 = Range(-7, 3, n=20)
r_x2 = Range(-4.4, 1.7, n=20)
r_y = Range(-49, 49, n=20)

x = [[x1 for x1 in r_x1] for x2 in r_x2]
y = [[x2 for x1 in r_x1] for x2 in r_x2]
z = np.array([[f(x1, x2) for x1 in r_x1] for x2 in r_x2])


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(x, y, z)
plt.show()

f_x1_low = gaussian(-7, 1.5)
f_x1_middle = gaussian(-2, 1.5)
f_x1_high = gaussian(3, 1.5)


f_x2_low = gaussian(-4.4, 1)
f_x2_middle = gaussian(-1.35, 1)
f_x2_high = gaussian(1.7, 1)


f_y_low = gaussian(-49, 7)
f_y_below_middle = gaussian(-25, 7)
f_y_middle = gaussian(0, 7)
f_y_above_middle = gaussian(25, 7)
f_y_high = gaussian(49, 7)


base = FuzzyBase.from_parameters(
    conditions_ranges=[r_x1, r_x2],
    conclusion_range=r_y,
    rules_parameters=[
        {
            'conditions': [f_x1_low, f_x2_low],
            'conclusion': f_very(f_y_high)
        },
        {
            'conditions': [f_x1_low, f_x2_middle],
            'conclusion': f_very(f_y_low)
        },
        {
            'conditions': [f_x1_low, f_x2_high],
            'conclusion': f_more_or_less(f_y_high)
        },
        {
            'conditions': [f_x1_middle, None],
            'conclusion': f_y_middle
        },
        {
            'conditions': [f_x1_high, f_x2_low],
            'conclusion': f_y_above_middle
        },
        {
            'conditions': [f_x1_high, f_x2_middle],
            'conclusion': f_y_below_middle
        },
        {
            'conditions': [f_x1_high, f_x2_high],
            'conclusion': f_y_above_middle
        },
    ],
)

s_x1 = [FuzzySet(r_x1, singleton(x1)) for x1 in r_x1]
s_x2 = [FuzzySet(r_x2, singleton(x2)) for x2 in r_x2]
z = np.array([[base.evaluate([x1, x2]) for x1 in s_x1] for x2 in s_x2])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(x, y, z)
plt.show()
