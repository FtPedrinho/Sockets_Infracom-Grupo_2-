from node import Node
import time

class DHT():
    def __init__(self):

        # serve como table porém é melhor usar hash
        self.nos = [Node(i) for i in range(5)]

        # <-> Nó 1 <-> Nó 2 <-> Nó 3 <-> Nó 4 <-> Nó 5 <-> 
        for no in self.nos:
            no.vizinhos([self.nos[(no.id-1)%5].porta,self.nos[(no.id+1)%5].porta])

    def add(self):
        self.nos.append(Node(len(self.nos)))
        for no in self.nos:
            no.vizinhos([self.nos[(no.id-1)%len(self.nos)].porta,self.nos[(no.id+1)%len(self.nos)].porta])
        
pega = DHT()
for no in pega.nos:
    for i in range(2):
        no.PUT(f'pegamovel{i+no.porta}.txt')

for no in pega.nos:
    print(f'{no.id} CHAMADAS:')
    no.get_info(no.porta)