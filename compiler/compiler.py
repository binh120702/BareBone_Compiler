from logging import exception
from const import *
import lexer
import parser
import codegenner
import coderunner
import subprocess
def compile(srcCode):
    try:
        tokenList, debugPosition = lexer.lexicalAnalyze(srcCode)
        parseTree = parser.syntaxAnalyze(tokenList, debugPosition)
        asmSource = codegenner.codeGenerate(parseTree)
        coderunner.codeRun(asmSource)
    except SystemExit as error:
        subprocess.call(["echo", "-e", "\\033[1;31m" + str(error) + "\\033[0m"])
    print("-----------------------------done-------------------------------------")
"""
if len(sys.argv) == 2:
    fileName = sys.argv[1]
    if not os.path.exists(fileName):
        sys.exit(Error.INVALID_FILE_NAME(fileName))
    fileSrcCode = open(fileName)
    srcCode = fileSrcCode.read()
    compile(srcCode)
else:
    sys.exit(Error.INVALID_COMMAND.value)
"""