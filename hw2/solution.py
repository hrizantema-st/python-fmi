class Constant:
    def __init__(self, const):
        self.const = const

    def __str__(self):
        return str(self.const)

    def __repr__(self):
        return str(self)

    def evaluate(self, **variables):
        return self.const


class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def evaluate(self, **variables):
        for kw in variables.keys():
            return variables[kw]


class Expression:
    def __init__(self, expression_structure):
        self.expr_struct = expression_structure
        variable_names = set()
        for exp in expression_structure:
            if isinstance(exp, Variable):
                variable_names.add(exp)

    def __str__(self):
        expr_str = "("
        for each in self.expr_struct:
            if not isinstance(each, tuple):
                expr_str += str(each)
            else:
                for element in each:
                    expr_str += element.__str__()
        expr_str += ")"
        return expr_str

    def __repr__(self):
        return str(self)

    def evaluate(self, **variables):
        op1 = self.expr_struct[0]
        op2 = self.expr_struct[2]
        val1 = op1.evaluate(variables)
        val2 = op2.evaluate(variables)
        val = self.expr_struct[1].function(val1, val2)
        return val

    def __add__(self, other):
        return Expression((self.expr_struct, '+', other))

    def __sub__(self, other):
        return Expression((self.expr_struct, '-', other))

    def __mul__(self, other):
        return Expression((self.expr_struct, '*', other))

    def __truediv__(self, other):
        return Expression((self.expr_struct, '/', other))


class Operator:
    def __init__(self, symbol, function):
        self.symbol = symbol
        self.function = function

    def __str__(self):
        return " " + self.symbol + " "

    def __repr__(self):
        return str(self)


def create_constant(value):
    const = Constant(value)
    return const


def create_variable(name):
    var = Variable(name)
    return var


def create_operator(symbol, function):
    op = Operator(symbol, function)
    return op


def create_expression(expression_structure):
    expr = Expression(expression_structure)
    return expr
