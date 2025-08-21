from Token import Token, Kind
from enum import Enum

CharType = Enum(value="CharType", names="Unknown WhiteSpace NumberLiteral StringLiteral IdentifierAndKeyword OperatorAndPunctuator", start=1)

def getCharType(c:str)->CharType:
    if c == ' ' or c == '\t' or c == '\r' or c == '\n':
        return CharType.WhiteSpace
    if '0' <= c and c <= '9':
        return CharType.NumberLiteral
    if c == '\'':
        return CharType.StringLiteral
    if ('a' <= c and c <= 'z') or ('A' <= c and c <= 'Z'):
        return CharType.IdentifierAndKeyword
    oc = ord(c)
    if (33 <= oc and oc <=47 and c != '\'') or (58 <= oc and oc <= 64) or (91 <= oc and oc <= 96) or (123 <= oc and oc <= 126):
        
    return CharType.Unknown

def lex(sourceCode:str)->list[Token]:
    result = []
    sourceCode += '\0'
    codeIter = iter(sourceCode)
    current = next(codeIter)
    while current != '\0':
        currentCharType = getCharType(current)
        if currentCharType == CharType.WhiteSpace:
            current = next(codeIter)
        elif currentCharType == CharType.NumberLiteral:
            pass
        elif currentCharType == CharType.StringLiteral:
            pass
        else:
            print("사용 불가 문자")
            exit(1)
    result.append(Kind.EndOfToken)
    return result