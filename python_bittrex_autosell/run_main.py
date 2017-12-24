from .autosell import run
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--coins', help='Specify three coins, separated by commas with no space in between. '
                                              'First coin -> trade for Second -> trade for Third', type=str, metavar='')
    parser.add_argument('-p', '--price', metavar='',
                        help='Specify price difference in percentage relative '
                             'to top order in the order book. '
                             'I.e if the top SELL order is 100EUR and -p '
                             'is 0.02, you will place an order for 102EUR. '
                             'For BUY orders, you will place an order for 98EUR. '
                             'Leave empty, if you want to take the top order (default: 0)',
                        default=0, type=float)
    parser.add_argument('-t', '--time', help='Sleep interval in seconds between re-running the script (default: 3600)',
                        default=3600, metavar='',
                        type=float)
    parser.add_argument('-f', '--fee',
                        help='Bittrex trade fee, don\'t touch unless Bittrex '
                             'has changed it and it is not reflected in the script (default: 0.0025)',
                        default=0.0025, type=float, metavar='')
    parser.add_argument('-l', '--log', action='store_true')
    args = parser.parse_args()

    if args.coins is not None:
        coins = str.split(args.coins, ',')
        if len(coins) != 3:
            print('Incorrect number of coins. You must specify 3 comma separated coins.')
            exit(0)
        else:
            for i in range(len(coins)):
                coins[i] = str.upper(coins[i])
    else:
        print('You did not specify the coins correctly. Check the readme.')
        exit(0)

    run(args.coins, args.price, args.time, args.fee, args.log)
