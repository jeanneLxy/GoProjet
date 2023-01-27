import sysv_ipc
import multiprocessing
import time

#type=1 : "I need energy"
#type=2 : energy sent

def home_process(home_id, energy):
	key=home_id
	print(f"home {home_id} start...")

	try:
		queue= sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
	except sysv_ipc.ExistentialError:
		print("connection exist ", key)
		queue= sysv_ipc.MessageQueue(key)
#while True:
	if energy > 10:
		# check other homes if they need energy
		for i in [1,2,3,4]:
			if i!=key:
				try:
					queue2= sysv_ipc.MessageQueue(i)
					print(f"home {home_id} connection success home {i}")
				except sysv_ipc.ExistentialError:
					print(f"home {home_id} connection n'exist pas ", i)
					continue
				# Receive response from other home
				response,t = queue2.receive(type=1)
				message=response.decode()
				# Send energy to the home that needs it
				energy_needed = int(message.split(" ")[-1])
				print(f"home {home_id} receive home {i} energy needed = {energy_needed}" )
				energy_extra=energy-10
				if energy-10>= energy_needed:
					message=str(energy_needed).encode()
					queue2.send(message,type=2)
					energy-=energy_needed
					print (f"home {home_id} send {energy_needed} units of energy to home {i}")
					print (f"home {home_id} remain {energy} units of energy")
					time.sleep(1)
				else:
					message=str(energy_extra).encode()
					queue2.send(message,type=2)
					energy=10
					print (f"home {home_id} send {energy_extra} units of energy to home {i}")
					print (f"home {home_id} remain {energy} units of energy")
					time.sleep(1)
  else:

		# Ask other homes for energy
		message="I need energy "+ str(10-energy)
		queue.send(message.encode(),type=1)
		print(f"home {home_id} message sent into the queue: energy_needed={10-energy}")
		# Receive energy from other home
		answer,t= queue.receive(type=2)
		value=answer.decode()
		energy+=int(value)
		print(f"home {home_id} received {value} units of energy")
		print (f"home {home_id} remain {energy} units of energy")
		time.sleep(1)
	print(f"home {home_id} process end")
	queue.remove()
	

if __name__ == "__main__":
	#
	home1_process = multiprocessing.Process(target=home_process, args=(1, 8))
	home2_process = multiprocessing.Process(target=home_process, args=(2, 19))
	home3_process = multiprocessing.Process(target=home_process, args=(3, 6))
	home4_process = multiprocessing.Process(target=home_process, args=(4, 12))
	home1_process.start()
	home2_process.start()
	home3_process.start()
	home4_process.start()
	home1_process.join()
	home2_process.join()
	home3_process.join()
	home4_process.join()
