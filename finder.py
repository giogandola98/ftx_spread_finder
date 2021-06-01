
import ftx
import time

API_KEY="" # pushbullet api key
TICKERS=['BTC','ETH']
OLD_SPREADS=[]
LIMIT=10	#minium spread percent
FUTURE_ELLAPSE='1231' #ftx future to track

def init():
	for ticker in TICKERS:
		OLD_SPREADS.append(0)
		

def find_spread(ticker,ellapse_date):
	client=ftx.FtxClient()
	#get future price
	result = client.get_orderbook(ticker+'-'+ellapse_date,1)
	future_price=result['bids'][0][0]
	#get real price
	result = client.get_orderbook(ticker+'/USD',1)
	real_price=result['bids'][0][0]
	#print("TICKER:",ticker,"FUTURE:",future_price,"REAL:",real_price,"DIFF:",future_price-real_price,"PERCENT:",((future_price-real_price)/real_price)*100)
	return [future_price,real_price,future_price-real_price,((future_price-real_price)/real_price)*100]

def send_notify(ticker,spread):
	print("SENDING:",ticker,spread)
	from pushbullet import Pushbullet
	pb= Pushbullet(API_KEY)
	title=ticker+"/USD spread"
	text="spread is now: "+str(spread)+'%'
	push = pb.push_note(title,text)
	
def check():
	for i in range(0,len(TICKERS)):
		x=find_spread(TICKERS[i],FUTURE_ELLAPSE)
		if((x[3]>LIMIT) and (x[3]>OLD_SPREADS[i]+0.5)):	
			OLD_SPREADS[i]=x[3]
			send_notify(TICKERS[i],x[3])
		

def run_forever():
	while True:
		check()
		time.sleep(60)

init()
run_forever()
