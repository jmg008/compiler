from Token import Kind, toString

def indent(depth: int)->None:
    print(' '*(depth*2), end = '')

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
    def print(self, depth: int):
        indent(depth)
        print(f"FUNCTION {self.name}: ")
        if self.parameters:
            indent(depth + 1)
            print("PARAMETERS:", end='')
            for name in self.parameters:
                print(f"{name} ", end='')
            print()
        indent(depth + 1)
        print("BLOCK:")
        for node in self.block:
            node.print(depth + 2)

class Program:
    def __init__(self, functions: list[Function] = []):
        self.functions = functions
    
    def printSyntaxTree(self):
        for function in self.functions:
            function.print(0)

class Return(Statement):
    def __init__(self, expression: Expression = None):
        self.expression = expression

    def print(self, depth: int):
        indent(depth)
        print("RETURN:")
        if self.expression:
            self.expression.print(depth + 1)

class Variable(Statement):
    def __init__(self, name: str = None, expression: Expression = None):
        self.name = name
        self.expression = expression

    def print(self, depth: int):
        indent(depth)
        print(f"VAR {self.name}:")
        self.expression.print(depth + 1)

class For(Statement):
    def __init__(self, variable: Variable = None, condition: Expression = None, expression: Expression = None, block: list[Statement] = []):
        self.variable = variable
        self.condition = condition
        self.expression = expression
        self.block = block
    
    def print(self, depth: int):
        indent(depth)
        print("FOR:")
        indent(depth + 1)
        print("VARIABLE:")
        self.variable.print(depth + 2)
        indent(depth + 1)
        print("CONDITION:")
        self.condition.print(depth + 2)
        indent(depth + 1)
        print("EXPRESSION:")
        self.expression.print(depth + 2)
        indent(depth + 1)
        print("BLOCK:")
        for node in self.block:
            node.print(depth + 2)

class Break(Statement):
    def print(self, depth: int):
        indent(depth)
        print("BREAK")

class Continue(Statement):
    def print(self, depth: int):
        indent(depth)
        print("CONTINUE")

class If(Statement):
    def __init__(self, conditions: list[Expression] = [], blocks: list[list[Statement]] = [], elseBlock: list[Statement] = []):
        self.conditions = conditions
        self.blocks = blocks
        self.elseBlock = elseBlock

    def print(self, depth: int):
        for i, condition in enumerate(self.conditions):
            indent(depth)
            print("IF:" if i == 0 else "ELIF:")
            indent(depth + 1)
            print("CONDITION:")
            condition.print(depth + 2)
            indent(depth + 1)
            print("BLOCK:")
            for node in self.blocks[i]:
                node.print(depth + 2)
        
        if self.elseBlock:
            indent(depth)
            print("ELSE:")
            for node in self.elseBlock:
                node.print(depth + 1)

class Print(Statement):
    def __init__(self, lineFeed: bool = None, arguments: list[Expression] = []):
        self.lineFeed = lineFeed
        self.arguments = arguments

    def print(self, depth: int):
        indent(depth)
        print("PRINT_LINE" if self.lineFeed else "PRINT:")
        for arg in self.arguments:
            arg.print(depth + 1)

class ExpressionStatement(Statement):
    def __init__(self, expression: Expression = None):
        self.expression = expression

    def print(self, depth: int):
        indent(depth)
        print("EXPRESSION:")
        self.expression.print(depth + 1)

class Or(Expression):
    def __init__(self, lhs: Expression = None, rhs: Expression = None):
        self.lhs = lhs
        self.rhs = rhs

    def print(self, depth: int):
        indent(depth)
        print("OR:")
        indent(depth + 1)
        print("LHS:")
        self.lhs.print(depth + 2)
        indent(depth + 1)
        print("RHS:")
        self.rhs.print(depth + 2)

class And(Expression):
    def __init__(self, lhs: Expression = None, rhs: Expression = None):
        self.lhs = lhs
        self.rhs = rhs

    def print(self, depth: int):
        indent(depth)
        print("AND:")
        indent(depth + 1)
        print("LHS:")
        self.lhs.print(depth + 2)
        indent(depth + 1)
        print("RHS:")
        self.rhs.print(depth + 2)

class Relational(Expression):
    def __init__(self, kind: Kind = None, lhs: Expression = None, rhs: Expression = None):
        self.kind = kind
        self.lhs = lhs
        self.rhs = rhs
    
    def print(self, depth: int):
        indent(depth)
        print(f"{toString(self.kind)}:")
        indent(depth + 1)
        print("LHS:")
        self.lhs.print(depth + 2)
        indent(depth + 1)
        print("RHS:")
        self.rhs.print(depth + 2)

class Arithmetic(Expression):
    def __init__(self, kind: Kind = None, lhs: Expression = None, rhs: Expression = None):
        self.kind = kind
        self.lhs = lhs
        self.rhs = rhs

    def print(self, depth: int):
        indent(depth)
        print(f"{toString(self.kind)}:")
        indent(depth + 1)
        print("LHS:")
        self.lhs.print(depth + 2)
        indent(depth + 1)
        print("RHS:")
        self.rhs.print(depth + 2)

class Unary(Expression):
    def __init__(self, kind: Kind = None, sub: Expression = None):
        self.kind = kind
        self.sub = sub

    def print(self, depth: int):
        indent(depth)
        print(toString(self.kind))
        self.sub.print(depth + 1)

class Call(Expression):
    def __init__(self, sub: Expression = None, arguments: list[Expression] = []):
        self.sub = sub
        self.arguments = arguments

    def print(self, depth: int):
        indent(depth)
        print("CALL:")
        indent(depth + 1)
        print("EXPRESSION:")
        self.sub.print(depth + 2)
        for arg in self.arguments:
            indent(depth + 1)
            print("ARGUMENT:")
            arg.print(depth + 2)

class GetElement(Expression):
    def __init__(self, sub: Expression = None, index: Expression = None):
        self.sub = sub
        self.index = index

    def print(self, depth: int):
        indent(depth)
        print("GET_ELEMENT:")
        indent(depth + 1)
        print("SUB:")
        self.sub.print(depth + 2)
        indent(depth + 1)
        print("INDEX:")
        self.index.print(depth + 2)

class SetElement(Expression):
    def __init__(self, sub: Expression = None, index: Expression = None, value: Expression = None):
        self.sub = sub
        self.index = index
        self.value = value

    def print(self, depth: int):
        indent(depth)
        print("SET_ELEMENT:")
        indent(depth + 1)
        print("SUB:")
        self.sub.print(depth + 2)
        indent(depth + 1)
        print("INDEX:")
        self.index.print(depth + 2)
        indent(depth + 1)
        print("VALUE:")
        self.value.print(depth + 2)

class GetVariable(Expression):
    def __init__(self, name: str = None):
        self.name = name

    def print(self, depth: int):
        indent(depth)
        print(f"GET_VARIABLE: {self.name}")

class SetVariable(Expression):
    def __init__(self, name: str = None, value: Expression = None):
        self.name = name
        self.value = value

    def print(self, depth: int):
        indent(depth)
        print(f"SET_VARIABLE: {self.name}")
        self.value.print(depth + 1)

class NullLiteral(Expression):
    def print(self, depth: int):
        indent(depth)
        print("null")

class BooleanLiteral(Expression):
    def __init__(self, value: bool = False):
        self.value = value

    def print(self, depth: int):
        indent(depth)
        print("true" if self.value else "false")

class NumberLiteral(Expression):
    def __init__(self, value: float = 0.0):
        self.value = value

    def print(self, depth: int):
        indent(depth)
        print(self.value)

class StringLiteral(Expression):
    def __init__(self, value: str = ""):
        self.value = value

    def print(self, depth: int):
        indent(depth)
        print(f'"{self.value}"')

class ArrayLiteral(Expression):
    def __init__(self, values: list[Expression] = []):
        self.values = values

    def print(self, depth: int):
        indent(depth)
        print("[")
        for value in self.values:
            value.print(depth + 1)
        indent(depth)
        print("]")

class MapLiteral(Expression):
    def __init__(self, values: dict[str, Expression] = {}):
        self.values = values

    def print(self, depth: int):
        indent(depth)
        print("{")
        for key, value in self.values.items():
            indent(depth + 1)
            print(f"{key}: ", end="")
            value.print(depth + 1) # value should be printed on the same line or next with deeper indent. C++ code is ambiguous. This implementation prints value on the same line.
        indent(depth)
        print("}")