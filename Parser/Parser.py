from Token import *
from Node import *

def skipCurrent(kind: Kind)->None:
    global tokensIter, current
    if current.kind != kind:
        print("toString(current.kind) 토큰이 필요함")
        exit(1)
    current = next(tokensIter)

def skipCurrentIf(kind: Kind)->None:
    global tokensIter, current
    if current.kind != kind:
        return False
    current = next(tokensIter)
    return True

def parseAnd()->Expression:
    pass

def parseOr()->Expression:
    result = parseAnd()
    while skipCurrentIf(Kind.LogicalOr):
        tmp = Or()
        tmp.lhs = result
        tmp.rhs = parseAnd()
        result = tmp
    return result

def parseAssigment()->Expression:
    result = parseOr()
    if current.kind != Kind.Assignment:
        return result
    skipCurrent(Kind.Assignment)
    if (getVariable := downCast(result, GetVariable)):
        result = SetVariable()
        result.name = getVariable.name
        result.value = parseAssigment()
        return result
    if (getElement := downCast(result, GetElement)):
        result = SetElement()
        result.name = getElement.name
        result.value = parseAssigment()
        return result
    print("옳지 못한 대입 연산 식")
    exit(1)

def parseExpression()->Expression:
    return parseAssigment()

def parseExpressionStatement()->ExpressionStatement:
    global tokensIter, current
    result = ExpressionStatement()
    result.expression = parseExpression()
    skipCurrent(Kind.Semicolon)
    return result

def parseVariable()->Variable:
    global tokensIter, current
    result = Variable()
    skipCurrent(Kind.Variable)
    result.name = current.string
    skipCurrent(Kind.Identifier)
    skipCurrent(Kind.Assignment)
    result.expression = parseExpression()
    skipCurrent(Kind.Semicolon)
    return result

def parseBlock()->list[Statement]:
    global tokensIter, current
    result = []
    while current.kind != Kind.RightBrace:
        if current.kind == Kind.Variable:
            result.append(parseVariable())
        elif current.kind == Kind.EndOfToken:
            print(current + " 옳지 못한 구문")
        else:
            result.append(parseExpressionStatement())
    return result

def parseFunction()->Function:
    global tokensIter, current
    result = Function()
    skipCurrent(Kind.Function)
    result.name = current.string
    skipCurrent(Kind.Identifier)
    skipCurrent(Kind.LeftParen)
    if current.kind != Kind.RightParen:
        while True:
            result.parameters.append(current.string)
            skipCurrent(Kind.Identifier)
            if not skipCurrentIf(Kind.Comma):
                break
    skipCurrent(Kind.RightParen)
    skipCurrent(Kind.LeftBrace)
    result.block = parseBlock()
    skipCurrent(Kind.RightBrace)
    return result

def parse(tokens: list[Token])->Program:
    result = Program()
    global tokensIter, current
    tokensIter = iter(tokens)
    current = next(tokensIter)
    while current.kind != Kind.EndOfToken:
        if current.kind == Kind.Function:
            result.functions.append(parseFunction)
        else:
            print(f"{current} 잘못된 구문")
    return result