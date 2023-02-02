def signalHandler:
    if signalReceived==SIGUSR1:
        change several factors in market!
def signalChild:
    50% probability
        send SIGUSR1 to market! 
 



class WeatherProcess:
    send the temperature to main
    
class MarketProcess:
    use socket to connect with clients
    start a random event by signal
    calculate the price of this round 
    
class homeProcess:
    receive temperature from main
    trade energy with other homes
    send its energy to market

main:
    start all processes
    print all results
    
