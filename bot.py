from broker import PaperTrade # to initiate paper trading instance
from plot import Plot
import pytchat
import sys
import time
from multiprocessing import Process

# test stream ID
# joma livestream ID -> PY8f1Z3nARo

class Bot:


#===============================
#   INIT
#===============================


    def __init__(self) -> None:
        """Constructor"""

        # checking that user provided enough launch parameters
        self.checkSys()

        # assigning values from parameters through sys (terminal)
        self.start_time = time.time()
        self.init_balance = int(float(sys.argv[1]))
        self.stream_id = sys.argv[2]

        # instantiating trade instance
        self.pt = PaperTrade(self.init_balance)
        self.chart = Plot(self.pt.chart_data)


#===============================
#   MAIN
#===============================


    def run(self) -> None:
        """Initiates chat monitor and trading"""

        # Instantiate chat pull passing stream ID to constructor
        chat = pytchat.create(video_id=self.stream_id)

        # Running to log
        self.isRunning(self.pt)

        k = 1

        # continuously evaluating new chat messages
        while ( chat.is_alive() ):

            # for each element in the continuously updated log
            for c in chat.get().sync_items():
                
                # checking if the message contains command prefix
                if c.message[0] == '!':

                    order = c.message.lower().split(' ')
                    
                    try:
                        command = order[0]
                        ticker = order[1]
                    except:
                        command = order[0]
                        ticker = 'N/A'
                    
                    user = c.author.name
                    msg_time = c.datetime

                    self.checkCommand(self.pt, command, ticker, user, msg_time)
            
            # adds updated information to the chart_data list
            self.pt.chartData()
            print(self.pt.chart_data)


#===============================
#   STATUS AND ACCESSORS
#===============================


    def checkSys(self) -> None:
        """Checks if user gave necessary arguments on launch"""

        if len(sys.argv) < 3:
            print("Incorrect or insufficient arguments given. Try 'python bot.py <initial-cash> <stream-ID>'")
            quit()


    def isRunning(self, trade_instance: PaperTrade) -> str:
        """Logs and returns initial data for bot"""

        stat = f"""
        ====== Bot is running ======
        Stream ID: {self.stream_id}
        Initial Balance: ${trade_instance.balance}

        """
        
        trade_instance.toLog(stat)


    def checkCommand(self, trade_instance: PaperTrade, command: str, ticker: str, user: str, time: str) -> None:
        """Checks each chat message for matching command and then handles instruction"""

        # if buy command
        if command == '!buy':
            trade_instance.buy(ticker, user, time)

        # if sell command
        elif command == '!sell':
            trade_instance.sell(ticker, user, time)

        elif command == '!update':
            trade_instance.getUpdate(time)

        elif command == '!uptime':
            trade_instance.getUptime(time)

        elif command == '!holdings':
            trade_instance.getHoldings(trade_instance.holdings)

        # no matching command, produce command error
        else:
            trade_instance.commandError(time)


#===============================
#   RUN
#===============================


# main module check
if __name__ == "__main__":
    
    # creating a bot object to run different processes from
    bot = Bot()

    # assigning seperate process to charting interface
    p = Process(target=bot.chart.run)
    # starting process
    p.start()

    # calling run() method from bot.py to initiate trading
    bot.run()

    # joining the chart process after closing to the main process
    p.join()