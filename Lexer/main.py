from lexer import lex
from Token import Kind

sourceCode = """\
    function main() {
      print 'Hello, World!';
    }"""
tokenList = lex(sourceCode)
for i in tokenList:
	if i != Kind.EndOfToken:
		print(f"{i.kind} : {i.string}")
	else:
		print("#EndOfToken")