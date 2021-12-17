import pytchat
from broker import PaperTrade # to initiate paper trading instance
import sys
import time
import datetime

# joma livestream ID -> PY8f1Z3nARo

class Bot:


    def __init__(self) -> None:
        """Constructor"""

        self.checkSys()
        self.start_time = time.time()
        self.init_balance = int(float(sys.argv[1]))
        self.stream_id = sys.argv[2]


#===============================
#   MAIN
#===============================


    def run(self) -> None:
        """Initiates chat monitor and trading"""

        # Instantiate paper trading instance
        pt = PaperTrade(self.init_balance)

        # Instantiate chat pull
        chat = pytchat.create(video_id=self.stream_id)

        # Running to log
        self.isRunning(pt)

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

                    self.checkCommand(pt, command, ticker, user, msg_time)


#===============================
#   STATUS AND ACCESSORS
#===============================


    def getUptime(self, trade_instance: PaperTrade, time: str) -> str:
        """Logs and returns uptime of bot from initialization"""

        trade_instance.getUptime(time)


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
        Initial Balance: {trade_instance.balance}

        """
        
        trade_instance.toLog(stat)


    def checkCommand(self, trade_instance: PaperTrade, command: str, ticker: str, user: str, time: str) -> None:
        # if buy command
        if command == '!buy':
            trade_instance.buy(ticker, user, time)

        # if sell command
        elif command == '!sell':
            trade_instance.sell(ticker, user, time)

        elif command == '!update':
            trade_instance.getUpdate(time)

        elif command == '!uptime':
            self.getUptime(trade_instance, time)

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
    Bot().run()