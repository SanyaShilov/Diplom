from fuzzy_logic.fuzzy_set import FuzzySet


class FuzzyRule:
    def __init__(self, conditions, conclusion, weight=1):
        self.conditions = conditions
        self.conclusion = conclusion
        self.weight = weight

    def truth(self, inputs):
        result = self.weight
        for input, condition in zip(inputs, self.conditions):
            if condition:
                if isinstance(input, FuzzySet):
                    height = condition.intersection_min(input).height
                else:
                    height = condition.intersection_singleton(input)
                result *= height
        return result

    def evaluate(self, inputs):
        truth = self.truth(inputs)
        result = FuzzySet(
            self.conclusion.values,
            lambda x: min(truth, self.conclusion.f(x))
        )
        return result
