import requests
import pandas as pd
import pandas_ta as ta
import numpy as np
import pandas_datareader as web
from binance import Client
from time import sleep
import datetime as dt
pd.options.mode.chained_assignment = None

### ESTRATEGIA
def strategy(df):
    if df["ema200"].iloc[-1] < df["ema50"].iloc[-1] and df["ema50"].iloc[-2] < df["ema200"].iloc[-2]:
        return "Buy"
    if df["ema200"].iloc[-1] > df["ema50"].iloc[-1] and df["ema50"].iloc[-2] > df["ema200"].iloc[-2]:
        return "Sell"

###    
info = client.futures_exchange_info() 
def get_precision(symbol):
   for x in info['symbols']:
    if x['symbol'] == symbol:
        return x['quantityPrecision']

    
api_key = ''
secret_key = ''
symbol = "BTCUSDT"

client = Client(api_key, secret_key)
  
def getdata():

  df = pd.DataFrame(client.futures_historical_klines(symbol = symbol, interval = "15m", limit = 1000, start_str = "5 days ago UTC"))
  df.columns = ["date","open","high","low","close","volume","close time","quote asset volume","number of trades","taker buy base asset volume","Taker buy quote asset volume","ignore"]
  df = df.astype("float")
  df['date'] =  pd.to_datetime(df['date'],dayfirst=True, unit = 'ms')
  df.set_index('date',inplace=True)
  df['close time'] =  pd.to_datetime(df['close time'],dayfirst=True, unit = 'ms')
  del df['ignore']

  ### Indicadores
  
  ema200 = df.ta.ema(200)
  ema50 = df.ta.ema(50)

  df["ema200"] = ema200
  df["ema50"] = ema50

  ###
  
  return df

df = getdata()
print(df.index[-1])

# FIXA
quantity = str(0.01) 

tpsl = False
tp = 5
sl = 3

strategycalls = True

flag_buy = False
flag_sell = False

while True:

  try:
    df = getdata()
  except:
    continue

  try:
    acc = pd.DataFrame(client.futures_get_all_orders()).tail(2)
  except:
    continue

  if tpsl == True:  
    if (acc["origType"].iloc[-1] == "TAKE_PROFIT_MARKET" or acc["origType"].iloc[-2] == "TAKE_PROFIT_MARKET" or acc["origType"].iloc[-1] == "STOP_MARKET" or acc["origType"].iloc[-2] == "STOP_MARKET") and (acc["status"].iloc[-1] == "FILLED" or acc["status"].iloc[-2] == "FILLED") and (flag_buy == True or flag_sell == True):
        print(client.futures_cancel_all_open_orders(symbol=symbol))
        if acc["side"].iloc[-1] == "SELL" and acc["status"].iloc[-1] == "FILLED":
            print(f'Long encerrado: {df.index[-1]}')
            flag_buy = False
        elif acc["side"].iloc[-2] == "SELL" and acc["status"].iloc[-2] == "FILLED":
            print(f'Long encerrado: {df.index[-1]}')
            flag_buy = False
        elif acc["side"].iloc[-1] == "BUY" and acc["status"].iloc[-1] == "FILLED":
            print(f'Short encerrado: {df.index[-1]}')
            flag_sell = False
        elif acc["side"].iloc[-2] == "BUY" and acc["status"].iloc[-2] == "FILLED":
            print(f'Short encerrado: {df.index[-1]}')
            flag_sell = False
            
  if strategycalls == True:
      if strategy(df) == "Buy" and flag_sell == True:
        print(client.futures_create_order(symbol=symbol, side='SELL', type='MARKET',quantity=quantity))
 
      if strategy(df) == "Sell" and flag_buy == True:
        print(client.futures_create_order(symbol=symbol, side='BUY', type='MARKET',quantity=quantity))

  if strategy(df) == "Sell" and (dt.datetime.now() <= df["close time"].iloc[-1] - dt.timedelta(seconds = 10)) == False and (flag_sell == False and flag_buy == False):
    print(client.futures_create_order(symbol=symbol, side='SELL', type='MARKET',quantity=quantity))
    
    if tpsl == True:
        print(client.futures_create_order(symbol=symbol, side='BUY', type='STOP_MARKET',stopPrice = round(df["close"].iloc[-1] * (1 + (sl/100)), get_precision(symbol)), closePosition = True))
        print(client.futures_create_order(symbol=symbol, side='BUY', type='TAKE_PROFIT_MARKET',stopPrice = round(df["close"].iloc[-1] * (1 - (tp/100)), get_precision(symbol)), closePosition = True))

    print(f'Short: {df.index[-1]}')
    flag_sell = True

  if strategy(df) == "Buy" and (dt.datetime.now() <= df["close time"].iloc[-1] - dt.timedelta(seconds = 10)) == False and (flag_buy == False and flag_sell == False):
    print(client.futures_create_order(symbol=symbol, side='BUY', type='MARKET',quantity=quantity))
    
    if tpsl == True:
        print(client.futures_create_order(symbol=symbol, side='SELL', type='STOP_MARKET',stopPrice = round(df["close"].iloc[-1] * (1 - (tp/100)), get_precision(symbol)), closePosition = True))
        print(client.futures_create_order(symbol=symbol, side='SELL', type='TAKE_PROFIT_MARKET',stopPrice = round(df["close"].iloc[-1] * (1 + (sl/100)), get_precision(symbol)), closePosition = True))

    print(f'Long: {df.index[-1]}')
    flag_buy = True

  sleep(2)
