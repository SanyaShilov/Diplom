from fuzzy_logic import *


r_distance = Range(0, 30 * (2 ** 0.5))

dis_small = gaussian(0, 0.8)
dis_middle = gaussian(2.5, 0.8)
dis_big = f_or(gaussian(5, 0.8), lambda x: 1 if x >= 5 else 0)


r_degree = Range(0, 180)

deg_small = gaussian(0, 7.5)
deg_middle = gaussian(22.5, 7.5)
deg_big = f_or(gaussian(45, 7.5), lambda x: 1 if x >= 45 else 0)


r_heuristic = Range(0, 1)

heur_small = gaussian(0, 0.2)
heur_middle = gaussian(0.5, 0.2)
heur_big = gaussian(1, 0.2)


base = FuzzyBase.from_parameters(
    condition_ranges=[r_distance, r_degree],
    conclusion_range=r_heuristic,
    rules_parameters=[
        {
            'conditions': [dis_big, None],
            'conclusion': heur_small
        },
        {
            'conditions': [None, deg_big],
            'conclusion': heur_small
        },
        {
            'conditions': [dis_middle, deg_small],
            'conclusion': heur_middle
        },
        {
            'conditions': [dis_middle, deg_middle],
            'conclusion': heur_small
        },
        {
            'conditions': [dis_small, deg_small],
            'conclusion': heur_big
        },
        {
            'conditions': [dis_small, deg_middle],
            'conclusion': heur_middle
        },
    ],
)
