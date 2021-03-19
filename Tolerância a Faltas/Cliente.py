import socket 
import threading 

HOST = '127.0.0.1'
IDPORT = 1000

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

                if (getOP == "OK"):
                    print("\nRecebido. Operação:", getID, "Saldo:", int(getVal))
                    break
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

def sendOperation(PORT, mensagem):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        test_con(s, PORT)
        s.sendall(mensagem.encode('utf-8'))
        


def Main(): 
    tw = threading.Thread(target=serverThread)
    tw.start()
    primary = 2000
    idop = 1
    while True:

        print("---------- Menu ----------\n")
        print("(1) Crédito:")
        print("(2) Débito:")
        print("(3) Sair.")
        print("--------------------------\n")
        opcao = int(input("Escolha:"))

        if(opcao == 1):
            decisao = int(input("Valor:"))
            mensagem = str(idop) + ":" + "CRÉDITO:" + str(decisao)
            th = threading.Thread(target = sendOperation, args=[primary, mensagem])
            th.start()
            print("Enviado. Operação:", str(idop), "Saldo:", str(decisao))
            idop +=1

        elif(opcao == 2):
            decisao = int(input("Valor:"))
            mensagem = str(idop) + ":" + "DÉBITO:" + str(decisao)
            th = threading.Thread(target = sendOperation, args=[primary, mensagem])
            th.start()
            idop +=1

        elif(opcao == 3):
            break

        else:
            break        

if __name__ == '__main__': 
    Main()     