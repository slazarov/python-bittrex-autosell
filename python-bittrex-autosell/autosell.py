#!/usr/bin/python
# -*- coding: utf-8 -*-

# auto_sell.py
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

# ==========
# Parameters
# ==========

# First coin -> trade for Second -> trade for Third
coins = ['ZEN', 'BTC', 'SALT']
# Price difference relative to top order in the order book.
# I.e if the top SELL order is 100EUR and undercut_price is 0.02, you will place an order for 102EUR
# For BUY orders, you will place an order for 98EUR
# Leave 0 if you want to take the top order
undercut_price = 0.02
# Sleep interval between restarting the script and replacing the orders
sleep_interval = 5400
# Bittrex default fee is 0.25%, it's used to calculate
# the quantity for buy orders, change only if Bittrex changes it's fee
fee = 0.0025

# =========
# Constants
# =========
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


if __name__ == '__main__':
    bittrex_client = create_client()
    # Reset log
    open(LOG, 'w').close()
    # Cancel previous orders
    while True:
        msgs = []
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
                msgs.append(msg)

        sleep(10)
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
            price = orderbook[0]['Rate'] * (1 + undercut_price)
            trade = bittrex_client.sell_limit(ticker, qty, price)
            msg = "Sell order for " + ticker + " for " + str(qty) + "@" + str(price)
            msgs.append(msg)
            print(msg)

        if coin_2['Currency'] == 'USDT':
            if coin_1['Balance'] > 0 and coin_1['Pending'] == 0:
                ticker = coins[2] + '-' + coins[1]
                qty = coin_1['Balance']
                orderbook = bittrex_client.get_orderbook(ticker, bittrex.SELL_ORDERBOOK)['result']
                price = orderbook[0]['Rate'] * (1 + undercut_price)
                trade = bittrex_client.sell_limit(ticker, qty, price)
                msg = "Sell order for " + ticker + " for " + str(qty) + "@" + str(price)
                msgs.append(msg)
                print(msg)
        else:
            if coin_1['Balance'] > 0 and coin_1['Pending'] == 0:
                ticker = coins[1] + '-' + coins[2]
                orderbook = bittrex_client.get_orderbook(ticker, bittrex.BUY_ORDERBOOK)['result']
                price = orderbook[0]['Rate'] * (1 - undercut_price)
                qty = round((coin_1['Balance'] / price) * (1 - fee), 8)
                trade = bittrex_client.buy_limit(ticker, qty, price)
                msg = "Buy order for " + ticker + " for " + str(qty) + "@" + str(price)
                msgs.append(msg)
                print(msg)

        with open(LOG, 'a') as log:
            for msg in msgs:
                log.write('{} \n'.format(msg))

        msg = "Sleep for " + str(sleep_interval / 3600) + " hours..."
        with open('autosell.log', 'a') as log:
            log.write(msg + " \n")
        print(msg)
        sleep(sleep_interval)
