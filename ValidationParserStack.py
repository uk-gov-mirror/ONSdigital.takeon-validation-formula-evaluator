import math
import operator


class ValidationParserStack:

    def __init__(self):
        # map operator symbols to corresponding arithmetic operations
        self.opn = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "^": operator.pow}

        self.epsilon = 1e-12
        self.fn = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "exp": math.exp,
            "abs": abs,
            "trunc": lambda a: int(a),
            "round": round,
            "sgn": lambda a: (a > self.epsilon) - (a < -self.epsilon)}

        self.comparison_operator = {
            "<": lambda a, b: a < b,
            ">": lambda a, b: a > b,
            "=": lambda a, b: a == b,
            "LE": lambda a, b: a <= b,
            "GE": lambda a, b: a >= b,
            "!=": lambda a, b: a != b}

        self.logic_operator = {
            "<": lambda a, b: a < b,
            ">": lambda a, b: a > b,
            "=": lambda a, b: a == b,
            "LE": lambda a, b: a <= b,
            "GE": lambda a, b: a >= b,
            "!=": lambda a, b: a != b,
            "AND": lambda a, b: a and b,
            "OR": lambda a, b: a or b}

        self.list_operator = {
            "IN": lambda a, b: a in b,
            "NOTIN": lambda a, b: a not in b}

    @staticmethod
    def is_number(s):

        try:
            float(s)
            # print(s + 'is a number!')
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        # print(s + 'is not a number!')
        return False

    def evaluate(self, s):
        pop_op = s.pop()

        if self.is_number(pop_op):
            op = float(pop_op)
        else:
            op = pop_op

        if op == 'unary -':
            return -self.evaluate(s)

        if op in self.opn:
            op2 = self.evaluate(s)
            op1 = self.evaluate(s)
            return self.opn[op](op1, op2)

        elif op in self.fn:
            return self.fn[op](self.evaluate(s))

        elif op in self.comparison_operator:
            op2 = self.evaluate(s)
            op1 = self.evaluate(s)
            return self.logic_operator[op](op1, op2)

        elif op in self.logic_operator:
            op2 = self.evaluate(s)
            op1 = self.evaluate(s)
            return self.logic_operator[op](op1, op2)

        elif op in self.list_operator:
            op2 = self.evaluate(s)
            op1 = self.evaluate(s)
            comparison_list = []
            for item in str(op2).split(','):
                if self.is_number(item):
                    comparison_list.append(float(item))
                else:
                    comparison_list.append(item)

            # print(op2, 'in', comparison_list)
            return self.list_operator[op](op1, comparison_list)
        elif str(op)[0].isalpha():
            raise Exception("invalid identifier '%s'" % op)
        else:
            return op
