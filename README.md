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

2.) Edit the parameters below.