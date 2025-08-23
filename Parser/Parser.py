from Token import *
from Node import *

def skipCurrent(kind: Kind = None)->None:
    global tokensIter, current
    if kind != None and current.kind != kind:
        print(f"{kind} 토큰이 필요함")
        print(current.kind, current.string)
        exit(1)
    current = next(tokensIter)

def skipCurrentIf(kind: Kind)->None:
    global tokensIter, current
    if current.kind != kind:
        return False
    current = next(tokensIter)
    return True

def parseExpression()->Expression:
    return parseAssigment()

def parseElement(sub: Expression)->Expression:
    global tokensIter, current
    result = GetElement()
    result.sub = sub
    skipCurrent(Kind.LeftBraket)
    result.index = parseExpression()
    skipCurrent(Kind.RightBraket)
    return result

def parseCall(sub: Expression)->Expression:
    global tokensIter, current
    result = Call()
    result.sub = sub
    skipCurrent(Kind.LeftParen)
    if current.kind != Kind.RightParen:
        while True:
            result.argumemts.append(parseExpression())
            if not skipCurrentIf(Kind.Comma):
                break
    skipCurrent(Kind.RightParen)
    return result

def parsePostFix(sub: Expression)->Expression:
    global tokensIter, current
    while True:
        if current.kind == Kind.LeftParen:
            sub = parseCall()
        elif current.kind == Kind.LeftBraket:
            sub = parseElement()
        else:
            return sub

def parseNullLiteral()->Expression:
    skipCurrent(Kind.NullLiteral)
    result = NullLiteral()
    return result

def parseBooleanLiteral()->Expression:
    result = BooleanLiteral()
    result.value = current.kind == Kind.TrueLiteral
    skipCurrent()
    return result

def parseNumberLiteral()->Expression:
    result = NumberLiteral()
    result.value = float(current.string)
    skipCurrent(Kind.NumberLiteral)
    return result

def parseStringLiteral()->Expression:
    result = StringLiteral()
    result.value = current.string
    skipCurrent(Kind.StringLiteral)
    return result

def parseListLiteral()->Expression:
    result = ArrayLiteral()
    skipCurrent(Kind.LeftBraket)
    if current.kind != Kind.RightBraket:
        while True:
            result.values.append(parseExpression())
            if not skipCurrentIf(Kind.Comma):
                break
    skipCurrent(Kind.RightBraket)
    return result

def parseMapLiteral()->Expression:
    result = MapLiteral()
    skipCurrent(Kind.LeftBrace)
    if current.kind != Kind.RightBrace:
        while True:
            name = current.string
            skipCurrent(Kind.StringLiteral)
            skipCurrent(Kind.Colon)
            value = parseExpression()
            result.values[name] = value
            if not skipCurrentIf(Kind.Comma):
                break
    skipCurrent(Kind.RightBrace)
    return result

def parseIdentifier()->Expression:
    result = GetVariable()
    result.name = current.string
    skipCurrent(Kind.Identifier)
    return result

def parseInnerExpression()->Expression:
    skipCurrent(Kind.LeftParen)
    result = parseExpression()
    skipCurrent(Kind.RightParen)
    return result

def parseOperand()->Expression:
    global tokensIter, current
    if current.kind == Kind.NullLiteral:
        result = parseNullLiteral()
    elif current.kind == Kind.TrueLiteral or current.kind == Kind.FalseLiteral:
        result = parseBooleanLiteral()
    elif current.kind == Kind.NumberLiteral:
        result = parseNumberLiteral()
    elif current.kind == Kind.StringLiteral:
        result = parseStringLiteral()
    elif current.kind == Kind.LeftBraket:
        result = parseListLiteral()
    elif current.kind == Kind.LeftBrace:
        result = parseMapLiteral()
    elif current.kind == Kind.Identifier:
        result = parseIdentifier()
    elif current.kind == Kind.LeftParen:
        result = parseInnerExpression()
    else:
        print("옳지 못한 식")
        print(current.kind, current.string)
        exit(1)
    return parsePostFix(result)

def parseUnary()->Expression:
    global tokensIter, current
    operators = [Kind.Add,
                 Kind.Subtract]
    while current.kind in operators:
        result = Unary()
        result.kind = current.kind
        skipCurrent()
        result.sub = parseUnary()
        return result
    return parseOperand()

def parseArithmetic2()->Expression:
    global tokensIter, current
    operators = [Kind.Multiply,
                 Kind.Divide,
                 Kind.Modulo]
    result = parseUnary()
    while current.kind in operators:
        tmp = Arithmetic()
        skipCurrent()
        tmp.lhs = result
        tmp.rhs = parseUnary()
        result = tmp
    return result

def parseArithmetic1()->Expression:
    global tokensIter, current
    operators = [Kind.Add,
                 Kind.Subtract]
    result = parseArithmetic2()
    while current.kind in operators:
        tmp = Arithmetic()
        tmp.kind = current.kind
        skipCurrent()
        tmp.lhs = result
        tmp.rhs = parseArithmetic2()
        result = tmp
    return result

def parseRelational()->Expression:
    global tokensIter, current
    operators = [Kind.Equal,
                 Kind.NotEqual,
                 Kind.LessThan,
                 Kind.LessOrEqual,
                 Kind.GreaterThan,
                 Kind.GreaterOrEqual]
    result = parseArithmetic1()
    while current.kind in operators:
        tmp = Relational()
        tmp.kind = current.kind
        skipCurrent()
        tmp.lhs = result
        tmp.rhs = parseArithmetic1()
        result = tmp
    return result

def parseAnd()->Expression:
    global tokensIter, current
    result = parseRelational()
    while skipCurrentIf(Kind.LogicalAnd):
        tmp = And()
        tmp.lhs = result
        tmp.rhs = parseRelational()
        result = tmp
    return result

def parseOr()->Expression:
    global tokensIter, current
    result = parseAnd()
    while skipCurrentIf(Kind.LogicalOr):
        tmp = Or()
        tmp.lhs = result
        tmp.rhs = parseAnd()
        result = tmp
    return result

def parseAssigment()->Expression:
    global tokensIter, current
    result = parseOr()
    if current.kind != Kind.Assignment:
        return result
    skipCurrent(Kind.Assignment)
    # if (getVariable := downCast(result, GetVariable)):
    if (issubclass(type(getVariable := result), GetVariable)):
        result = SetVariable()
        result.name = getVariable.name
        result.value = parseAssigment()
        return result
    # if (getElement := downCast(result, GetElement)):
    if (issubclass(type(getElement := result), GetElement)):
        result = SetElement()
        result.name = getElement.name
        result.value = parseAssigment()
        return result
    print("옳지 못한 대입 연산 식")
    exit(1)

def parseExpressionStatement()->ExpressionStatement:
    global tokensIter, current
    result = ExpressionStatement()
    result.expression = parseExpression()
    skipCurrent(Kind.Semicolon)
    return result

def parseContinue()->Continue:
    result = Continue()
    skipCurrent(Kind.Continue)
    skipCurrent(Kind.Semicolon)
    return result

def parseBreak()->Break:
    result = Break()
    skipCurrent(Kind.Break)
    skipCurrent(Kind.Semicolon)
    return result

def parseReturn()->Return:
    result = Return()
    skipCurrent(Kind.Return)
    result.expression = parseExpression()
    if not result.expression:
        print("return문에 식이 없음")
        exit(1)
    skipCurrent(Kind.Semicolon)
    return result

def parsePrint()->Print:
    result = Print()
    result.lindFeed = current.kind == Kind.PrintLine
    skipCurrent()
    if current.kind != Kind.Semicolon:
        while True:
            result.arguments.append(parseExpression())
            if not skipCurrentIf(Kind.Comma):
                break
    skipCurrent(Kind.Semicolon)
    return result

def parseIf()->If:
    result = If()
    skipCurrent(Kind.If)
    while True:
        condition = parseExpression()
        if not condition:
            print("If문 조건식 없음")
            exit(1)
        result.conditons.append(condition)
        skipCurrent(Kind.LeftBrace)
        result.blocks.append(parseBlock())
        skipCurrent(Kind.RightBrace)
        if not skipCurrentIf(Kind.Elif):
            break
    if skipCurrentIf(Kind.Else):
        skipCurrent(Kind.LeftBrace)
        result.elseBlock = parseBlock()
        skipCurrent(Kind.RightBrace)
    return result

def parseFor()->For:
    result = For()
    skipCurrent(Kind.For)
    result.variable = Variable()
    result.variable.name = current.string
    skipCurrent(Kind.Identifier)
    skipCurrent(Kind.Assignment)
    result.variable.expression = parseExpression()
    if not result.variable.expressing:
        print("for문에 초기화식이 없음")
        exit(1)
    skipCurrent(Kind.Comma)
    result.condition = parseExpression()
    if not result.condition:
        print("for문에 조건식이 없음")
        exit(1)
    skipCurrent(Kind.Comma)
    result.expression = parseExpression()
    if not result.expression    :
        print("for문에 증감식이 없음")
        exit(1)
    skipCurrent(Kind.LeftBrace)
    result.block = parseBlock()
    skipCurrent(Kind.RightBrace)
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
        elif current.kind == Kind.For:
            result.append(parseFor())
        elif current.kind == Kind.If:
            result.append(parseIf())
        elif current.kind == Kind.Print or current.kind == Kind.PrintLine:
            result.append(parsePrint())
        elif current.kind == Kind.Return:
            result.append(parseReturn())
        elif current.kind == Kind.Break:
            result.append(parseBreak())
        elif current.kind == Kind.Continue:
            result.append(parseContinue())
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
            result.functions.append(parseFunction())
        else:
            print(f"{current} 잘못된 구문")
    return result