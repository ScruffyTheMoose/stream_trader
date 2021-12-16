import pytchat
from broker import PaperTrade # to initiate paper trading instance
import sys
import time
import datetime

# example chat access for reference
# print(f"{c.datetime} [{c.author.name}]- {c.message}")

class Bot:


    def __init__(self) -> None:
        """Constructor"""
        self.start_time = time.time()


    def getUptime(self) -> None:
        uptime_sec = time.time() - self.start_time
        conversion = datetime.timedelta(seconds=uptime_sec)
        uptime_min = str(conversion)

        print(f"""Current uptime: {uptime_min}""")


    def checkSys(self) -> None:
        if len(sys.argv) < 3:
            print("Incorrect or insufficient arguments given. Try 'python bot.py <initial-cash> <stream-ID>'")
            quit()


    def run(self) -> None:
        """Initiates chat monitor and trading"""

        self.checkSys()

        # get input for initial cash stack and initiate paper trading instance
        init_balance = int(float(sys.argv[1]))
        pt = PaperTrade(init_balance)

        # get input for channel ID and initiate chat instance
        stream_id = sys.argv[2]
        chat = pytchat.create(video_id=stream_id)

        # print to log that bot is running
        print(f"""
                    == Bot is running ==
                Stream ID: {stream_id}
                Initial Balance: {pt.bank}
            """)

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