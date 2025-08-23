from Token import Token, Kind, toKind
from enum import Enum

CharType = Enum(value="CharType", names="Unknown WhiteSpace NumberLiteral StringLiteral IdentifierAndKeyword OperatorAndPunctuator", start=1)

def getCharType(c: str)->CharType:
    if c == ' ' or c == '\t' or c == '\r' or c == '\n':
        return CharType.WhiteSpace
    if '0' <= c and c <= '9':
        return CharType.NumberLiteral
    if c == '\'':
        return CharType.StringLiteral
    if ('a' <= c and c <= 'z') or ('A' <= c and c <= 'Z'):
        return CharType.IdentifierAndKeyword
    oc = ord(c)
    if (33 <= oc and oc <= 47 and c != '\'') or (58 <= oc and oc <= 64) or (91 <= oc and oc <= 96) or (123 <= oc and oc <= 126):
        return CharType.OperatorAndPunctuator
    return CharType.Unknown

def isCharType(c: str, type: CharType)->bool:
    if type == CharType.NumberLiteral:
        return '0' <= c and c <= '9'
    oc = ord(c)
    if type == CharType.StringLiteral:
        return 32 <= oc and oc <= 126 and c != '\''
    if type == CharType.IdentifierAndKeyword:
        return ('0' <= c and c <= '9') or ('a' <= c and c <= 'z') or ('A' <= c and c <= 'Z')
    if type == CharType.OperatorAndPunctuator:
        return (33 <= oc and oc <= 47) or (58 <= oc and oc <= 64) or (91 <= oc and oc <= 96) or (123 <= oc and oc <= 126)
    return False

def scanNumberLiteral()->Token:
    global codeIter, current
    string = ""
    while isCharType(current, CharType.NumberLiteral):
        string += current
        current = next(codeIter)
    if current == '.':
        while isCharType(current, CharType.NumberLiteral):
            string += current
            current = next(codeIter)
    return Token(Kind.NumberLiteral, string)

def scanStringLiteral()->Token:
    global codeIter, current
    string = ''
    current = next(codeIter)
    while isCharType(current, CharType.StringLiteral):
        string += current
        current = next(codeIter)
    if current != '\'':
        print("문자열 안 닫힘")
        exit(1)
    current = next(codeIter)
    return Token(Kind.StringLiteral, string)

def scanIdentifierAndKeyword()->Token:
    global codeIter, current
    string = ''
    while isCharType(current, CharType.IdentifierAndKeyword):
        string += current
        current = next(codeIter)
    kind = toKind(string)
    if kind == Kind.Unknown:
        kind = Kind.Identifier
    return Token(kind, string)

def scanOperatorAndPunctuator()->Token:
    global codeIter, current
    string = []
    while isCharType(current, CharType.OperatorAndPunctuator):
        string.append(current)
        current = next(codeIter)
    tmp = []
    while string != [] and toKind(''.join(string)) == Kind.Unknown:
        tmp = [string.pop()]+tmp
    if string == []:
        print(tmp[0] + " 사용못하는문자")
        exit(1)
    # 왜 파이썬 이터레이터는 뒤로 못감????
    # 이거 때문에 이후 코드 한 번 순회해야함
    tmp = ''.join(tmp)
    while current != '\0':
        tmp += current
        current = next(codeIter)
    tmp += '\0'
    codeIter = iter(tmp)
    current = next(codeIter)
    return Token(toKind(''.join(string)), ''.join(string))

def lex(sourceCode: str)->list[Token]:
    result = []
    sourceCode += '\0'
    global codeIter, current
    codeIter = iter(sourceCode)
    current = next(codeIter)
    while current != '\0':
        currentCharType = getCharType(current)
        if currentCharType == CharType.WhiteSpace:
            current = next(codeIter)
        elif currentCharType == CharType.NumberLiteral:
            result.append(scanNumberLiteral())
        elif currentCharType == CharType.StringLiteral:
            result.append(scanStringLiteral())
        elif currentCharType == CharType.OperatorAndPunctuator:
            result.append(scanOperatorAndPunctuator())
        elif currentCharType == CharType.IdentifierAndKeyword:
            result.append(scanIdentifierAndKeyword())
        else:
            print(current)
            print("사용 불가 문자")
            exit(1)
    result.append(Token(Kind.EndOfToken, "\0"))
    return result