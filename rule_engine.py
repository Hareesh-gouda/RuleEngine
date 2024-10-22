import json
from rule_ast import Node

class RuleEngine:
    def create_rule(self, rule_string):
        try:
            return self._parse_rule(rule_string)
        except Exception as e:
            raise ValueError(f"Error parsing rule: {e}")

    def _parse_rule(self, rule_string):
        rule_string = rule_string.strip()
        if "AND" in rule_string:
            left, right = rule_string.split(" AND ", 1)
            return Node("operator", "AND", self._parse_rule(left.strip()), self._parse_rule(right.strip()))
        elif "OR" in rule_string:
            left, right = rule_string.split(" OR ", 1)
            return Node("operator", "OR", self._parse_rule(left.strip()), self._parse_rule(right.strip()))
        else:
            if not self._is_valid_operand(rule_string):
                raise ValueError(f"Invalid operand: {rule_string}")
            return Node("operand", rule_string.strip())

    def _is_valid_operand(self, operand):
        return "=" in operand or ">" in operand or "<" in operand

    def combine_rules(self, rules):
        combined = None
        for rule in rules:
            if combined is None:
                combined = self.create_rule(rule)
            else:
                combined = Node("operator", "OR", combined, self.create_rule(rule))
        return combined

    def evaluate_rule(self, ast, data):
        if ast.type == "operand":
            return self._evaluate_condition(ast.value, data)
        elif ast.type == "operator":
            if ast.value == "AND":
                return self.evaluate_rule(ast.left, data) and self.evaluate_rule(ast.right, data)
            elif ast.value == "OR":
                return self.evaluate_rule(ast.left, data) or self.evaluate_rule(ast.right, data)

    def _evaluate_condition(self, condition, data):
        # Handle different types of conditions
        if ">" in condition:
            left, right = condition.split(">", 1)
            left_key = left.strip()
            if left_key not in data:
                raise KeyError(f"Key '{left_key}' not found in data.")
            return data[left_key] > self._parse_value(right.strip())
        elif "<" in condition:
            left, right = condition.split("<", 1)
            left_key = left.strip()
            if left_key not in data:
                raise KeyError(f"Key '{left_key}' not found in data.")
            return data[left_key] < self._parse_value(right.strip())
        elif "=" in condition:
            left, right = condition.split("=", 1)
            left_key = left.strip()
            if left_key not in data:
                raise KeyError(f"Key '{left_key}' not found in data.")
            return data[left_key] == self._parse_value(right.strip())
        else:
            raise ValueError(f"Invalid condition: {condition}")

    def _parse_value(self, value):
        value = value.strip()
        if value.isdigit():
            return int(value)
        elif value.replace('.', '', 1).isdigit():
            return float(value)
        elif value.startswith("'") and value.endswith("'"):
            return value[1:-1]  # remove quotes
        raise ValueError(f"Invalid value: {value}")
