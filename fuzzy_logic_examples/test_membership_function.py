from matplotlib import pyplot as plt

from fuzzy_logic import *


r = Range(0, 100, h=1)

triangular = membership_function.triangular(5, 30, 90)
trapezoidal = membership_function.trapezoidal(0, 6, 24, 100)
gaussian = membership_function.gaussian(50, 12)
sigmoid = membership_function.sigmoid(0.2, 70)
singleton = membership_function.singleton(38)

for function in [triangular, trapezoidal, gaussian, sigmoid, singleton]:
    plt.plot(list(r), [function(x) for x in r])

plt.grid(True)
plt.show()
