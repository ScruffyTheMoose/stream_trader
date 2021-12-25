from os import times_result
import pandas as pd
import yahoo_fin.stock_info as si
import time
import datetime
import logging


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
        self.holdings = {}
        self.order_count = 0

        # Instance time data
        self.start_time = time.time()

        # Log file
        logging.basicConfig(filename=f"log-{int(self.start_time)}.log", encoding='utf-8', level=logging.INFO)

        # counts refresh iterations to allow for timing
        self.refresh_ctr = 0

        # 2d list which contains ordered pairs of portfolio data to be plotted
        # [minute, value]
        self.chart_data = [[0, int(self.balance)]]


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
            logging.info(console)


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
            if self.holdings[ticker]['shares'] >= 1:

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
                logging.info(console)
            
            # produce share count error
            else:
                self.shareCountError(ticker, time)
        
        # produce holdings error
        else:
            self.holdingsError(ticker, time)


#===============================
#   STATUS AND ACCESSORS
#===============================


    # output pnl to log
    def getUpdate(self, time: str) -> None:
        """Output the PnL to log/terminal"""

        holdings_value = self.getLiveValue(self.holdings)
        pnl = (holdings_value + self.balance) - self.init_balance
        console = f"""[{time}] -- Current Profit/Loss: ${pnl}"""

        print(console)
        logging.info(console)


    def getHoldings(self, holdings: dict) -> None:
        """Logs dataframe of holdings at time of request"""

        # Cloning current holdings to append with current
        stats = pd.DataFrame(holdings)

        # convert to dataframe
        df = pd.DataFrame(self.holdings)
        
        print(df)
        logging.info(df)


    # Logs the uptime in date format
    def getUptime(self, msg_time) -> None:
        """Logs and returns uptime of trade instance from initialization"""

        uptime_sec = time.time() - self.start_time
        conversion = datetime.timedelta(seconds=uptime_sec)
        uptime = str(conversion)
        console = f"""[{msg_time}] -- Current uptime: {uptime}"""

        print(console)
        logging.info(console)

    # Returns the uptime in seconds
    def runtime(self) -> int:
        """Evaluates and returns the runtime of the trade instance measured in seconds"""

        uptime_sec = int(time.time() - self.start_time)
        
        return uptime_sec


    def chartData(self) -> None:
        """Writes updated asset values to log file for animated plot"""

        # evaluating total value of combined cash and holdings
        tot_assets = round(self.balance + self.getLiveValue(self.holdings), 2)
        minute = int(self.runtime() / 60)

        # to 2d list
        if self.chart_data[-1][0] == minute:
            self.chart_data[-1][1] = tot_assets
        else:
            self.chart_data.append([minute, tot_assets])

        self.refresh_ctr += 1


    def getLiveValue(self, holdings: dict) -> float:
        """Returns live value of combined holdings"""

        # for each company in holdings, get value and add to total
        total = 0
        for company in holdings.keys():
            price = si.get_live_price(company)
            count = holdings[company]['shares']
            total += count * price

        return total


#===============================
#   LOGGING
#===============================


    def logInfo(self, text: str) -> None:
        """For logging info outside of module"""

        logging.info(text)


    def logError(self, text: str) -> None:
        """For logging errors outside of module"""

        logging.error(text)


#===============================
#   ERRORS
#===============================

    
    def balanceError(self, ticker: str, time: str) -> None:
        """Prints and Logs error if balance is not large enough to place order"""

        console = f"[{time}] -- There is not a large enough balance to purchase ${ticker}"
        logging.error(console)

    
    def shareCountError(self, ticker: str, time: str) -> None:
        """Prints and Logs error if there are no shares to sell"""

        console = f"[{time}] -- There are no remaining shares of ${ticker} to sell"
        logging.error(console)

    
    def holdingsError(self, ticker: str, time: str) -> None:
        """Prints and Logs error if portfolio does not contains symbol"""

        console = f"[{time}] -- There are no holdings of ${ticker} currently in the portfolio"
        logging.error(console)


    def commandError(self, time: str) -> None:
        """Prints and Logs if a command was received but is unable to be completed"""

        console = f"[{time}] -- Incorrect command syntax, try: !buy ['ticker-symbol'] or !sell ['ticker-symbol']"
        logging.error(console)


    def notFound(self, ticker: str, time: str) -> None:
        """Prints and Logs error if order is placed for symbol that does not exist"""

        console = f"[{time}] -- No pricing data found for ticker ${ticker}"
        logging.error(console)