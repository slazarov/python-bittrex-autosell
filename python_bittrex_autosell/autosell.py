#!/usr/bin/python
# -*- coding: utf-8 -*-

# autosell.py
from __future__ import print_function
import bittrex
from json import load
from time import sleep
"""
Description:
Auto sell script for bittrex. It is used in the cases when you want 
to auto sell a specific coin for another, but there is no direct market,
so you have to use an intermediate market.

For example, you are currently mining ZEN but want to convert it to GNT.
Since there is no direct market for ZEN/GNT, you have to purchase BTC with ZEN and then purchase GNT with BTC.
ZEN >> BTC >> GNT

The script does the following procedure (with example):
1.) Cancels all existing orders.
2.) Tries to place orders for ZEN >> BTC or BTC >> GNT.
3.) Sleeps for sleep_interval = x.
4.) Repeat.

How to use it:
1.) Put a credentials.json file in the directory with the following structure:
{"api_key": "your_api_key", "api_secret": "your_api_secret"}
Make sure you have given the correct permission to your api!
2.) Edit the parameters below.
"""

LOG = 'autosell.log'
CREDENTIALS = 'credentials.json'


def open_credentials():
    with open(CREDENTIALS, 'r') as file:
        credentials = load(file)
    return credentials


def create_client():
    credentials = open_credentials()
    c = bittrex.Bittrex(api_key=credentials['api_key'],
                        api_secret=credentials['api_secret'],
                        api_version=bittrex.API_V1_1)
    return c


def run(coins, price, time, fee,log):
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-c', '--coins', help='Specify three coins, separated by commas with no space in between. '
    #                                           'First coin -> trade for Second -> trade for Third', type=str, metavar='')
    # parser.add_argument('-p', '--price', metavar='',
    #                     help='Specify price difference in percentage relative '
    #                          'to top order in the order book. '
    #                          'I.e if the top SELL order is 100EUR and -p '
    #                          'is 0.02, you will place an order for 102EUR. '
    #                          'For BUY orders, you will place an order for 98EUR. '
    #                          'Leave empty, if you want to take the top order (default: 0)',
    #                     default=0, type=float)
    # parser.add_argument('-t', '--time', help='Sleep interval in seconds between re-running the script (default: 3600)',
    #                     default=3600, metavar='',
    #                     type=float)
    # parser.add_argument('-f', '--fee',
    #                     help='Bittrex trade fee, don\'t touch unless Bittrex '
    #                          'has changed it and it is not reflected in the script (default: 0.0025)',
    #                     default=0.0025, type=float, metavar='')
    # parser.add_argument('-l', '--log', action='store_true')
    # args = parser.parse_args()

    # if coins is not None:
    #     coins = str.split(coins, ',')
    #     if len(coins) != 3:
    #         print('Incorrect number of coins. You must specify 3 comma separated coins.')
    #         exit(0)
    #     else:
    #         for i in range(len(coins)):
    #             coins[i] = str.upper(coins[i])
    # else:
    #     print('You did not specify the coins correctly. Check the readme.')
    #     exit(0)

    bittrex_client = create_client()

    # Cancel previous orders
    while True:
        msg = 'Getting open orders.'
        if log is True:
            msgs = [msg]
        print(msg)
        open_orders = []
        for _ in range(5):
            open_orders = bittrex_client.get_open_orders()['result']
            if not open_orders or open_orders is None:
                sleep(1)
            else:
                break
        if open_orders is not None:
            for order in open_orders:
                cancel = bittrex_client.cancel(order['OrderUuid'])
                msg = 'Canceling order for {} for {}@{}.'.format(order['Exchange'], order['Quantity'], order['Limit'])
                print(msg)
                if log is True:
                    msgs.append(msg)

        sleep(5)
        balance = bittrex_client.get_balances()
        balances = {}

        while len(balances) < len(coins):
            for item in balance['result']:
                for coin in coins:
                    if item['Currency'] == coin:
                        balances[coin] = item
                        break

        coin_0 = balances[coins[0]]
        coin_1 = balances[coins[1]]
        coin_2 = balances[coins[2]]

        # Sell first coin for second coin
        if coin_0['Balance'] == coin_0['Available'] > 0 and coin_0['Pending'] == 0:
            ticker = coins[1] + '-' + coins[0]
            qty = coin_0['Balance']
            orderbook = bittrex_client.get_orderbook(ticker, bittrex.SELL_ORDERBOOK)['result']
            # Don't sell @ market price, set a price at 3% higher and hope it will move into your favour
            price = orderbook[0]['Rate'] * (1 + price)
            trade = bittrex_client.sell_limit(ticker, qty, price)
            msg = "Sell order for " + ticker + " for " + str(qty) + "@" + str(price)
            if log is True:
                msgs.append(msg)
            print(msg)

        if coin_2['Currency'] == 'USDT':
            if coin_1['Balance'] > 0 and coin_1['Pending'] == 0:
                ticker = coins[2] + '-' + coins[1]
                qty = coin_1['Balance']
                orderbook = bittrex_client.get_orderbook(ticker, bittrex.SELL_ORDERBOOK)['result']
                price = orderbook[0]['Rate'] * (1 + price)
                trade = bittrex_client.sell_limit(ticker, qty, price)
                msg = "Sell order for " + ticker + " for " + str(qty) + "@" + str(price)
                if log is True:
                    msgs.append(msg)
                print(msg)
        else:
            if coin_1['Balance'] > 0 and coin_1['Pending'] == 0:
                ticker = coins[1] + '-' + coins[2]
                orderbook = bittrex_client.get_orderbook(ticker, bittrex.BUY_ORDERBOOK)['result']
                price = orderbook[0]['Rate'] * (1 - price)
                qty = round((coin_1['Balance'] / price) * (1 - fee), 8)
                trade = bittrex_client.buy_limit(ticker, qty, price)
                msg = "Buy order for " + ticker + " for " + str(qty) + "@" + str(price)
                if log is True:
                    msgs.append(msg)
                print(msg)

        msg = "Sleep for " + str(time / 3600) + " hours..."
        if log is True:
            msgs.append(msg)
        if log is True:
            with open(LOG, 'a') as log:
                for msg in msgs:
                    log.write('{} \n'.format(msg))
        print(msg)
        sleep(time)

# if __name__ == '__main__':
#
