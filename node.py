from socket import socket, AF_INET, SOCK_STREAM 
from threading import Thread 
from random import randint 
from hashlib import sha1  
import os  

class Node():
    
    def __init__(self, id):
        
        # Inicialização do nó com um identificador único e porta aleatória
        
        self.id = id
        self.porta = randint(200, 50000)
        
        self.filename = ''
        self.data = ''
        self.pasta = f'no{id+1}/'  # Diretório específico para o nó
        self.peers = None  # Vizinhos do nó
        
        # Inicia uma thread para o servidor
        Thread(target=self.servidor).start()
        print(f'criado nó {self.id} com porta {self.porta}')
        
        self.files = {}  # files[hash do arquivo] = nome_do_arquivo.txt
        self.hash = {}  # Armazena hash de arquivos de outros nós
        try:
            os.mkdir(self.pasta)  # Cria o diretório do nó
        except:
            pass
    
    # ------------------------------    
    # Funções de guardar data
    # ------------------------------    


    def PUT(self, data):
        self.make_file(data)  # Cria um arquivo com dados aleatórios
        self.get_files()  # Atualiza a lista de arquivos do nó


    def GET(self, id):
        try:
            if id in self.files.keys():
                return self.files[id]  # Retorna o arquivo se ele existir no nó (não acontece por enquanto)
            else:
                no_com_arquivo = int(self.hash[id])
                self.enviar(f'GET {id} {self.porta}', no_com_arquivo)  # Pede o arquivo, manda o hash do arquivo, a porta do nó que tá pedindo para o nó que possui o arquivo
        except Exception as e:
            print(e)


    def vizinhos(self, nb):
        self.peers = nb  # Define os vizinhos do nó


    def encode(self, string):
        return sha1(string.encode()).hexdigest()  # Processo de gerar os hashes dos arquivos
    

    def get_files(self):
        files = os.listdir(self.pasta)  # Lista todos os arquivos no diretório do nó
        for file in files:
            self.files[self.encode(file)] = file  # Atualiza o dicionário de arquivos com seus hashes
    

    def make_file(self, data):
        with open(f'{self.pasta}/{data}', 'w') as arquivo:
            for _ in range(128):
                arquivo.write(f'{randint(0,9)}')  # Escreve dados aleatórios no arquivo

    # ------------------------------    
    # Funções de request
    # ------------------------------    


    def get_info(self, master):
        self.enviar(f'INFO {master}', self.peers[1])  # Gira de maneira circular, pede informações para TODOS os nós


    # ------------------------------    
    # Funcionalidades nativas do p2p
    # ------------------------------  
      

    def HandleRequest(self, mClientSocket, mClientAddr):
        data = mClientSocket.recv(2048)  # Recebe dados do cliente
        req = data.decode()  # Decodifica a requisição
        rep = '200 ok'
        mClientSocket.send(rep.encode())  # Envia resposta para o cliente

        tipo = req.split(" ")[0]  # Pega o tipo da requisição


    #-----------------------------
    # Tipos de requisição
    #-----------------------------


        if tipo == 'GET':
            self.send_file(int(req.split(" ")[2]), req.split(" ")[1])  # Entra aqui em um self.get(), ele puxa a função de enviar arquivo, enviando o hash e a porta


        if tipo == 'INFO': # Entra aqui em um get_info()
            portamaster = int(req.split(" ")[1])
            porta_sua = self.porta
            if portamaster != porta_sua:
                for key in self.files.keys():
                    self.enviar(f'DATA {key} {porta_sua}', int(req.split(" ")[1]))  # Envia dados para o nó que pediu as informações
                self.get_info(int(req.split(" ")[1])) # Repassa a chamada para o próximo nó


        if tipo == 'DATA':
            self.hash[req.split(" ")[1]] = req.split(" ")[2]  # Atualiza a hash table do nó


        if tipo == 'FILE':
            filename = req.split(" ")[1]
            self.receive_file(mClientSocket, filename)  # Recebe o arquivo


    def servidor(self):
        SocketServer = socket(AF_INET, SOCK_STREAM)  
        mSocketServer = socket(AF_INET, SOCK_STREAM)
        mSocketServer.bind(('localhost', self.porta))  
        mSocketServer.listen()  
        while True:
            clientSocket, clientAddr = mSocketServer.accept()  
            Thread(target=self.HandleRequest, args=(clientSocket, clientAddr)).start()


    def enviar(self, message, port):
        mClientSocket = socket(AF_INET, SOCK_STREAM)
        mClientSocket.connect(('localhost', port))  
        mClientSocket.send(message.encode()) 
        data = mClientSocket.recv(2048)  
        reply = data.decode()


    def receive_file(self, mClientSocket, filename):
        with open(self.pasta + filename, 'wb') as f:
            while True:
                bytes_read = mClientSocket.recv(4096)
                if not bytes_read:
                    break
                f.write(bytes_read)
        print(f'Arquivo {filename} recebido com sucesso')
    
    
    def send_file(self, port, hashed):
        filepath = self.pasta + self.files[hashed]
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
