from const import *

class assemblyBuilder():
    def __init__(self, parseTree):
        self.parseTree = parseTree
        self.asmSource = ""
        self.identifierLabel = {}
        self.orginalLabel = {}
        self.labelCount = 0

    def getNewLabel(self, key, reserve = 0):
        if not reserve:
            self.labelCount += 1
        return "Label_" + key + str(self.labelCount)

    def addToSource(self, str):
        self.asmSource += str

    def prepare(self):
        # labeling variables 
        for index in self.parseTree.nodeInfo:
            for id in self.parseTree.nodeInfo[index][1:]:
                if id not in self.identifierLabel:
                    self.identifierLabel[id] = self.getNewLabel("id")
                    self.orginalLabel[id] = self.getNewLabel("idOrigin", reserve=1)

        self.addToSource(Nasm.EXTENSION.value)
        self.addToSource(Nasm.DATA_SECTION_HEADER.value)
        self.addToSource(Nasm.DATA_SECTION_MESSAGE.value)
        for id in self.identifierLabel:
            self.addToSource(Nasm.DATA_SECTION_DECLARE(self.identifierLabel[id], 0))
            self.addToSource(Nasm.DATA_SECTION_DECLARE(self.orginalLabel[id], '"' + id + '"'))
        
        self.addToSource(Nasm.TEXT_SECTION_HEADER.value)
        self.addToSource(Nasm.GLOBAL_HEADER.value)

    def build(self, thisNode):
        nodeInfo = self.parseTree.nodeInfo[thisNode]
        nodeInfoType = nodeInfo[0] 

        if nodeInfoType == NodeInfo.STASEG:
            for child in self.parseTree.edge[thisNode]:
                self.build(child)
                
        elif nodeInfoType == NodeInfo.WHILE:
            thisBeginLabel = self.getNewLabel("while")
            thisEndLabel = self.getNewLabel("end_While", reserve=1)

            self.addToSource(Nasm.LABEL(thisBeginLabel))
            for child in self.parseTree.edge[thisNode]:
                self.build(child)
            self.addToSource(Nasm.JUMPTO(thisBeginLabel))
            self.addToSource(Nasm.LABEL(thisEndLabel))
            
        elif nodeInfoType == NodeInfo.CONDITION:
            ident = nodeInfo[1]
            thisEndLabel = self.getNewLabel("end_While", reserve=1)
            self.addToSource(Nasm.IFNOTZERO(self.identifierLabel[ident], thisEndLabel))

        elif nodeInfoType == NodeInfo.CLEAR:
            ident = nodeInfo[1]
            self.addToSource(Nasm.CLEAR(self.identifierLabel[ident]))
            
        elif nodeInfoType == NodeInfo.INCR:
            ident = nodeInfo[1]
            self.addToSource(Nasm.INCR(self.identifierLabel[ident]))
            
        elif nodeInfoType == NodeInfo.DECR:
            ident = nodeInfo[1]
            thisEndLabel = self.getNewLabel("end_decr")
            self.addToSource(Nasm.IFNOTZERO(self.identifierLabel[ident], thisEndLabel))
            self.addToSource(Nasm.DECR(self.identifierLabel[ident]))
            self.addToSource(Nasm.LABEL(thisEndLabel))

        elif nodeInfoType == NodeInfo.COPY:
            id0 = nodeInfo[1]
            id1 = nodeInfo[2]
            self.addToSource(Nasm.COPY(self.identifierLabel[id0], self.identifierLabel[id1]))

    def finish(self):
        for id in self.identifierLabel:
            self.addToSource(Nasm.PRINT(self.orginalLabel[id], self.identifierLabel[id]))
        self.addToSource(Nasm.ENDFILE.value)
            

def codeGenerate(parseTree):
    builder = assemblyBuilder(parseTree)
    builder.prepare()
    builder.build(0)
    builder.finish()
    return builder.asmSource

