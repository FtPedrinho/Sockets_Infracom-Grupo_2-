from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from random import randint
import os

class Node():
    def __init__(self,id):
        # identificação, porta e thread pro servidor
        self.id = id
        self.porta = randint(200,50000)
        self.filename = ''
        self.data = ''
        self.pasta = f'no{id+1}/'
        self.peers = None
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

    # Pega informações dos vizinhos.

    def transverse(self, master):
        # DFS em rede parte 2
        for port in self.peers:
            self.enviar(f'GET {master} ', port)

    # Pega informações de todos os nós em ordem crescente

    def get_info(self, master):
        self.enviar(f'INFO {master}',self.peers[1])

    # ------------------------------    
    # funcionalidades nativas do p2p
    # ------------------------------  
      
    def HandleRequest(self, mClientSocket, mClientAddr):
        data = mClientSocket.recv(2048)
        req = data.decode()
        print(f'A requisição foi:{req}')
        rep = '200 ok'
        mClientSocket.send(rep.encode())

        tipo = req.split(" ")[0]
        if tipo == 'GET':
            self.enviar(f'DATA {self.data}', int(req.split(" ")[1]))

        if tipo == 'INFO':
            if int(req.split(" ")[1]) != self.porta:
                self.enviar(f'DATA {self.data}', int(req.split(" ")[1]))
                self.get_info(int(req.split(" ")[1]))

        if tipo == 'DATA':
            self.hash[mClientAddr[1]] = " ".join(req.split(" ")[1:])

        if tipo == 'FILE':
            filename = req.split(" ")[1]
            self.receive_file(mClientSocket, filename)

        

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

    def receive_file(self, mClientSocket, filename):
        with open(self.pasta+filename, 'wb') as f:
            while True:
                bytes_read = mClientSocket.recv(4096)
                if not bytes_read:
                    break
                f.write(bytes_read)
        print(f'Arquivo {filename} recebido com sucesso')
    
    def send_file(self, port):
        filepath = self.pasta+self.filename
        mClientSocket = socket(AF_INET, SOCK_STREAM)
        mClientSocket.connect(('localhost', port))
        
        filename = os.path.basename(filepath)
        mClientSocket.send(f'FILE {filename}'.encode())
        data = mClientSocket.recv(2048)
        reply = data.decode()
        print(f'Resposta recebida:{reply}')

        with open(filepath, 'rb') as f:
            while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break
                mClientSocket.sendall(bytes_read)

        mClientSocket.close()

    



 
