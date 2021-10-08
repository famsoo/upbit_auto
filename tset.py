import time
import pyupbit
import datetime

access = "lJgmfUdvkRffmPvzGDZLxibbDiSbAui6nLftZmUS"
secret = "YRsinVz3K5ta0JmnoR6nrshO2UcxlxRm4QNUA2ZX"

def get_target_price(ticker, k):
    """dolpa"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_ma(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=30)
    ma = df['close'].rolling(k).mean().iloc[-1]
    return ma


def get_start_time(ticker):
    """start time"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """monry"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """current"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# LOGIN
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

hold = False
profit2 = False
profit3 = False
profit4 = False
coin_list = ['KRW-XTZ', 'KRW-QTUM','KRW-MTL','KRW-ADA','KRW-SRM','KRW-EOS','KRW-XLM','KRW-CHZ','KRW-ETC']

target_price = get_target_price(C, 0.5)
current_price = get_current_price(C)
ma_price = get_ma(C,10)
print("Coin",C,"Current",current_price, "Target",target_price,"MA", ma_price,"HOLD", hold,"PROFITs", profit2,profit3,profit4,Vol)
