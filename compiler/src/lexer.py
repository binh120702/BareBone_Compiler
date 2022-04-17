from const import *

def invalidCharacterDetect(character):
    if character == '\t' or character == ' '  or character == '\n' or character == ';' or character == '_' or str.isalpha(character) or str.isdigit(character):
        return False
    return True

def invalidLexeme(lexeme):
    if lexeme == '0':
        return False
    if len(lexeme) and str.isdigit(lexeme[0]):
        return True
    return False

def tokenCategorize(lexeme):
    for name, member in Reserved.__members__.items():
        if lexeme.upper() == name:
            return member
    if lexeme == '0':
        return Reserved.ZERO
    if lexeme == ';':
        return Reserved.SEMICOLON
    return Reserved.ID

def lexicalAnalyze(srcCode):
    tokenList = []
    debugPosition = []
    lexeme = ""
    line = 1
    col = 0
    inComment = False
    for character in srcCode:
        col += 1
        if character == '#':
            inComment = True
        if character == '\n':
            inComment = False
        if inComment : 
            continue
        if invalidCharacterDetect(character):
            sys.exit(Error.INVALID_CHARACTER(character, line, col))
        if character == ' '  or character == '\t' or character == '\n' or character == ';':
            if invalidLexeme(lexeme):
                sys.exit(Error.INVALID_IDENTIFIER(lexeme, line, col))
            if len(lexeme):
                token = tokenCategorize(lexeme)
                if (token == Reserved.ID):
                    lexeme = lexeme.upper()
                tokenList.append([token, lexeme])
                debugPosition.append([line, col-1])
            lexeme = ""
            if character == '\n':
                line += 1
                col = 1
            if character == ';':
                lexeme = ";"
        else:
            lexeme = lexeme + character
    return tokenList, debugPosition
