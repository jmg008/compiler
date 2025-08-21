from lexer import lex

sourceCode = """\
    function main() {
      print 'Hello, World!';
    }"""
tokenList = lex(sourceCode)
print(sourceCode)