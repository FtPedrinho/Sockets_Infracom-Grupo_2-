from socket import socket, AF_INET, SOCK_STREAM 
from threading import Thread 
from random import randint 
from hashlib import sha1  
import os, time

class Node():
    
    def __init__(self, id):
        
        # Inicialização do nó com um identificador único e porta aleatória
        
        self.id = str(id)
        self.porta = randint(200, 50000)
        self.pasta = f'no{id}/'  # Diretório específico para o nó
        self.fingertable = []
        self.peers = None

        # Inicia uma thread para o servidor
        Thread(target=self.servidor).start()
        print(f'criado nó {self.id} com porta {self.porta}')
        
        self.portdecode = {} # Armazena as portas dos nós na finger table, o forrmato é portdecode[id] = porta
        self.files = {}  # files[hash do arquivo] = nome_do_arquivo.txt
        self.hash = {}  # Armazena hash de arquivos de outros nós
        self.set_fingertable()

        try:
            os.mkdir(self.pasta)  # Cria o diretório do nó
        except:
            pass
            
    
    # ------------------------------    
    # Setar os vizinhos
    # ------------------------------  

    def vizinhos(self, nb):
        self.peers = nb

    def set_fingertable(self):
        n = int(self.id)
        for i in range(4):
            adicionar = (n+2**i)%5
            if adicionar == 0:
                adicionar = 5
            self.fingertable.append(str(adicionar))

    # ------------------------------    
    # Funções de guardar data
    # ------------------------------   

    def PUT(self, data):

        self.make_file(data)  # Cria um arquivo com dados aleatórios

        diretorio_arquivo = f'{data}'
        hash_arquivo = self.encode(diretorio_arquivo)
        self.files[hash_arquivo] = diretorio_arquivo

        self.enviar(f'NEWFILE {self.id} {hash_arquivo}',self.peers[1]) #comunica a todos os nós que um arquivo novo chegou
        print(f'Arquivo {data} foi criado com hash {hash_arquivo}')

    def GET(self, hash_do_arquivo):
        #try:

            no_com_arquivo = hash_do_arquivo[0]
            self.enviar(f'GET {hash_do_arquivo} {self.porta} {time.time()}', self.portdecode[no_com_arquivo])  # Pede o arquivo, manda o hash do arquivo, a porta do nó que tá pedindo para o nó que possui o arquivo

        #except Exception as e:
            #print(e)

    def encode(self, string):
        return self.id+sha1(string.encode()).hexdigest()  # Processo de gerar os hashes dos arquivos, o primeiro byte é o id do nó
    
    def make_file(self, data):
        with open(f'{self.pasta}/{data}', 'w') as arquivo:
            for _ in range(128):
                arquivo.write(f'{randint(0,9)}')  # Escreve dados aleatórios no arquivo

    def ports_update(self):
        self.enviar(f'REQUESTING {",".join(self.fingertable)} {self.porta}',self.peers[1])

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

        if tipo == 'NEWFILE':

            id_do_no = req.split(" ")[1]
            if id_do_no != self.id:

                hash_arquivo = req.split(" ")[2]

                self.hash[hash_arquivo] = id_do_no

                self.enviar(req,self.peers[1])

        if tipo == 'GET':

            hash = req.split(" ")[1]
            porta = int(req.split(" ")[2])
            tempo = req.split(" ")[3]

            self.send_file(porta, hash, tempo)  # Entra aqui em um self.get(), ele puxa a função de enviar arquivo, enviando o hash e a porta

        if tipo == 'FILE':

            filename = req.split(" ")[1]

            self.receive_file(mClientSocket, filename)  # Recebe o arquivo

        if tipo == 'REQUESTING':

            nos_da_ft = req.split(" ")[1].split(",")
            porta_da_req = int(req.split(" ")[2])

            if self.id in nos_da_ft: # Checa pra ver se é pra retornar o hi
                self.enviar(f'HI {self.id} {self.porta}', porta_da_req)
                self.enviar(req, self.peers[1]) # Repassa a mensagem

        if tipo == 'HI':

            id = req.split(" ")[1]
            porta = req.split(" ")[2]

            self.portdecode[id] = int(porta)


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
        #print(f'Arquivo {filename} recebido com sucesso')
    
    
    def send_file(self, port, hashed, tempo):
        filepath = self.pasta+self.files[hashed]
        mClientSocket = socket(AF_INET, SOCK_STREAM)
        mClientSocket.connect(('localhost', port))
        
        filename = os.path.basename(filepath)
        mClientSocket.send(f'FILE {filename}'.encode())
        data = mClientSocket.recv(2048)
        reply = data.decode()
        #print(f'Resposta recebida:{reply}')

        with open(filepath, 'rb') as f:
            while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break
                mClientSocket.sendall(bytes_read)

        mClientSocket.close()
        print(f'O arquivo {self.files[hashed]} demorou {(time.time()-float(tempo))*1000} ms para ser recebido com dht\n')
