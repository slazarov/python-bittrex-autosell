# python-bittrex-autosell
Python CLI tool to auto sell coins on Bittrex.

It is used in the cases when you want to auto sell a specific coin for
another, but there is no direct market, so you have to use an intermediate market.

# Why use it?:
The tool is mostly geared to miners who are mining a given coin but
want to hold another one.

For example, you are currently mining ZEN but want to convert it to GNT.
Since there is no direct market for ZEN/GNT on Bittrex, you have to purchase BTC with ZEN and then purchase GNT with BTC.

So what happens in reality is the following (example):

1.) You mine ZEN on some pool.

2.) The pool periodically sends the mined coins to the relevant wallet on Bittrex

while this is happening the script is doing the following:

3.) Cancels all existing orders.

4.) Tries to place orders for ZEN >> BTC and BTC >> GNT.

5.) Sleeps for x seconds.

6.) Repeat.


# Usage
```
usage: pba [-h] [-c] [-p] [-t] [-f] [-l ] [-a]

optional arguments:
  -h, --help       show this help message and exit
  -c , --coins     Specify three coins, separated by commas with no space in
                   between. First coin -> trade for Second -> trade for Third
  -p , --price     Specify price difference in percentage relative to top
                   order in the order book. I.e if the top SELL order is
                   100EUR and -p is 0.02, you will place an order for 102EUR.
                   For BUY orders, you will place an order for 98EUR. Leave
                   empty, if you want to take the top order (default: 0)
  -t , --time      Sleep interval in seconds between re-running the script
                   (default: 3600)
  -f , --fee       Bittrex trade fee, don't touch unless Bittrex has changed
                   it and it is not reflected in the script (default: 0.0025)
  -l [], --log []  Append logs to the file named by 'path'. If 'path' is not
                   given, append to 'autosell.log' in current working folder.
  -a , --api       Read api keys from json filed named by 'path'. If 'path' is
                   not given, read from 'credentials.json' in current working
                   folder.
 ```

You need to put a json file (e.g credentials.json) with your api keys in your current bash directory with the following structure.
```
{"api_key": "your_api_key", "api_secret": "your_api_secret"}
````

Make sure you have given the correct permission to your api!

**The script doesn't store your api keys anywhere, but be prudent and check the source code.**

I advise to use a docker image.

# Example usage:
Open your terminal/cmd and fire pba.
#### Scenario 1
* buy SALT with ZEN
  * Sell ZEN for BTC
  * Buy SALT with BTC
* trades are executed so that they match the top order from the respective order book
* re-run the script in 3600 seconds (1hr)
* no external file logging
* api keys are contained in 'credentials.json' which in the folder where the script is executed
 ```
$ pba --coins ZEN,BTC,SALT
```

#### Scenario 2
* place limit orders that are 2.5% higher/lower than the top order from the respective order book
 ```
$ pba --coins ZEN,BTC,SALT --price 0.025
```
#### Scenario 3
* change re-run time to 5400 seconds (1.5hrs)
 ```
$ pba --coins ZEN,BTC,SALT --price 0.025 --time 5400
```
#### Scenario 4
* add external file logging
 ```
$ pba --coins ZEN,BTC,SALT --price 0.025 --time 5400 --log /Users/slazarov/Documents/autosell.log
```
#### Scenario 5
* specify credentials file
 ```
$ pba --coins ZEN,BTC,SALT --price 0.025 --time 5400 --log ~/Documents/autosell.log --api ~/Documents/autosell.log
```


