# Stream Trader

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

'Stream Trader' is a Youtube based chat bot. It takes a simple commands in the live chat and makes live tracked paper trades instantly. This bot is made possible using the [yahoo_fin](http://theautomatic.net/yahoo_fin-documentation/) and [pytchat](https://github.com/taizan-hokuto/pytchat) libraries.

### To Be Built
* Live updating chart and table that will provide users/chatters with easy to read data regarding the status of the bot
* Installation through pip and instructions for install
* Live chat output alongside current terminal logging

### Installation
*coming soon*

## Commands
None of the commands are case sensitive. There are a series of code blocks to catch errors and log specific details regarding what occurred.

* Purchase a share
```
!buy ['ticker-symbol']
```
An update regarding the purchase order will be logged to terminal.
If the chatter fails to input a symbol or enters a non-existant symbol, an error with specific information will be printed to the terminal. 
If there is not a large enough cash balance to make the purchase a note will be printed to terminal.
```
Successfully purchased share of $AAPL for $155.47
```
--
* Sell a share
```
!sell ['ticker-symbol']
```
If the chatter order the sale of a stock which is not in the portfolio, an error is returned and logged.
```
Successfully sold share of $AAPL for $127.86
```
--
* Update PnL
```
!update
```
Upon receiving the order to update, a message containing the current profit/loss will be printed. This is based on current market value of the entire portfolio.
```
Current Profit/Loss: $88977.24
```
--
* Bot Uptime
```
!uptime
```
Returns the uptime of the bot from initialization in minutes.

## Errors
* Balance
```
### There is not a large enough balance to purchase ${ticker} ###
```

* Share Count
```
### There are no remaining shares of ${ticker} to sell ###
```

* Holdings
```
### There are no holdings of ${ticker} currently in the portfolio ###
```

* Command
```
### Incorrect command syntax, try: !buy ['ticker-symbol'] or !sell ['ticker-symbol'] ###
```

* Symbol Not Found
```
### No pricing data found for ticker ${ticker} ###
```
