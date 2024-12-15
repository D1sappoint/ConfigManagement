import operator
from parser import Program, ConstDeclaration, ArrayLiteral, DictLiteral, ConstExpression, VariableReference
class Evaluator:
    def __init__(self):
        self.variables = {}

    def evaluate(self, node):
        if isinstance(node, Program):
            return self.eval_program(node)
        else:
            raise Exception(f"Unknown node type: {type(node)}")

    def eval_program(self, program):
        for stmt in program.statements:
            if isinstance(stmt, ConstDeclaration):
                value = self.eval_value(stmt.value)
                self.variables[stmt.name] = value
            else:
                raise Exception(f"Unknown statement type: {type(stmt)}")
        return self.variables

    def eval_value(self, val):
        if isinstance(val, (int, float, str)):
            return val
        elif isinstance(val, ArrayLiteral):
            return [self.eval_value(elem) for elem in val.elements]
        elif isinstance(val, DictLiteral):
            return {key: self.eval_value(value) for key, value in val.pairs}
        elif isinstance(val, ConstExpression):
            return self.eval_const_expression(val)
        elif isinstance(val, VariableReference):
            if val.name in self.variables:
                return self.variables[val.name]
            else:
                raise Exception(f"Undefined variable '{val.name}'")
        else:
            raise Exception(f"Unsupported value type: {type(val)}")
    def eval_const_expression(self, expr):
        ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            'sort': sorted
        }
        if expr.operator in ops:
            func = ops[expr.operator]
            operands = [self.eval_value(op) for op in expr.operands]
            try:
                return func(*operands)
            except Exception as e:
                raise Exception(f"Error evaluating expression: {e}")
        else:
            raise Exception(f"Unknown operator: {expr.operator}")

    def to_toml(self, data):
        import toml
        return toml.dumps(data)