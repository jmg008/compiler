from Token import Kind

class Statement:
    def __init__(self):
        pass

class Expression:
    def __init__(self):
        pass

class Function(Statement):
    def __init__(self, name: str = None, parameters: list[str] = [], block: list[Statement] = []):
        self.name = name
        self.parameters = parameters
        self.block = block

class Program:
    def __init__(self, functions: list[Function] = []):
        self.functions = functions

class Return(Statement):
    def __init__(self, expression: Expression = None):
        self.expression = expression

class Variable(Statement):
    def __init__(self, name: str = None, expression: Expression = None):
        self.name = name
        self.expression = expression

class For(Statement):
    def __init__(self, variable: Variable = None, condition: Expression = None, expression: Expression = None, block: list[Statement] = []):
        self.variable = variable
        self.condition = condition
        self.expression = expression
        self.blcok = block

class Break(Statement): pass

class Countinue(Statement): pass

class If(Statement):
    def __init__(self, conditons: list[Expression] = [], blocks: list[list[Statement]] = [], elseBlock: list[Statement] = []):
        self.conditons = conditons
        self.blocks = blocks
        self.elseBlock = elseBlock

class Print(Statement):
    def __init__(self, lindFeed: bool = None, arguments: list[Expression] = []):
        self.lindFeed = lindFeed
        self.arguments = arguments

class ExpressionStatement(Statement):
    def __init__(self, expression: Expression = None):
        self.expression = expression

class Or(Expression):
    def __init__(self, lhs: Expression = None, rhs: Expression = None):
        self.lhs = lhs
        self.rhs = rhs

class And(Expression):
    def __init__(self, lhs: Expression = None, rhs: Expression = None):
        self.lhs = lhs
        self.rhs = rhs

class Relational(Expression):
    def __init__(self, kind: Kind = None, lhs: Expression = None, rhs: Expression = None):
        self.kind = kind
        self.lhs = lhs
        self.rhs = rhs

class Arithmetic(Expression):
    def __init__(self, kind: Kind = None, lhs: Expression = None, rhs: Expression = None):
        self.kind = kind
        self.lhs = lhs
        self.rhs = rhs

class Unary(Expression):
    def __init__(self, kind: Kind = None, sub: Expression = None):
        self.kind = kind
        self.sub = sub

class Call(Expression):
    def __init__(self, sub: Expression = None, arguments: list[Expression] = []):
        self.sub = sub
        self.argumemts = arguments

class GetElement(Expression):
    def __init__(self, sub: Expression = None, index: Expression = None):
        self.sub = sub
        self.index = index

class SetElement(Expression):
    def __init__(self, sub: Expression = None, index: Expression = None, value: Expression = None):
        self.sub = sub
        self.index = index
        self.value = value

class GetVariable(Expression):
    def __init__(self, name: str = None):
        self.name = name

class SetVariable(Expression):
    def __init__(self, name: str = None, value: Expression = None):
        self.name = name
        self.value = value

class NullLiteral(Expression): pass

class BoolLiteral(Expression):
    def __init__(self, value: bool = False):
        self.value = value

class NumberLiteral(Expression):
    def __init__(self, value: float = 0.0):
        self.value = value

class StringLiteral(Expression):
    def __init__(self, value: str):
        self.value = value

class ArrayLiteral(Expression):
    def __init__(self, values: list[Expression] = []):
        self.values = values

class MapLiteral(Expression):
    def __init__(self, values: dict[str: Expression] = {}):
        self.values = values

def downCast(obj, targetClass):
    if issubclass(targetClass, type(obj)):
        return targetClass(**vars(obj))
    return None