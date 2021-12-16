import yahoo_fin.stock_info as si

class PaperTrade:

    # Constructor
    # Initiates bank with $100,000 default cash
    # Initiates empty holdings dictionary
    # Initiates value to track share value as prices update
    def __init__(self) -> None:
        """Constructor"""
        self.init_bank = 100000
        self.bank = 100000
        self.holdings_value = 0
        self.pnl = 0
        self.holdings = {}


    def buy(self, ticker: str) -> None:
        """Purchase a single share of the given stock ticker."""
     
        # retrieving live price
        price = si.get_live_price(ticker)

        # checking if reference already exists in holdings
        # if no reference exists, create a new element with init values
        if ticker not in self.holdings.keys():
            self.holdings[ticker] = {'shares': 1, 'cost': price}
        # if reference already exists, update
        else:
            self.holdings[ticker]['shares'] += 1
            self.holdings[ticker]['cost'] += price

        # taking cost of share from cash stack
        self.bank -= price


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
                self.bank += price


    def getValue(self) -> None:
        # value to return
        newValue = 0

        # identifying current value of holdings by ticker
        for ticker in self.holdings.keys():
            shares = self.holdings[ticker]['shares']
            price = si.get_live_price(ticker)
            newValue += shares * price
        
        # assigning to value
        self.holdings_value = newValue


    def getpnl(self) -> None:
        # determine and assign PnL
        self.pnl = self.holdings_value - self.init_bank