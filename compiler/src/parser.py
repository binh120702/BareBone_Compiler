""" 
CLEARIFY:
    <staSeg>: stament sequence
    <while>: while stament
    <generalSta>: generalStament
    <conSta>: conditional stament
    <null>: no stament 
RULES:
    <staSeg> = <while> + <staSeg> | <generalSta> + <staSeg> | <null>
    <while> = <conSta> + <staSeg> 
    <generalSta> = 
        <copy> + <id> + <to> + <id> + <semicolon> |
        <clear> + <id> + <semicolon> |
        <incr> + <id> + <semicolon> | 
        <decr> + <id> + <semicolon> 

"""
from const import *
from collections import defaultdict

class ParseTree:

    def __init__(self, tokenList = [], debugPosition = []):
        self.tokenList = tokenList
        self.debugPosition = debugPosition
        self.tokenCount = len(tokenList)
        self.edge = defaultdict(list)
        self.nodeInfo = defaultdict(list)
        self.nodeCount = 0
        self.current = 0

    def addEdge(self, u, v):
        self.edge[u].append(v)
    
    def addNode(self, type, parent = -1, arg1 = "", arg2 = ""):
        self.nodeInfo[self.nodeCount].append(type)
        if arg1 != "":
            self.nodeInfo[self.nodeCount].append(arg1)
        if arg2 != "":
            self.nodeInfo[self.nodeCount].append(arg2)
        if parent != -1 :
            self.addEdge(parent, self.nodeCount)
        self.nodeCount += 1

    def getCurrentToken(self, shift = 0):
        return self.tokenList[self.current + shift]

    def moveCurrent(self, shift):
        self.current += shift

    def treeBuild(self, buildType):
        tokenName = self.getCurrentToken()[0]
        tokenType = tokenName.value
        thisNode = self.nodeCount
        if buildType == Build.STASEG:
            self.addNode(NodeInfo.STASEG)
            # <staSeg> = <while> + <staSeg> | <generalSta> + <staSeg> | <null>
            while self.current < self.tokenCount:
                tokenName = self.getCurrentToken()[0]
                tokenType = tokenName.value
                if tokenType in range(1, 5):
                    self.addEdge(thisNode, self.treeBuild(Build.GENERALSTA))
                elif tokenType == 6:
                    self.addEdge(thisNode, self.treeBuild(Build.WHILE))
                else:
                    break

        elif buildType == Build.WHILE:
            # <while> = <conSta> + <staSeg> 
            self.addNode(NodeInfo.WHILE)
            if not self.firstWhileCheck():
                self.exitError()
            self.addNode(NodeInfo.CONDITION, parent = thisNode, arg1 = self.getCurrentToken(1)[1])
            self.moveCurrent(6)
            self.addEdge(thisNode, self.treeBuild(Build.STASEG))
            if not self.lastWhileCheck():
                self.exitError()
            self.moveCurrent(2)

        elif buildType == Build.GENERALSTA:
            if tokenName == Reserved.COPY:
                if not self.binaryGeneralCheck():
                    self.exitError()
                self.addNode(NodeInfo.COPY, arg1 = self.getCurrentToken(1)[1], arg2 = self.getCurrentToken(3)[1])
                self.moveCurrent(5)
            else:
                if not self.unaryGeneralCheck():
                    self.exitError()
                if tokenName == Reserved.CLEAR:
                    self.addNode(NodeInfo.CLEAR, arg1 = self.getCurrentToken(1)[1])
                elif tokenName == Reserved.INCR:
                    self.addNode(NodeInfo.INCR, arg1 = self.getCurrentToken(1)[1])
                elif tokenName == Reserved.DECR:
                    self.addNode(NodeInfo.DECR, arg1 = self.getCurrentToken(1)[1])           
                self.moveCurrent(3)

        return thisNode

    def unaryGeneralCheck(self):
        if self.current + 2 >= self.tokenCount or self.getCurrentToken(1)[0] != Reserved.ID:
            return False
        if self.getCurrentToken(2)[0] != Reserved.SEMICOLON:
            return False
        return True

    def binaryGeneralCheck(self):
        if self.current + 4 >= self.tokenCount or self.getCurrentToken(1)[0] != Reserved.ID:
            return False
        if self.getCurrentToken(2)[0] != Reserved.TO or self.getCurrentToken(3)[0] != Reserved.ID:
            return False
        if self.getCurrentToken(4)[0] != Reserved.SEMICOLON:
            return False
        return True

    def firstWhileCheck(self):
        if self.current + 7 >= self.tokenCount or self.getCurrentToken(1)[0] != Reserved.ID:
            return False
        if self.getCurrentToken(2)[0] != Reserved.NOT or self.getCurrentToken(3)[0] != Reserved.ZERO:
            return False
        if self.getCurrentToken(4)[0] != Reserved.DO or self.getCurrentToken(5)[0] != Reserved.SEMICOLON:
            return False
        return True

    def lastWhileCheck(self):
        if self.current + 1 >= self.tokenCount or self.getCurrentToken(0)[0] != Reserved.END:
            return False
        if self.getCurrentToken(1)[0] != Reserved.SEMICOLON:
            return False
        return True
    
    def exitError(self):
        sys.exit(Error.INVALID_SYNTAX(self.debugPosition[self.current]))

    def buildCheck(self):
        if self.current != self.tokenCount:
            self.exitError()

def syntaxAnalyze(tokenList, debugPosition):
    myParseTree = ParseTree(tokenList, debugPosition)
    myParseTree.treeBuild(Build.STASEG)
    myParseTree.buildCheck()
    return myParseTree
