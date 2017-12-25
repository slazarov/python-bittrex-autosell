#!/usr/bin/python
# -*- coding: utf-8 -*-

# _constants.py

# =============
# Help messages
# =============

MSG_COINS = 'Specify three coins, separated by commas with no space ' \
            'in between. First coin -> trade for Second -> trade for Third'

MSG_PRICE = 'Specify price difference in percentage relative to top ' \
            'order in the order book. I.e if the top SELL order is ' \
            '100EUR and -p is 0.02, you will place an order for 102EUR. ' \
            'For BUY orders, you will place an order for 98EUR. Leave ' \
            'empty, if you want to take the top order (default: 0)'

MSG_TIME = 'Sleep interval in seconds between re-running the script (default: 3600)'

MSG_FEE = 'Bittrex trade fee, don\'t touch unless Bittrex has changed it ' \
          'and it is not reflected in the script (default: 0.0025)'

MSG_LOG = '[Optional] Append logs to the file named by \'path\'. If ' \
          '\'path\' is not given, append to \'autosell.log\' in current working folder.'

MSG_API = '[Optional] filepath to credentials file, e.g /Users/username/Documents/credentials.json ' \
          '(default: looks for credentials.json within the same folder where the script is executed'

# ==============
# Error messages
# ==============

CREDENTIALS_FILE_NOT_FOUND = 'Credentials file missing or incorrect filepath. Check $pba -h for help. Quitting...'
ERROR_COIN_NUMBER = 'Incorrect number of coins. You must specify 3 comma separated coins. E.g --coins ZEN,BTC,SALT'
ERROR_COIN_FORMAT = 'You did not specify the coins correctly. E.g --coins ZEN,BTC,SALT'

# =============
# Info messages
# =============

INFO_GETTING_BALANCES= 'Getting and sorting balances.'
INFO_GETTING_ORDERS = 'Getting open orders.'
INFO_CANCELLING_ORDERS = 'Canceling order for {} for {}@{} with ID: {}.'
INFO_ORDER_CANCEL_STATUS = 'Order {} cancellation success status: {}.'
INFO_ORDERS_NONE='No open orders found.'
INFO_PLACED_SELL_ORDER = 'Sell order for {} for {}@{}.'
INFO_PLACED_BUY_ORDER = 'Buy order for {} for {}@{}.'
INFO_PLACED_ORDER_STATUS = 'Order {} placement success status: {}.'
INFO_SLEEP = 'Sleep for {} hours.'
