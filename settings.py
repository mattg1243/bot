import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import sys
import talib
import websocket

api_key = "bBUxPdmHeJCigGHjkK9BI3aB5pYvaSVG01N2dtoHAL5kPaXCWdklP2qxV23ixLlJ"

COIN_FOR_SOCKET = 'dogeusdt'
INTERVAL_FOR_SOCKET = '1m'

RISK = 1

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

SOCKET = f'wss://stream.binance.us:9443/ws/{COIN_FOR_SOCKET}@kline_{INTERVAL_FOR_SOCKET}'
print(f'\nSOCKET : {SOCKET}')

global json_message
closes = []


def on_open(ws):
    sys.stdout = open('run-log.txt', 'a')
    print('   ---   websocket connected   ---   ')
    sys.stdout.close()


def on_close(ws):
    sys.stdout = open('run-log.txt', 'a')
    print('   ---   websocket disconnected   ---   ')
    sys.stdout.close()


def on_message(ws, message):
    sys.stdout = open('run-log.txt', 'a')
    global json_message
    print('message received')
    json_message = json.loads(message)
    candle = json_message['k']
    is_closed = candle['x']
    open_price = candle['o']
    close_price = candle['c']
    print(f'open : {open_price}\nclose: {close_price}\n')

    if is_closed:
        print(f'candle closed at {close_price}\n')
        closes.append(float(close_price))
        
        if len(closes) > RSI_PERIOD:
            np_closes = np.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            last_rsi = rsi[-1]
            print(f'   +++   all RSIs calculated so far : {rsi}   +++\n')
            print(f'   +++   last RSIs calculated : {last_rsi: .2f}   +++\n')

            if last_rsi > RSI_OVERBOUGHT:
                print(f'RSI is giving a buy signal. Current RSI level : {last_rsi}')
                buy_confirm = input('Would you like to buy? (y/n) : ')

                if buy_confirm == 'y':
                    buy(COIN_FOR_SOCKET)
                else:
                    print('Signal ignored')

            if last_rsi < RSI_OVERSOLD:
                print(f'RSI is giving a SELL signal. Current RSI level : {last_rsi}')
                sell_confirm = input('Would you like to sell? (y/n) : ')

                if sell_confirm == 'y':
                    sell(COIN_FOR_SOCKET)
                else:
                    print('Signal ignored')

    sys.stdout.close()


def on_error(ws, error):
    sys.stdout = open('run-log.txt', 'a')
    print(error)
    sys.stdout.close()git


def sell(symbol):
    pass


def buy(symbol):
    pass


ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error)


