import time
import pyupbit
import datetime

access = "lJgmfUdvkRffmPvzGDZLxibbDiSbAui6nLftZmUS"
secret = "YRsinVz3K5ta0JmnoR6nrshO2UcxlxRm4QNUA2ZX"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_ma(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=30)
    ma = df['close'].rolling(k).mean().iloc[-1]
    return ma


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

hold = False

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-OMG", 0.5)
            current_price = get_current_price("KRW-OMG")
            ma_price = get_ma("KRW-OMG",10)
            #volume = get_balance("BTC")
            profit2 = False
            profit3 = False
            profit4 = False
            if target_price < current_price and ma_price < current_price and hold is False:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-OMG", 100000)
                    hold = True

            if hold is True and profit2 is False and profit3 is False and profit4 is False:
                Vol = get_balance("OMG")
                if (target_price * 1.2) < current_price:
                    upbit.sell_market_order("KRW-OMG", Vol*0.2)
                    profit2 is True
            if hold is True and profit2 is True and profit3 is False and profit4 is False:
                if (target_price * 1.3) < current_price:
                    upbit.sell_market_order("KRW-OMG", Vol*0.2)
                    profit3 is True
            if hold is True and profit2 is True and profit3 is True and profit4 is False:
                if (target_price * 1.4) < current_price:
                    upbit.sell_market_order("KRW-OMG", Vol*0.2)
                    profit4 is True


        else:
            Vol1 = get_balance("BTC")
            if Vol1 > 0.00008:
                upbit.sell_market_order("KRW-BTC", Vol1*0.9995)
        time.sleep(1)
        print(current_price, target_price, ma_price)
    except Exception as e:
        print(e)
        time.sleep(1)
