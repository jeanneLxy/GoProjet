from multiprocessing import Process
import threading
class HomeProcess(Process):

    def __init__(self, production_rate, consumption_rate, policy):
        super().__init__()
        self.production_rate = production_rate
        self.consumption_rate = consumption_rate
        self.message_queue = []
    
    def run (self):
        while True:
            # Receive messages from other home processes
            self.receive_messages()
            # Calculate energy balance
            self.calculate_energy_balance()
            # Trade energy according to policy
            self.trade_energy()
            # Update home display
            self.update_home_display()
            # Sleep for a time period
            time.sleep(1)

class MarketProcess(Process):

    	def __init__(self, current_price):
    		super().__init__()
        	self.current_price = current_price
        	self.sockets = []
        	self.transaction_limit = 10

	def run (self):
	        external=ExternalProcess()
	        external.start()
	        #external.join()
	        def myMarket():
	        	while True:
	            # Receive messages from home processes
				self.receive_messages()
	            # Calculate energy price
	            		self.calculate_energy_price()
	            # Update market display
	            		self.update_market_display()
	            # Sleep for a time period
	            		time.sleep(1)
	        market1=threading.Thread(target=myMarket,args())
	        market2=threading.Thread(target=myMarket,args())
	        market3=threading.Thread(target=myMarket,args())
	        market1.start()
	        market2.start()
	        market3.start()
	        market1.join()
	        market2.join()
	        market3.join()
	        external.join()
	        
	        
	#def marketCalculate()	
            
            
            
class ExternalProcess(Process):

    def run(self):
        while True:
            # Generate random events
            self.generate_random_events()
            # Signal parent process
            self.signal_parent_process()
            # Sleep for a time period
            time.sleep(1)                 

class WeatherProcess(Process):

	def __init__(self):
        	super().__init__()
        	self.shared_memory = {}
	def run(self):
		#à ajouter

if __name__=="__main__":
	home1=HomeProcess(productionRate1,consumptionRate1,policy)
	home2=HomeProcess(productionRate2,consumptionRate2,policy)
	home3=HomeProcess(productionRate3,consumptionRate3,policy)
	
	market=MarketProcess(currentPrice)
	
	weather=WeatherProcess()
	
	
	home1.start()
	home2.start()
	home3.start()
	
	market.start()
	
	weather.start()
	
	
	home1.join()
	home2.join()
	home3.join()
	
	market.join()
	
	weather.join()
	
	
	
	
	


