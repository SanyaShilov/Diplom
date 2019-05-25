from fuzzy_logic.fuzzy_rule import FuzzyRule
from fuzzy_logic.fuzzy_set import FuzzySet


class FuzzyBase:
    def __init__(self, rules):
        self.rules = rules

    @classmethod
    def from_parameters(cls, condition_ranges, conclusion_range, rules_parameters):
        return cls(
            [
                FuzzyRule(
                    [
                        FuzzySet(condition_range, condition)
                        if condition else None
                        for condition_range, condition
                        in zip(condition_ranges, rule_parameters['conditions'])
                    ],
                    FuzzySet(conclusion_range, rule_parameters['conclusion'])
                )
                for rule_parameters in rules_parameters
            ]
        )

    def evaluate(self, inputs):
        rules_evaluation = [rule.evaluate(inputs) for rule in self.rules]
        result = rules_evaluation[0]
        for rule_evaluation in rules_evaluation[1:]:
            result = result.union_max(rule_evaluation)
        return result.defuzzification_centroid()
