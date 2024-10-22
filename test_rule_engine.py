import unittest
from rule_engine import RuleEngine

class TestRuleEngine(unittest.TestCase):
    def setUp(self):
        self.engine = RuleEngine()

    def test_create_rule(self):
        rule_string = "age > 30 AND department = 'Sales'"
        ast = self.engine.create_rule(rule_string)
        print(f"AST for rule '{rule_string}': {ast}")
        self.assertIsNotNone(ast)

    def test_combine_rules(self):
        rules = ["age > 30 AND department = 'Sales'", "age < 25 AND department = 'Marketing'"]
        combined_ast = self.engine.combine_rules(rules)
        self.assertIsNotNone(combined_ast)

    def test_evaluate_rule(self):
        rule_string = "age > 30 AND department = 'Sales'"
        ast = self.engine.create_rule(rule_string)
        data = {"age": 35, "department": "Sales"}
        result = self.engine.evaluate_rule(ast, data)
        self.assertTrue(result)

    def test_invalid_rule(self):
        with self.assertRaises(ValueError):
            self.engine.create_rule("invalid_rule")

    def test_evaluate_invalid_data(self):
        rule_string = "age > 30 AND department = 'Sales'"
        ast = self.engine.create_rule(rule_string)
        data = {"age": 35}  # Missing 'department'
        with self.assertRaises(KeyError):
            self.engine.evaluate_rule(ast, data)

if __name__ == '__main__':
    unittest.main()
