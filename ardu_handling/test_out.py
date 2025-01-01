import serial as sr
import time
adresy_COM = ['COM9']
PRINT = False

def _send():
    _sendLine("$$$$CC##aB&&##bB&&##cD&&##dE&&CC##eB&&##f3&&##gD&&##hB&&CC##iF&&##jF&&##k7&&##lF&&LL##a6&&##b5&&##c7&&##d7&&LL##eB&&##fB&&##gD&&##hF&&LL##i7&&##jB&&##kD&&##lF&&PP##aC&&##bB&&##cD&&##dF&&PP##eB&&##fB&&##gD&&##hB&&PP##iF&&##jF&&##k7&&##lF&&PP##mF&&##nB&&##oD&&##pF&&ZZZZ")
    time.sleep(2)
    _sendLine("$$$$CC##aD&&##bD&&##cB&&##d7&&CC##eD&&##fC&&##gB&&##hD&&CC##iF&&##jF&&##kE&&##lF&&LL##a^&&##bA&&##cE&&##dE&&LL##eD&&##fD&&##gB&&##hF&&LL##iE&&##jD&&##kB&&##lF&&PP##aD&&##bD&&##cB&&##d0&&PP##eD&&##fD&&##gB&&##hD&&PP##iF&&##jF&&##kE&&##lF&&PP##mF&&##nD&&##oB&&##pF&&ZZZZ")
    time.sleep(2)

def _sendLine(x):
    ready_code = x
    #ready_code = ready_code.encode()
    for x in adresy_COM:
        x = sr.Serial(x, 115200)#, timeout=0.1)
        #x.write(ready_code)
        k = 5
        r = len(ready_code)%k
        for n in range(r): ready_code+='Z'
        for n in range(0, len(ready_code),k):
            try:
                toWrite = ''
                for m in range(k):
                    toWrite+=ready_code[n+m]
                x.write(toWrite.encode())
                time.sleep(0.001)
                if PRINT: print(toWrite)
            except: pass

        #x.write(ready_code)
        x.close()
    #print(ready_code)

while True:
    _send()

