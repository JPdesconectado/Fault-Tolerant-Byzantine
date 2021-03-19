import socket 
import threading 
import time

HOST = '127.0.0.1'
Client = 1000
IDPORT = 2000
Soldiers = [3000, 4000, 5000, 6000]

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
                    for soldier in Soldiers:
                        tt = threading.Thread(target = informThread, args=[soldier, msg.decode()])
                        tt.start()
          
                elif(getOP == "DÉBITO"):
                    print("Débito.")
                    saldo._saldo -= int(getVal)
                    for soldier in Soldiers:
                        tt = threading.Thread(target = informThread, args=[soldier, msg.decode()])
                        tt.start()                    
                    
                elif(getOP == "OK"):
                    conf._confirmado +=1

                    if (conf._confirmado == 4):
                        print("Cálculo OK.")
                        mensagem = getID + ":OK:" + str(saldo._saldo)
                        tt = threading.Thread(target = informThread, args=[Client, mensagem])
                        tt.start()
                        conf._confirmado = 0
                elif(getOP == "ERRO"):
                    conf._confirmado +=1
                    if (conf._confirmado == 4):
                        print("Não Houve Acordo.")     
                        conf._confirmado = 0
        finally:
            con.close()

def infos(msg):
    var = msg.decode().split(":")
    getID= var[0]
    getOP = var[1]
    getVal = var[2]
    return getID, getOP, getVal

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