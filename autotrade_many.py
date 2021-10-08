import time
import pyupbit
import datetime

access = "lJgmfUdvkRffmPvzGDZLxibbDiSbAui6nLftZmUS"
secret = "YRsinVz3K5ta0JmnoR6nrshO2UcxlxRm4QNUA2ZX"

def get_target_price(ticker, k):
    """get target price by Break through volatility"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_ma(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=30)
    ma = df['close'].rolling(k).mean().iloc[-1]
    return ma


def get_start_time(ticker):
    """get start time"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """cheak money"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """check current price"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# LOGIN
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

hold = False
profit2 = False
profit3 = False
profit4 = False
coin_list = ['KRW-XTZ', 'KRW-QTUM','KRW-MTL','KRW-ADA','KRW-SRM','KRW-EOS','KRW-XLM','KRW-CHZ','KRW-ETC']



# Start autotrade
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        for C in coin_list:
            end_time = start_time + datetime.timedelta(days=1)
            if start_time < now < end_time - datetime.timedelta(seconds=10):
                target_price = get_target_price(C, 0.5)
                current_price = get_current_price(C)
                ma_price = get_ma(C,10)
                #volume = get_balance("BTC")
                Vol = upbit.get_balance(C)
                
                if target_price < current_price and ma_price < current_price and hold is False:
                    krw = get_balance("KRW")
                    if krw > 5000:
                        upbit.buy_market_order(C, 200000)
                        hold = True

                if hold is True and profit2 is False and profit3 is False and profit4 is False:
                    Vol = upbit.get_balance(C)
                    if (target_price * 1.2) < current_price:
                        upbit.sell_market_order(C, Vol*0.2)
                        profit2 is True
                if hold is True and profit2 is True and profit3 is False and profit4 is False:
                    if (target_price * 1.3) < current_price:
                        upbit.sell_market_order(C, Vol*0.2)
                        profit3 is True
                if hold is True and profit2 is True and profit3 is True and profit4 is False:
                    if (target_price * 1.4) < current_price:
                        upbit.sell_market_order(C, Vol*0.2)
                        profit4 is True


            else:
                Vol1 = upbit.get_balance(C)
                if Vol1 > 0.00008:
                    upbit.sell_market_order(C, Vol1*0.97)
                    hold = False
                    profit2 = True
                    profit3 = True
                    profit4 = True
            time.sleep(1)
            print("Coin",C,"Current",current_price, "Target",target_price,"MA", ma_price,"HOLD", hold,"PROFITs", profit2,profit3,profit4,Vol)
    except Exception as e:
        print(e)
        time.sleep(1)
