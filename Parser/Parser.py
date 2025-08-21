# TODO: 60p부터, parseFunction부터

from Token import *
from Node import *

def skipCurrent(kind: Kind)->None:
    global tokensIter, current
    if current.kind != kind:
        print("토큰이 없어요")
        exit(1)
    current = next(tokensIter)

def parseFunction()->Function:
    result = Function()
    skipCurrent(Kind.Function)
    result.name = current.string

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