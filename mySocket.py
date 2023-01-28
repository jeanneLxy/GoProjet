from multiprocessing import Process
import threading
#import socket
import time
#from queue import Queue

class MarketProcess(Process):
	def __init__(self):
		super().__init__()
		self.total=0
	
	def run (self):
		#def receiveHome():
			#global totalEnergy=100
			#total=100
			
			#les threads de marché, recevoir les énergies non utilisées des familles
			def client_handler(s,a):#socket,address,queue
				with s:
					data=s.recv(1024)
					global total			
					while len(data):
						s.sendall(data)
						#time.sleep(1)
						data=s.recv(1024)
						#print(threading.get_ident())
						print(data.decode())
						totalEnergy=int(data.decode())
						self.total+=totalEnergy
						#q.put(totalEnergy)
						#time.sleep(1)
						print("total in market:",self.total)
						
			
			HOST="localhost"
			PORT=6666
			import socket
			with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_socket:
				server_socket.bind((HOST,PORT))
				server_socket.listen(5)
				while True:
					client_socket,address=server_socket.accept()
					queue1=Queue()
					queue2=Queue()
					th=threading.Thread(target=client_handler,args=(client_socket,address))
					th1=threading.Thread(target=client_handler,args=(client_socket,address))
					#th1=threading.Thread(target=receiveHome,args=())
					th.start()
					th1.start()	
					#th.join()
					#print("receive q1: ",queue1.get())
					#print("receive q2: ",queue2.get())
					#total+=queue1.get()+queue2.get()
					#print(total)
					
				#client_socket, address = server_socket.accept()
				#with client_socket:
					#print("Connected to client: ", address)
				#	data = client_socket.recv(1024)
				#	while len(data):
				#		client_socket.sendall(data)
				#		data = client_socket.recv(1024)
					#print("Disconnecting from client: ", address)
		
		#th1.join()
		#receiveHome(self)
		#while True:
		
		#	receiveHome(self)

class HomeProcess(Process):
	def sendToMarket(self):
		HOST = "localhost"
		PORT = 6666
		import socket
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
			client_socket.connect((HOST, PORT))
			m =1
			#boucle infini et envoyer toutes les secondes
			#while len(m)<10:
			while True:
				client_socket.sendall(str(m).encode())
				data = client_socket.recv(1024)
				#print("echo> ", data.decode())
				time.sleep(1)
				m+=1
	
	def run (self):
		while True:
			self.sendToMarket()
			#time.sleep(1)
			

if __name__=="__main__":
	
	
	home1=HomeProcess()
	home2=HomeProcess()
	
	market=MarketProcess()
	
	market.start()
	
	home1.start()
	home2.start()
	
	market.join()
	
	home1.join()
	
	home2.join()
	
	
			
		
