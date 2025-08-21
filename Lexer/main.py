from Lexer import lex
from Token import Kind

sourceCode = """\
    function main() {
      print 'Hello, World!';
    }"""
tokenList = lex(sourceCode)
print("Kind                 : String")
print("--------------------------------")
for i in tokenList:
	if i != Kind.EndOfToken:
		print(f"{i.kind:20} : {i.string}")
	else:
		print("#EndOfToken")