import sysv_ipc
from multiprocessing import Process
import time
import random
import re
class homeProcess(Process):
	def __init__(self,home_id,energy):
		super().__init__()
		self.home_id=home_id
		self.energy=energy
	def sendall(self,home_id):
		key=self.home_id
		try:
			queue3= sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
		except sysv_ipc.ExistentialError:
			print("connection exist ", key)
			queue3= sysv_ipc.MessageQueue(key)
	
		for i in range(5):
			if i!=key and i!=0:
				try:
					queue= sysv_ipc.MessageQueue(i)
					#print(f"home {home_id} connection success home {i}")
				except sysv_ipc.ExistentialError:
					print(f"sendall home {home_id} connection n'exist pas avec home {i}")
					continue
				#send to other home to indique source home has no energy
				hint="energy non plus"
				message=hint.encode()
				queue.send(message,type=2)
			
	def run (self):
		key=self.home_id
		print(f"\nhome {self.home_id} start...")
		try:
			queue= sysv_ipc.MessageQueue(key)
		except sysv_ipc.ExistentialError:
			print("connection exist ", key)
			queue= sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
		
		if self.energy==10:
			i=0
			self.sendall(self.home_id)
			while i<4:	
				i+=1 
				#send to other home to indique other source home it is a home 0 
				hint="home 0"
				message=hint.encode()
				queue.send(message,type=1)	
			
		elif self.energy > 10:
			# check other homes if they need energy
			for i in range(5):
				if i!=key and i!=0:
					try:
						queue2= sysv_ipc.MessageQueue(i)
						print(f"home {self.home_id} connection success home {i}")
					except sysv_ipc.ExistentialError:
						print(f"home {home_id} connection n'exist pas avec home {i}")
						continue

					#tell other source it's also a source home
					for j in range(4):
						#send type1 message to other source home to skip this queue
						sc="source also"
						queue.send(sc.encode(), type=1)
				
					# Receive response from other home
					response,t = queue2.receive(type=1)
					message=response.decode()
				
					if "home 0" in message:
						print(f"home {self.home_id} said home {i} is home 0")
						continue

					if "source also" in message:
						print(f"home {self.home_id} said home {i} is source")
						continue
					elif "no need" in message:
						print(f"home {self.home_id} said home{i} don't need energy anymore")
						continue
					else:
						# Send energy to the needed home
						print(f"home {self.home_id} received home {i} : {message}")
						energy_needed = int(message.split(" ")[-1])
						
						energy_extra=self.energy-10
						if self.energy-10> energy_needed:
							message=str(energy_needed).encode()
							queue2.send(message,type=2)
							self.energy-=energy_needed
							print (f"home {self.home_id} send {energy_needed} units of energy to home {i}")
							print (f"home {self.home_id} remain {self.energy} units of energy")
						
						else:
							message=str(energy_extra).encode()
							queue2.send(message,type=2)
							self.energy=10
							print (f"home {self.home_id} send {energy_extra} units of energy to home {i}")
							print (f"home {self.home_id} remain {self.energy} units of energy")
							print (f"home {self.home_id} don't have extra energy")
							self.sendall(self.home_id)
			#tell other home it has no extra energy at all
			if self.energy ==10:
				self.sendall(self.home_id)	
		else:
			self.sendall(self.home_id)
			print(f"home {self.home_id} sendall")
			counter=0
			nbsource=0
			while self.energy<10 and counter<3:
				#step 1: send in its own queue to tell "it need energy"
				message="I need energy "+ str(10-self.energy)
				queue.send(message.encode(),type=1)
				print(f"home {self.home_id} message sent into its queue: energy_needed={10-self.energy}")
				
				#Receive energy from other home
				#print(f"home {self.home_id} waiting type2")
				answer,t= queue.receive(type=2)
				an=answer.decode()
				
				#count to exit while if all home has no extra energy
				while  "energy non plus" in an and counter < 3:
					counter+=1	
					print(f"home {self.home_id} counter={counter}")
					if counter<3:
						print(f"home {self.home_id} continue to wait...")
						answer,t= queue.receive(type=2)
					an=answer.decode()

				print(f"home {self.home_id} receive  __{an}")
				value = an.split(" ")[0]

				if "energy" not in value:
					nbsource+=1
					self.energy+=int(value)							

				print (f"home {self.home_id} remain {self.energy} units of energy")
				
			#send type1 message to other source home it has enough energy
			k=1
			while k<=4:
				noneed="no need"
				queue.send(noneed.encode(), type=1)
				k+=1
		
		print(f"home {self.home_id} process end")
		print(f"final {self.home_id} = {self.energy}")
		print(f"home {self.home_id} energyNeedToTrade = {self.energy-10}")

		
if __name__=="__main__":
	energy = [random.randint(-10, 20) for _ in range(4)]
	for i in range(4):
		print(f"home {i+1} init={energy[i]}")
	for key in [1,2,3,4]:
		try:
			queue= sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
			print(f"message queue {key} created!!!")
		except sysv_ipc.ExistentialError:
			print("connection exist ", key)
			queue= sysv_ipc.MessageQueue(key)
			queue.remove()
			queue= sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
	#clear all messages still remain in queue		
	while queue.current_messages:
		m, t = queue.receive()
		dm = m.decode()
		print(f"main process: message received: {dm}, type: {t}")
			
	home1_process = homeProcess(1,energy[0])
	home2_process = homeProcess(2,energy[1])
	home3_process = homeProcess(3,energy[2])
	home4_process = homeProcess(4,energy[3])
	home1_process.start()
	home2_process.start()
	home3_process.start()
	home4_process.start()
	home1_process.join()
	home2_process.join()
	home3_process.join()
	home4_process.join()
	for i in [1,2,3,4]:
		try:
			queue= sysv_ipc.MessageQueue(i)
			queue.remove()
			print(f"message queue {i} removed")
		except sysv_ipc.ExistentialError:
			print("connection n'exist ", i)			
		
