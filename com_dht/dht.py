from node import Node
import time

class DHT():
    def __init__(self):

        self.nos = [Node(i+1) for i in range(5)]

        for no in self.nos:
            no.vizinhos([self.nos[(int(no.id)-2)%5].porta,self.nos[(int(no.id))%5].porta])
        
dht = DHT()

for no in dht.nos:
     no.ports_update()
time.sleep(0.3)

no_1 = dht.nos[0]
no_2 = dht.nos[1]
no_3 = dht.nos[2]
no_4 = dht.nos[3]
no_5 = dht.nos[4]

no_1.PUT('arquivo1.txt')
no_3.PUT('arquivo3.txt')
no_4.PUT('arquivo4.txt')
arquivo_1_hash = no_1.encode('arquivo1.txt')
arquivo_3_hash = no_3.encode('arquivo3.txt')
arquivo_4_hash = no_4.encode('arquivo4.txt')

print('-'*32)
print('\n Requisições no nó 1 \n')
print('-'*32)

no_2.GET(arquivo_1_hash)
time.sleep(0.1)
no_3.GET(arquivo_1_hash)
time.sleep(0.1)
no_4.GET(arquivo_1_hash)
time.sleep(0.1)
no_5.GET(arquivo_1_hash)
time.sleep(0.1)

print('-'*32)
print('\n Requisições no nó 3 \n')
print('-'*32)

no_1.GET(arquivo_3_hash)
time.sleep(0.1)
no_2.GET(arquivo_3_hash)
time.sleep(0.1)
no_4.GET(arquivo_3_hash)
time.sleep(0.1)
no_5.GET(arquivo_3_hash)
time.sleep(0.1)

print('-'*32)
print('\n Requisições no nó 4 \n')
print('-'*32)

time.sleep(0.1)
no_1.GET(arquivo_4_hash)
time.sleep(0.1)
no_2.GET(arquivo_4_hash)
time.sleep(0.1)
no_3.GET(arquivo_4_hash)
time.sleep(0.1)
no_5.GET(arquivo_4_hash)
time.sleep(0.1)





