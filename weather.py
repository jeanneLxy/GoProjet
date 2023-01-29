import time
from multiprocessing import Process, Value, Lock

class WeatherProcess(Process):

    def __init__(self):
        super().__init__()
        self.shared_memory = Value("d", 0.1)
        self.lock = Lock()
        self.current_month=1

    def run(self):
        while True:
            #current_month = time.gmtime().tm_mon
            if self.current_month in range(1, 3):
                self.lock.acquire()
                self.shared_memory.value = 0.1
                self.lock.release()
            elif self.current_month in range(4, 6):
                self.lock.acquire()
                self.shared_memory.value = 0.55
                self.lock.release()
            elif self.current_month in range(7, 9):
                self.lock.acquire()
                self.shared_memory.value = 0.15
                self.lock.release()
            elif self.current_month in range(9, 12):
                self.lock.acquire()
                self.shared_memory.value = 0.65
                self.lock.release()
            self.current_month+=1
            if self.current_month>12:
            	self.current_month=1
            time.sleep(1)

if __name__ == '__main__':
    weather_process = WeatherProcess()
    weather_process.start()
    while True:
        weather_process.lock.acquire()
        print("Shared memory value:", weather_process.shared_memory.value)
        weather_process.lock.release()
        time.sleep(1)
