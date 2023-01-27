from multiprocessing import Process
#import socket
import time

class MarketProcess(Process):
	def receiveHome(self):
		HOST="localhost"
		PORT=6666
		import socket
		with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_socket:
			server_socket.bind((HOST,PORT))
			server_socket.listen(1)
			client_socket, address = server_socket.accept()
			with client_socket:
				#print("Connected to client: ", address)
				data = client_socket.recv(1024)
				while len(data):
					client_socket.sendall(data)
					data = client_socket.recv(1024)
				#print("Disconnecting from client: ", address)
					
	
	def run (self):
		while True:
			self.receiveHome()

class HomeProcess(Process):
	def sendToMarket(self):
		HOST = "localhost"
		PORT = 6666
		import socket
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
			client_socket.connect((HOST, PORT))
			m = "1233221"
			#boucle infini et envoyer toutes les secondes
			while True:
				client_socket.sendall(m.encode())
				data = client_socket.recv(1024)
				print("echo> ", data.decode())
				time.sleep(1)
       			
	
	def run (self):
		while True:
			self.sendToMarket()
			#time.sleep(1)
			

if __name__=="__main__":
	
	
	home1=HomeProcess()
	
	market=MarketProcess()
	
	market.start()
	
	home1.start()
	
	market.join()
	
	home1.join()
	
	
	
	
			
		
