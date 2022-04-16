import subprocess

def codeRun(asmSource):
    asmFile = open("./compiler/tmp/newNASM.asm", "w")
    asmFile.write(asmSource)    
    asmFile.close()  
    subprocess.call("nasm -f elf64 ./compiler/tmp/newNASM.asm", shell=True)
    subprocess.call("gcc -no-pie -o ./compiler/tmp/demo ./compiler/tmp/newNASM.o", shell=True)
    subprocess.call("./compiler/tmp/demo", shell=True)