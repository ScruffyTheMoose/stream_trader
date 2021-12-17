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

                    self.checkCommand(pt, command, ticker)


    def getUptime(self) -> None:
        """Logs uptime of bot from start"""

        uptime_sec = time.time() - self.start_time
        conversion = datetime.timedelta(seconds=uptime_sec)
        uptime_min = str(conversion)
        print(f"""Current uptime: {uptime_min}""")


    def checkSys(self) -> None:
        """Checks if user gave necessary arguments on launch"""

        if len(sys.argv) < 3:
            print("Incorrect or insufficient arguments given. Try 'python bot.py <initial-cash> <stream-ID>'")
            quit()


    def isRunning(self, pt: PaperTrade) -> None:
        """Logs initial data for bot"""

        print(f"""
                    == Bot is running ==
                Stream ID: {self.stream_id}
                Initial Balance: {pt.balance}
            """)


    def checkCommand(self, pt: PaperTrade, command: str, ticker: str) -> None:
        # if buy command
        if command == '!buy':
            pt.buy(ticker)

        # if sell command
        elif command == '!sell':
            pt.sell(ticker)

        elif command == '!update':
            pt.getUpdate()

        elif command == '!uptime':
            self.getUptime()

        # no matching command, produce command error
        else:
            pt.commandError()


# main module check
if __name__ == "__main__":
    Bot().run()