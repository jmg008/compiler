from Lexer import lex
from Parser import parse

sourceCode = """\
    function main() {
      print 'Hello, World!';
      var a = {'1' : 1 + 2 * 5};
    }"""

tokenList = lex(sourceCode)
syntaxTree = parse(tokenList)
syntaxTree.printSyntaxTree()