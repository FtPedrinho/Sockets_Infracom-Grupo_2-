from node import Node
import time

class DHT():
    def __init__(self):

        # serve como table porém é melhor usar hash
        self.nos = [Node(i) for i in range(5)]

        # <-> Nó 1 <-> Nó 2 <-> Nó 3 <-> Nó 4 <-> Nó 5 <-> 
        for no in self.nos:
            no.vizinhos([self.nos[(no.id-1)%5].porta,self.nos[(no.id+1)%5].porta])
        
        self.nos[0].put('File 1')
        self.nos[1].put('File 2')
        self.nos[2].put('File 3')
        self.nos[3].put('File 4')
        self.nos[4].put('File 5')
    

    def add(self):
        self.nos.append(Node(len(self.nos)))
        for no in self.nos:
            no.vizinhos([self.nos[(no.id-1)%len(self.nos)].porta,self.nos[(no.id+1)%len(self.nos)].porta])
        
pega = DHT()

for no in pega.nos:
    no.get_info(no.porta)
    print()

time.sleep(1)
print("INFORMAÇÕES RECEBIDAS: (PORTA : INFORMAÇÃO GUARDADA)")
for no in pega.nos:
    print(f'Nó {no.id}')
    print(no.hash)
    print()
