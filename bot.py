from broker import PaperTrade # to initiate paper trading instance
from plot import Plot
import pytchat
import sys
import time
from multiprocessing import Process # to run bot and chart in parallel

# test stream ID
# joma livestream ID -> PY8f1Z3nARo

class Bot:


#===============================
#   INIT
#===============================


    def __init__(self, trade_instance: PaperTrade) -> None:
        """Constructor"""

        # checking that user provided enough launch parameters
        self.checkSys()

        # assigning values from parameters through sys (terminal)
        self.start_time = time.time()
        
        # ID of youtube live stream to track
        self.stream_id = sys.argv[1]

        # instantiating trade instance
        self.pt = trade_instance


#===============================
#   MAIN
#===============================


    # main method to operate the bot
    def run(self) -> None:
        """Initiates chat monitor and trading"""

        # Instantiate chat pull passing stream ID to constructor
        chat = pytchat.create(video_id=self.stream_id)

        # Running to log
        self.isRunning(self.pt)

        # continuously evaluating new chat messages
        while ( chat.is_alive() ):

            # for each element in the continuously updated log
            for c in chat.get().sync_items():
                
                # checking if the message contains command prefix
                if c.message[0] == '!':

                    order = c.message.lower().split(' ')
                    
                    # parsing out single and multi-string commands
                    try:
                        command = order[0]
                        ticker = order[1]
                    except:
                        command = order[0]
                        ticker = 'N/A'
                    
                    # parsing message information
                    user = c.author.name
                    msg_time = c.datetime

                    # passing message details to the checkCommand() method to handle it
                    self.checkCommand(self.pt, command, ticker, user, msg_time)
            
            # adds updated information to the chart_data list
            self.pt.chartData()


#===============================
#   STATUS AND ACCESSORS
#===============================


    # ensures the user launched the app with the appropriate parameters
    def checkSys(self, trade_instance: PaperTrade) -> None:
        """Checks if user gave necessary arguments on launch"""

        if len(sys.argv) < 2:
            console = "Incorrect or insufficient arguments given. Try 'python bot.py <stream-ID>'"
            print(console)
            trade_instance.logError(console)
            quit()


    # initial validation that the bot is running and prints the initial arguments passed on launch to terminal
    def isRunning(self, trade_instance: PaperTrade) -> str:
        """Logs and returns initial data for bot"""

        stat = f"""
        ====== Bot is running ======
        Stream ID: {self.stream_id}
        Initial Balance: ${trade_instance.balance}

        """
        
        print(stat)
        trade_instance.logInfo(stat)


    # used to validate the commands that are being read from the live chat
    def checkCommand(self, trade_instance: PaperTrade, command: str, ticker: str, user: str, time: str) -> None:
        """Checks each chat message for matching command and then handles instruction"""

        # catches buy command and passes to the trade instance
        if command == '!buy':
            trade_instance.buy(ticker, user, time)

        # catches sell command and passes to the trade instance
        elif command == '!sell':
            trade_instance.sell(ticker, user, time)

        # passes request to update on current portfio value to trade instance
        elif command == '!update':
            trade_instance.getUpdate(time)

        # passes request for uptime update to log in date format
        elif command == '!uptime':
            trade_instance.getUptime(time)

        # *currently* prints dataframe of holdings to terminal
        elif command == '!holdings':
            trade_instance.getHoldings(trade_instance.holdings)

        # no matching command, produce command error
        else:
            trade_instance.commandError(time)


#===============================
#   RUN
#===============================

# live charting is still not function at the moment
# the chart will run as a seperate process, but is not pulling from the live updated date
# need to use pool with main process so that the chart process can access the newly updated chart data

# # main module check
# if __name__ == "__main__":
    
#     # creating a bot object to run different processes from
#     bot = Bot()

#     # assigning seperate process to charting interface
#     p = Process(target=bot.chart.run)
#     # starting process
#     p.start()

#     # calling run() method from bot.py to initiate trading
#     bot.run()

#     # joining the chart process after closing to the main process
#     p.join()