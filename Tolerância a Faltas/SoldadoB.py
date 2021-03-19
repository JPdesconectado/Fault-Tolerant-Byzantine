import socket 
import threading 
import time

HOST = '127.0.0.1'
IDPORT = 4000
IDGEN = 2000
Soldiers = [3000, 5000, 6000]
Values = []

class Saldo(object):
    def __init__(self, valor):
        self._saldo = valor

class Confirmado(object):
    def __init__(self, valor):
        self._confirmado = valor

def serverThread():
    addr = (HOST, IDPORT) 
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_socket.bind(addr) 
    serv_socket.listen()
    while True:
        con, port = serv_socket.accept() 
        try:
            while True:
                msg = con.recv(1024) 
                if not msg: break

                getID, getOP, getVal = infos(msg)

                if(getOP == "CRÉDITO"):
                    print("Crédito.")
                    saldo._saldo += int(getVal)
                    sendComparacao(getID)   
          
                elif(getOP == "DÉBITO"):
                    print("Débito.")
                    saldo._saldo -= int(getVal)
                    sendComparacao(getID)

                elif(getOP == "COMPARAÇÃO"):
                    compare(getID, getVal)

        finally:
            con.close()

def infos(msg):
    var = msg.decode().split(":")
    getID= var[0]
    getOP = var[1]
    getVal = var[2]
    return getID, getOP, getVal

def sendComparacao(getID):
    mensagem = getID + ":COMPARAÇÃO:" + str(saldo._saldo)
    for soldier in Soldiers:
        tt = threading.Thread(target = comparationThread, args=[soldier, mensagem])
        tt.start()

def compare(getID, getVal):
    Values.append(int(getVal))
    if (len(Values) == 3):
        for val in Values:
            if (val == saldo._saldo):
                conf._confirmado += 1
        if (conf._confirmado == 3):
            mensagem = str(getID) + ":OK:" + str(saldo._saldo)
            print("OK")
            tt = threading.Thread(target = informThread, args=[2000, mensagem])
            tt.start()
            Values.clear()
            conf._confirmado = 0
        else:
            mensagem = str(getID) + ":ERRO:" + str(saldo._saldo)
            print("ERRO")
            tt = threading.Thread(target = informThread, args=[2000, mensagem])
            tt.start()    
            Values.clear()
            conf._confirmado = 0 

def test_con(s, PORT):
    try:
       return s.connect((HOST, PORT))
    except:
        test_con(s, PORT)

def comparationThread(PORT, mensagem):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        test_con(s, PORT)
        s.sendall(mensagem.encode('utf-8'))

def informThread(PORT, mensagem):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        test_con(s, PORT)
        s.sendall(mensagem.encode('utf-8'))

saldo = Saldo(0)
conf = Confirmado(0)

def Main():

    saldo._saldo = 0
    conf._confirmado = 0
    tw = threading.Thread(target=serverThread)
    tw.start()


if __name__ == '__main__': 
    Main()     