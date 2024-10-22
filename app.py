from flask import Flask, request, jsonify
from rule_engine import RuleEngine
from database import initialize_db, insert_rule, fetch_rules

app = Flask(__name__)
engine = RuleEngine()

initialize_db()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Rule Engine API!"})

@app.route('/create_rule', methods=['POST'])
def create_rule():
    if not request.json or 'rule' not in request.json:
        return jsonify({"error": "Missing 'rule' key in JSON"}), 400

    rule_string = request.json['rule']
    try:
        ast = engine.create_rule(rule_string)
        insert_rule(rule_string)
        return jsonify({"message": "Rule created successfully", "ast": repr(ast)}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json.get('data', {})
    rules = fetch_rules()
    combined_ast = engine.combine_rules(rules)
    result = engine.evaluate_rule(combined_ast, data)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
