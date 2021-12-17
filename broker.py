from os import error
import yahoo_fin.stock_info as si

class PaperTrade:


    # Constructor
    # Initiates balance with $100,000 default cash
    # Initiates empty holdings dictionary
    # Initiates value to track share value as prices update
    def __init__(self, initial_balance=100000) -> None:
        """Constructs a paper trading instance"""
        self.init_balance = initial_balance
        self.balance = initial_balance
        self.holdings_value = 0
        self.pnl = 0
        self.holdings = {}
        self.order_count = 0


    # Purchase given ticker and update
    def buy(self, ticker: str) -> None:
        """Purchase a single share of the given stock ticker."""
        
        # retrieving live price
        try:
            price = si.get_live_price(ticker)
        except AssertionError:
            self.notFound(ticker)
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
            print(f"""Successfully purchased share of ${ticker.upper()} for ${price}""")

        # produce balance error
        else:
            self.balanceError(ticker)


    # Sell given ticker and update
    def sell(self, ticker: str) -> None:
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

                # adding profit/loss to cash stack
                self.balance += price
                self.order_count += 1

                # print to log
                print(f"""Successfully sold share of ${ticker.upper()} for ${price}""")
            
            # produce share count error
            else:
                self.shareCountError(ticker)
        
        # produce holdings error
        else:
            self.holdingsError(ticker)


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
    def getUpdate(self):
        """Output the PnL to log/terminal"""
        self.getValue()
        self.getpnl()
        print(f"""Current Profit/Loss: ${self.pnl}""")

    
    def balanceError(self, ticker) -> None:
        print(f"### There is not a large enough balance to purchase ${ticker} ###")

    
    def shareCountError(self, ticker) -> None:
        print(f"### There are no remaining shares of ${ticker} to sell ###")

    
    def holdingsError(self, ticker) -> None:
        print(f"### There are no holdings of ${ticker} currently in the portfolio ###")


    def commandError(self) -> None:
        print("### Incorrect command syntax, try: !buy ['ticker-symbol'] or !sell ['ticker-symbol'] ###")

    def notFound(self, ticker) -> None:
        print("### No pricing data found for ticker ${ticker} ###")