import pandas as pd
import yahoo_fin.stock_info as si
import time
import datetime


class PaperTrade:


#===============================
#   INIT
#===============================


    # Constructor
    # Initiates balance with $100,000 default cash
    # Initiates empty holdings dictionary
    # Initiates value to track share value as prices update
    def __init__(self, initial_balance=100000) -> None:
        """Constructs a paper trading instance"""

        # Instance trade data
        self.init_balance = initial_balance
        self.balance = initial_balance
        self.holdings_value = 0
        self.pnl = 0
        self.holdings = {}
        self.order_count = 0

        # Instance time data
        self.start_time = time.time()

        # Log file
        self.log_file = f"log-{int(self.start_time)}.txt"
        f = open(self.log_file, 'x')
        f.close()

        # Animation log file
        self.anim_log = f"anim-{int(self.start_time)}.txt"
        f = open(self.anim_log, 'w')
        f.write(f"0,{self.init_balance}")
        f.close()


#===============================
#   ORDER HANDLING
#===============================


    # Purchase given ticker and update
    def buy(self, ticker: str, user: str, time: str) -> None:
        """Purchase a single share of the given stock ticker."""
        
        # retrieving live price
        try:
            price = si.get_live_price(ticker)
        except AssertionError:
            self.notFound(ticker, time)
            return

        # checking that there is enough cash to purchase
        if self.balance > price:

            # checking if reference already exists in holdings
            # if no reference exists, create a new element with init values
            if ticker not in self.holdings.keys():
                self.holdings[ticker] = {'shares': 1, 'cost': price}
            # if reference already exists, update
            else:
                self.holdings[ticker]['shares'] += 1
                self.holdings[ticker]['cost'] += price

            # taking cost of share from cash stack
            self.balance -= price
            self.order_count += 1

            # print to log
            console = f"""[{time}] -- {user} successfully purchased share of ${ticker.upper()} for ${price}"""
            self.toLog(console)


        # produce balance error
        else:
            self.balanceError(ticker, time)


    # Sell given ticker and update
    def sell(self, ticker: str, user: str, time: str) -> None:
        """Sell a single share of the given stock ticker."""

        # checking that ticker exists in holdings
        if ticker in self.holdings.keys():

            # checking that atleast 1 share currently owned
            # this check needs to be separate in order to prevent key error
            if self.holdings[ticker]['shares'] > 1:

                # getting current price
                price = si.get_live_price(ticker)

                # getting shares held count
                shares = self.holdings[ticker]['shares']
                # getting cost of held shares
                cost = self.holdings[ticker]['cost']
                # estimating average cost
                avg_cost = cost / shares
                
                # removing 1 share from holdings and the average cost of that share
                self.holdings[ticker]['shares'] -= 1
                self.holdings[ticker]['cost'] -= avg_cost

                # if no shares remaining, remove from portfolio
                if self.holdings[ticker]['shares'] == 0:
                    self.holdings.pop(ticker)

                # adding profit/loss to cash stack
                self.balance += price
                self.order_count += 1

                # print to log
                console = f"""[{time}] -- {user} successfully sold share of ${ticker.upper()} for ${price}"""
                self.toLog(console)
            
            # produce share count error
            else:
                self.shareCountError(ticker, time)
        
        # produce holdings error
        else:
            self.holdingsError(ticker, time)


#===============================
#   STATUS AND ACCESSORS
#===============================


    # update the value of current holdings in this instance
    def getValue(self) -> None:
        """Determine the value of current holdings"""

        # value to return
        newValue = 0

        # identifying current value of holdings by ticker
        for ticker in self.holdings.keys():
            shares = self.holdings[ticker]['shares']
            price = si.get_live_price(ticker)
            newValue += shares * price
        
        # assigning to value
        self.holdings_value = newValue


    # update the pnl tracker if this instance
    def getpnl(self) -> None:
        """Determine the Profit and Loss"""

        # determine and assign PnL
        self.pnl = (self.holdings_value + self.balance)- self.init_balance


    # output pnl to log
    def getUpdate(self, time: str) -> None:
        """Output the PnL to log/terminal"""

        self.getValue()
        self.getpnl()
        console = f"""[{time}] -- Current Profit/Loss: ${self.pnl}"""

        self.toLog(console)


    def getHoldings(self, holdings: dict) -> None:
        """Logs dataframe of holdings at time of request"""

        # Cloning current holdings to append with current
        stats = pd.DataFrame(holdings)

        df = pd.DataFrame(self.holdings)
        print(df)


    # Logs the uptime in date format
    def getUptime(self, msg_time) -> None:
        """Logs and returns uptime of trade instance from initialization"""

        uptime_sec = time.time() - self.start_time
        conversion = datetime.timedelta(seconds=uptime_sec)
        uptime = str(conversion)
        console = f"""[{msg_time}] -- Current uptime: {uptime}"""

        self.toLog(console)

    # Returns the uptime in seconds
    def getRuntime(self) -> float:
        uptime_sec = int(time.time() - self.start_time)
        return uptime_sec


    def toLog(self, item: str) -> None:
        """Prints and Logs argument"""

        print(item)
        file = open(self.log_file, 'a')
        file.write(item + " \n")
        file.close()


#===============================
#   CHARTING
#===============================


    def chartLog(self, req_time: float) -> None:
        """Writes updated asset values to log file for animated plot"""

        # evaluating total value of combined cash and holdings
        tot_assets = str(round(self.balance + self.getLiveValue(), 2))

        # writing
        file = open(self.anim_log, 'a')
        file.write(f"{req_time},{tot_assets}")
        file.close()



    def getLiveValue(self, holdings: dict) -> float:
        """Returns live value of combined holdings"""

        # for each company in holdings, get value and add to total
        total = 0
        for company in holdings.keys():
            price = si.get_live_price(company)
            count = holdings[company['shares']]
            total += count * price

        return total
    
#===============================
#   ERRORS
#===============================

    
    def balanceError(self, ticker: str, time: str) -> None:
        """Prints and Logs error if balance is not large enough to place order"""

        console = f"[{time}] -- ### There is not a large enough balance to purchase ${ticker} ###"
        self.toLog(console)

    
    def shareCountError(self, ticker: str, time: str) -> None:
        """Prints and Logs error if there are no shares to sell"""

        console = f"[{time}] -- ### There are no remaining shares of ${ticker} to sell ###"
        self.toLog(console)

    
    def holdingsError(self, ticker: str, time: str) -> None:
        """Prints and Logs error if portfolio does not contains symbol"""

        console = f"[{time}] -- ### There are no holdings of ${ticker} currently in the portfolio ###"
        self.toLog(console)


    def commandError(self, time: str) -> None:
        """Prints and Logs if a command was received but is unable to be completed"""

        console = f"[{time}] -- ### Incorrect command syntax, try: !buy ['ticker-symbol'] or !sell ['ticker-symbol'] ###"
        self.toLog(console)


    def notFound(self, ticker: str, time: str) -> None:
        """Prints and Logs error if order is placed for symbol that does not exist"""

        console = f"[{time}] -- ### No pricing data found for ticker ${ticker} ###"
        self.toLog(console)