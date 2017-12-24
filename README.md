### Description:
Auto sell script for bittrex. It is used in the cases when you want
to auto sell a specific coin for another, but there is no direct market,
so you have to use an intermediate market.

For example, you are currently mining ZEN but want to convert it to GNT.
Since there is no direct market for ZEN/GNT, you have to purchase BTC with ZEN and then purchase GNT with BTC.

i.e ZEN >> BTC >> GNT

The script does the following procedure (with example):

1.) Cancels all existing orders.

2.) Tries to place orders for ZEN >> BTC or BTC >> GNT.

3.) Sleeps for sleep_interval = x.

4.) Repeat.

### How to use it:
1.) Put a credentials.json file in the directory with the following structure:

`{"api_key": "your_api_key", "api_secret": "your_api_secret"}`

Make sure you have given the correct permission to your api!

2.) Study the parameters
```python
$ python autosell.py -h
  -h, --help     show this help message and exit
  -c , --coins   Specify three coins, separated by commas. First coin -> trade
                 for Second -> trade for Third
  -p , --price   Specify price difference in percentage relative to top order
                 in the order book. I.e if the top SELL order is 100EUR and -p
                 is 0.02, you will place an order for 102EUR. For BUY orders,
                 you will place an order for 98EUR. Leave empty, if you want
                 to take the top order (default: 0)
  -t , --time    Sleep interval in seconds between re-running the script
                 (default: 3600)
  -f , --fee     Bittrex trade fee, don't touch unless Bittrex has changed it
                 and it is not reflected in the script (default: 0.0025)
  -l, --log
 ```

 ### Example usage:
 ```bash
 $ python autosell.py -coins  ZEN, BTC, SALT -price 0.02 -time 5400 -log
 ```
