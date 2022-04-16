import enum
import sys
import os 

class Error(enum.Enum):
    INVALID_COMMAND = "Invalid command! Command should exactly contain two arguments: 1 - compliler and 2 - source code"
    INVALID_CHARACTER =  lambda char, line, col : "Invalid character: {}\nDetected in: line {}, col {}".format(char, str(line), str(col))
    INVALID_FILE_NAME = lambda fileName : "Invalid file name: {}".format(fileName) 
    INVALID_IDENTIFIER = lambda lexeme, line, col : "Invalid lexeme: {}\nDetected in: line {}, col {}".format(lexeme, line, col)
    INVALID_SYNTAX = lambda debugPosition : "Invalid syntax!\nDetected in: line {}, col {}".format(debugPosition[0], debugPosition[1])

class Nasm(enum.Enum):
    EXTENSION = "extern printf\n" 
    DATA_SECTION_HEADER = "SECTION .data\n"
    DATA_SECTION_DECLARE = lambda name, value : "{} : dq {}\n".format(name, str(value))
    DATA_SECTION_MESSAGE = "fmt: db \"%s = %lld\", 10, 0\n"
    TEXT_SECTION_HEADER = "SECTION .text\n"
    GLOBAL_HEADER = "global main \n main: \n push rbp \n"
    LABEL = lambda name : "{}:\n".format(name) 
    JUMPTO = lambda name : "jmp {}\n".format(name) 
    IFNOTZERO = lambda ident, end_label : "mov rcx, [{}] \n cmp rcx, 0 \n je {}\n".format(ident, end_label)
    CLEAR = lambda ident : "mov rcx, 0 \n mov [{}], rcx \n".format(ident)
    INCR = lambda ident : "mov rcx, [{}] \n add rcx, 1 \n mov [{}], rcx \n".format(ident, ident)
    DECR = lambda ident : "mov rcx, [{}] \n sub rcx, 1 \n mov [{}], rcx \n".format(ident, ident)
    COPY = lambda id0, id1 : "mov rcx, [{}] \n mov [{}], rcx \n".format(id0, id1)
    PRINT = lambda idName, id: "mov rdi, fmt \n mov rsi, {} \n mov rdx, [{}] \n mov rax, 0 \n call printf \n".format(idName, id)
    ENDFILE = "pop rbp \n mov rax, 0 \n ret"

class Build(enum.Enum):
    STASEG = 0
    GENERALSTA = 1
    WHILE = 2

class NodeInfo(enum.Enum):
    STASEG = 0
    WHILE = 1
    CONDITION = 2
    CLEAR = 3
    INCR = 4
    DECR = 5
    COPY = 6

class Reserved(enum.Enum):
    ID = 0
    CLEAR = 1
    INCR = 2
    DECR = 3
    COPY = 4
    TO = 5
    WHILE = 6
    NOT = 7
    DO = 8
    END = 9
    SEMICOLON = 10
    ZERO = 11
