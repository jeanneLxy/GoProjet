import sysv_ipc
from multiprocessing import Process,Value,Lock
import time
import random

class WeatherProcess(Process):
	def __init__(self):
		super().__init__()
		self.shared_memory = Value("d", 15)
		self.current_month= Value("d", 1)
		self.lock1 = Lock()
		self.lock2 = Lock()
	def run(self):
		while True:
			self.lock2.acquire()
			month=self.current_month.value
			self.lock2.release()
			
			# if main process make current_month plus de 12, reset to month 1
			if self.current_month.value>12:
				self.lock2.acquire()
				self.current_month.value = 1
				self.lock2.release()
				
			if month in range(1, 3):
				self.lock1.acquire()
				self.shared_memory.value = 15
				self.lock1.release()
			elif month in range(4, 6):
				self.lock1.acquire()
				self.shared_memory.value = 20
				self.lock1.release()
			elif month in range(7, 9):
				self.lock1.acquire()
				self.shared_memory.value = 25
				self.lock1.release()
			elif month in range(9, 12):
				self.lock1.acquire()
				self.shared_memory.value = 10
				self.lock1.release()
			elif month==0:
				break
		
	 


class homeProcess(Process):
	def __init__(self,home_id,energy,mode):
		super().__init__()
		self.home_id=home_id
		self.energy=energy
		self.mode=mode
	def sendall1(self,home_id):
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
		
		if self.energy.value==0:
			i=0
			self.sendall1(self.home_id)
			while i<4:	
				i+=1 
				#send to other home to indique other source home it is a home 0 
				hint="home 0"
				message=hint.encode()
				queue.send(message,type=1)	
			
		elif self.energy.value > 0:
			if self.mode[key-1]==1:		
				#(no need to send energy to others if it only trade with market)
				for j in range(4):
					#send type1 message to other source home to skip this queue
					sc="source also"
					queue.send(sc.encode(), type=1)
				print(f"home {self.home_id} energyNeedToTrade = {self.energy.value}")
				self.energy.value=0
			else:
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
							energy_needed = float(message.split(" ")[-1])
							
							energy_extra=self.energy.value
							if self.energy.value> energy_needed:
								message=str(energy_needed).encode()
								queue2.send(message,type=2)
								self.energy.value-=energy_needed
								print (f"home {self.home_id} send {energy_needed} units of energy to home {i}")
								print (f"home {self.home_id} remain {self.energy.value} units of energy")
							
							else:
								message=str(energy_extra).encode()
								queue2.send(message,type=2)
								self.energy.value=0
								print (f"home {self.home_id} send {energy_extra} units of energy to home {i}")
								print (f"home {self.home_id} remain {self.energy.value} units of energy")
								print (f"home {self.home_id} don't have extra energy")
			#tell other home it has no extra energy at all
			if self.energy.value ==0:
				self.sendall1(self.home_id)	
		else:
			#tell other source it no need for energy if it only trade with market
			if self.mode[key-1]==1:
				self.sendall1(self.home_id)
				#send type1 message to other source home it has enough energy
				k=1
				while k<=4:
					noneed="no need"
					queue.send(noneed.encode(), type=1)
					k+=1
				print(f"home {self.home_id} energyNeedToTrade = {self.energy.value}")
				self.energy.value=0	
			else:
				self.sendall1(self.home_id)
				print(f"home {self.home_id} sendall")
				counter=0
				nbsource=0
				while self.energy.value<0 and counter<3:
					#step 1: send in its own queue to tell "it need energy"
					message="I need energy "+ str(-self.energy.value)
					queue.send(message.encode(),type=1)
					print(f"home {self.home_id} message sent into its queue: energy_needed={-self.energy.value}")
					
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
						self.energy.value+=float(value)							

					print (f"home {self.home_id} remain {self.energy.value} units of energy")
					
				#send type1 message to other source home it has enough energy
				k=1
				while k<=4:
					noneed="no need"
					queue.send(noneed.encode(), type=1)
					k+=1
				print(f"home {self.home_id} energyNeedToTrade = {self.energy.value}")
		
		print(f"home {self.home_id} process end")
		print(f"final {self.home_id} = {self.energy.value}")
				

		
if __name__=="__main__":
	energy = [random.randint(-10, 20) for _ in range(4)]
	product=10
	consume = [random.randint(5, 15) for _ in range(4)]
	mode= [random.randint(1,3) for _ in range(4)]
	
	#shared memory for each home
	for i in range(4):
		print(f"home {i+1} init={energy[i]}")
		re=product-consume[i]
		print(f"home {i+1} rate={re}")
		print(f"home {i+1} mode={mode[i]}\n")
	
	Energy0=Value('d', energy[0])
	Energy1=Value('d', energy[1])
	Energy2=Value('d', energy[2])
	Energy3=Value('d', energy[3])
	
	weather_process = WeatherProcess()
	weather_process.start()	
		
	#try certain rounds of process
	for i in range(15):	
		print(f"\n\n\n round {i}")
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

		home1_process = homeProcess(1,Energy0,mode)
		home2_process = homeProcess(2,Energy1,mode)
		home3_process = homeProcess(3,Energy2,mode)
		home4_process = homeProcess(4,Energy3,mode)
		home1_process.start()
		home2_process.start()
		home3_process.start()
		home4_process.start()
		home1_process.join()
		home2_process.join()
		home3_process.join()
		home4_process.join()
		
		#read weather temperature	
		weather_process.lock1.acquire()
		temperature=weather_process.shared_memory.value
		print("temperature : ", temperature)
		weather_process.lock1.release()
		
		#change to next month
		weather_process.lock2.acquire()
		weather_process.current_month.value += 1
		print("next month : ", weather_process.current_month.value)
		weather_process.lock2.release()	
		
		#modify weather influence index from temperature get 
		rapport=temperature-20  # average temperature=17
		influence=rapport/10
		
		#after producing and consuming energy per month
		Energy0.value+=round(product-consume[0]*(1-influence),2)
		Energy1.value+=round(product-consume[1]*(1-influence),2)
		Energy2.value+=round(product-consume[2]*(1-influence),2)
		Energy3.value+=round(product-consume[3]*(1-influence),2)
		time.sleep(0.5)
		
		#remove all queue created
		for i in [1,2,3,4]:
			try:
				queue= sysv_ipc.MessageQueue(i)
				queue.remove()
				print(f"message queue {i} removed")
			except sysv_ipc.ExistentialError:
				print("connection n'exist ", i)
	#terminate weather
	weather_process.lock2.acquire()
	weather_process.current_month.value =0
	print("terminate weather ")
	weather_process.lock2.release()	

