# Stream Trader

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

`Stream Trader` is a Youtube based chat bot. It receives commands in the live chat of a stream and makes trades in a simulated 'paper' market. This bot is made possible using the [yahoo_fin](http://theautomatic.net/yahoo_fin-documentation/) and [pytchat](https://github.com/taizan-hokuto/pytchat) libraries.

### To Be Built
* Live updating chart and table that will provide users/chatters with easy to read data regarding the status of the bot
* Installation through pip and ~~instructions for install~~
* List of key features

### Installation
*pip coming soon*
Currently, you can fork this repo and install all dependencies through the pipfile.
```
pipenv install
```

### Launch
```
pipenv run python bot.py <starting-cash> <stream-id>
```

## Commands
None of the commands are case sensitive. There are a series of code blocks to catch errors and log specific details regarding what occurred.

* Purchase a share
```
!buy ['ticker-symbol']
```
```
[HH:MM:SS] -- <user> successfully purchased share of $AAPL for $155.47
```
--
* Sell a share
```
!sell ['ticker-symbol']
```
```
[HH:MM:SS] -- <user> successfully sold share of $AAPL for $127.86
```
--
* Update PnL
```
!update
```
```
[HH:MM:SS] -- Current Profit/Loss: $88977.24
```
--
* Bot Uptime
```
!uptime
```
```
[HH:MM:SS] -- Current uptime: HH:MM:SS
```

## Errors
* Balance
```
[HH:MM:SS] -- ### There is not a large enough balance to purchase ${ticker} ###
```

* Share Count
```
[HH:MM:SS] -- ### There are no remaining shares of ${ticker} to sell ###
```

* Holdings
```
[HH:MM:SS] -- ### There are no holdings of ${ticker} currently in the portfolio ###
```

* Command
```
[HH:MM:SS] -- ### Incorrect command syntax, try: !buy ['ticker-symbol'] or !sell ['ticker-symbol'] ###
```

* Symbol Not Found
```
[HH:MM:SS] -- ### No pricing data found for ticker ${ticker} ###
```
