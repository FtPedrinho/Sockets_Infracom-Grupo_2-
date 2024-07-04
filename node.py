from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from random import randint

class Node():
    def __init__(self,id):
        # identificação, porta e thread pro servidor
        self.id = id
        self.porta = randint(200,50000)
        Thread(target=self.servidor).start()
        print(f'criado nó {self.id} com porta {self.porta}')

        # identifica as informações que cada nó tem
        self.hash = {}
    
    # ------------------------------    
    # funções de guardar data
    # ------------------------------    

    def put(self, data):
        self.data = data

    def vizinhos(self, nb):
        self.peers = nb

    # ------------------------------    
    # funções de request
    # ------------------------------    

    def get(self, id):
        # DFS em rede (a fazer)
        pass

    def transverse(self, master):
        # DFS em rede parte 2
        for port in self.peers:
            self.enviar(f'GET {master}', port)

    # ------------------------------    
    # funcionalidades nativas do p2p
    # ------------------------------  
      
    def HandleRequest(self, mClientSocket, mClientAddr):
        data = mClientSocket.recv(2048)

        req = data.decode()
        print(f'A requisição foi:{req}')
        rep = '200 ok'
        mClientSocket.send(rep.encode())

        # encoding adicional

        if req.split(" ")[0] == 'GET':
            self.enviar(f'DATA {self.data}', int(req.split(" ")[1]))

        if req.split(" ")[0] == 'DATA':
            self.hash[mClientAddr[1]] = " ".join(req.split(" ")[1:])

    def servidor(self):
        SocketServer = socket(AF_INET, SOCK_STREAM)
        mSocketServer = socket(AF_INET, SOCK_STREAM)
        mSocketServer.bind(('localhost',self.porta))
        mSocketServer.listen()
        while True:
            clientSocket, clientAddr =  mSocketServer.accept()
            #print(f'O servidor aceitou a conexão do Cliente: {clientAddr}')
            Thread(target=self.HandleRequest, args=(clientSocket, clientAddr)).start()

    def enviar(self, message, port):
        mClientSocket = socket(AF_INET, SOCK_STREAM)
        mClientSocket.connect(('localhost', port))
        mClientSocket.send(message.encode())
        data = mClientSocket.recv(2048)
        reply = data.decode()
        print(f'Resposta recebida:{reply}')



 
