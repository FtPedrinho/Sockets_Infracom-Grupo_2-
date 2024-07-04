from node import Node
import time

class DHT():
    def __init__(self):

        # serve como table porém é melhor usar hash
        self.nos = [Node(i) for i in range(5)]

        # <-> Nó 1 <-> Nó 2 <-> Nó 3 <-> Nó 4 <-> Nó 5 <-> 
        for no in self.nos:
            no.vizinhos([self.nos[(no.id-1)%5].porta,self.nos[(no.id+1)%5].porta])
        
        self.nos[0].put('senhas cartao de credito marciano')
        self.nos[1].put('arquivos exposed arthur couto')
        self.nos[2].put('tiktoks pedrelias')
        self.nos[3].put('album novo da taylor')
        self.nos[4].put('vazamento prova 2 infrahard')
        
pega = DHT()

for no in pega.nos:
    no.transverse(no.porta)
    print()

time.sleep(3)
print("INFORMAÇÕES RECEBIDAS: (PORTA : INFORMAÇÃO GUARDADA)")
for no in pega.nos:
    print(f'Nó {no.id}')
    print(no.hash)
    print()
