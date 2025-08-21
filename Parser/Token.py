from enum import Enum

Kind = Enum(value='Kind', names="Unknown EndOfToken NullLiteral TrueLiteral FalseLiteral NumberLiteral StringLiteral Identifier Function Return Variable For Break Continue If Elif Else Print PrintLine LogicalAnd LogicalOr Assignment Add Subtract Multiply Divide Modulo Equal NotEqual LessThan GreaterThan LessOrEqual GreaterOrEqual Comma Colon Semicolon LeftParen RightParen LeftBrace RightBrace LeftBraket RightBraket", start=1)

stringToKind = {
    "#unknown":    Kind.Unknown,
    "#EndOfToken": Kind.EndOfToken,

    "null":        Kind.NullLiteral,
    "true":        Kind.TrueLiteral,
    "false":       Kind.FalseLiteral,
    "#Number":     Kind.NumberLiteral,
    "#String":     Kind.StringLiteral,
    "#identifier": Kind.Identifier,

    "function":    Kind.Function,
    "return":      Kind.Return,
    "var":         Kind.Variable,
    "for":         Kind.For,
    "break":       Kind.Break,
    "continue":    Kind.Continue,
    "if":          Kind.If,
    "elif":        Kind.Elif,
    "else":        Kind.Else,
    "print":       Kind.Print,
    "printLine":   Kind.PrintLine,

    "and":         Kind.LogicalAnd,
    "or":          Kind.LogicalOr,

    "=":           Kind.Assignment,

    "+":           Kind.Add,
    "-":           Kind.Subtract,
    "*":           Kind.Multiply,
    "/":           Kind.Divide,
    "%":           Kind.Modulo,

    "==":          Kind.Equal,
    "!=":          Kind.NotEqual,
    "<":           Kind.LessThan,
    ">":           Kind.GreaterThan,
    "<=":          Kind.LessOrEqual,
    ">=":          Kind.GreaterOrEqual,

    ",":           Kind.Comma,
    ":":           Kind.Colon,
    ";":           Kind.Semicolon,
    "(":           Kind.LeftParen,
    ")":           Kind.RightParen,
    "{":           Kind.LeftBrace,
    "}":            Kind.RightBrace,
    "[":           Kind.LeftBraket,
    "]":           Kind.RightBraket,
}

class Token:
    def __init__(self, kind:Kind, string:str):
        self.kind = kind
        self.string = string

def toKind(string)->Kind:
    if string in stringToKind:
        return stringToKind[string]
    return Kind.Unknown