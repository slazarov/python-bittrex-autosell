#!/usr/bin/python
# -*- coding: utf-8 -*-

# main.py
from __future__ import print_function
import bittrex
import argparse
from json import load
from time import sleep
from sys import exit
from ._constants import *
import logging
from ._logger import add_stream_logger

logger = logging.getLogger(__name__)

"""
Readme:
https://github.com/slazarov/python-bittrex-autosell
"""


def open_credentials(credentials_file):
    try:
        with open(credentials_file, 'r') as file:
            credentials = load(file)
        return credentials
    except FileNotFoundError:
        print(CREDENTIALS_FILE_NOT_FOUND)
        exit(0)


def create_client(api_keys):
    credentials = open_credentials(api_keys)
    c = bittrex.Bittrex(api_key=credentials['api_key'],
                        api_secret=credentials['api_secret'],
                        api_version=bittrex.API_V1_1)
    return c


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--coins', help=MSG_COINS, type=str, metavar='')
    parser.add_argument('-p', '--price', help=MSG_PRICE, default=0, type=float, metavar='')
    parser.add_argument('-t', '--time', help=MSG_TIME, default=3600, type=float, metavar='')
    parser.add_argument('-f', '--fee', help=MSG_FEE, default=0.0025, type=float, metavar='')
    parser.add_argument('-l', '--log', help=MSG_LOG, default=False, type=str, nargs='?', const='autosell.log',
                        metavar='')
    parser.add_argument('-a', '--api', help=MSG_API, default='credentials.json', type=str, metavar='')
    args = parser.parse_args()

    if args.coins is not None:
        coins = str.split(args.coins, ',')
        if len(coins) != 3:
            print(ERROR_COIN_NUMBER)
            exit(0)
        else:
            for i in range(len(coins)):
                coins[i] = str.upper(coins[i])
    else:
        print(ERROR_COIN_FORMAT)
        exit(0)

    bittrex_client = create_client(args.api)
    add_stream_logger()
    logger.info('hi')
    exit(0)

    # Cancel previous orders
    while True:
        msg = INFO_GETTING_ORDERS
        if args.log is True:
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
                msg = INFO_CANCELLING_ORDERS.format(order['Exchange'], order['Quantity'], order['Limit'])
                print(msg)
                if args.log is True:
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
            price = orderbook[0]['Rate'] * (1 + args.price)
            trade = bittrex_client.sell_limit(ticker, qty, price)
            # msg = "Sell order for " + ticker + " for " + str(qty) + "@" + str(price)
            msg = INFO_PLACED_SELL_ORDER.format(ticker, qty, price)
            if args.log is True:
                msgs.append(msg)
            print(msg)

        if coin_2['Currency'] == 'USDT':
            if coin_1['Balance'] > 0 and coin_1['Pending'] == 0:
                ticker = coins[2] + '-' + coins[1]
                qty = coin_1['Balance']
                orderbook = bittrex_client.get_orderbook(ticker, bittrex.SELL_ORDERBOOK)['result']
                price = orderbook[0]['Rate'] * (1 + args.price)
                trade = bittrex_client.sell_limit(ticker, qty, price)
                # msg = "Sell order for " + ticker + " for " + str(qty) + "@" + str(price)
                msg = INFO_PLACED_SELL_ORDER.format(ticker, qty, price)
                if args.log is True:
                    msgs.append(msg)
                print(msg)
        else:
            if coin_1['Balance'] > 0 and coin_1['Pending'] == 0:
                ticker = coins[1] + '-' + coins[2]
                orderbook = bittrex_client.get_orderbook(ticker, bittrex.BUY_ORDERBOOK)['result']
                price = orderbook[0]['Rate'] * (1 - args.price)
                qty = round((coin_1['Balance'] / price) * (1 - args.fee), 8)
                trade = bittrex_client.buy_limit(ticker, qty, price)
                # msg = "Buy order for " + ticker + " for " + str(qty) + "@" + str(price)
                msg = INFO_PLACED_BUY_ORDER.format(ticker, qty, price)
                if args.log is True:
                    msgs.append(msg)
                print(msg)

        # msg = "Sleep for " + str(args.time / 3600) + " hours..."
        msg = INFO_SLEEP.format(args.time / 3600)
        if args.log is True:
            msgs.append(msg)
        if args.log is True:
            with open(args.log, 'a') as log:
                for msg in msgs:
                    log.write('{} \n'.format(msg))
        print(msg)
        sleep(args.time)


if __name__ == '__main__':
    main()
