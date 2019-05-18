class FuzzyBase:
    def __init__(self, rules):
        self.rules = rules

    def evaluate(self, inputs):
        rules_evaluation = [rule.evaluate(inputs) for rule in self.rules]
        result = rules_evaluation[0]
        for rule_evaluation in rules_evaluation[1:]:
            result = result.union_max(rule_evaluation)
        return result.defuzzification_centroid()
