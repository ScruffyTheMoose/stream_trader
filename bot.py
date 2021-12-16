import pytchat
from broker import PaperTrade # to initiate paper trading instance
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

        print(f"""
            Current uptime: {uptime_min} minutes
        """)

    def run():
        """Initiates chat monitor and trading"""

        # get input for initial cash stack and initiate paper trading instance
        # start_cash = input("Enter starting cash stack:")
        init_balance = input("Enter initial trade balance: ")
        pt = PaperTrade(init_balance)

        # get input for channel ID and initiate chat instance
        # channel = input("Enter stream ID:")
        stream_id = input("Enter Youtube stream ID: ")
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

                    order = c.message.split(' ')
                    
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

                    # no matching command, produce command error
                    else:
                        pt.commandError()

                if pt.order_count > 0 and pt.order_count % 10 == 0:
                    pt.getValue()
                    pt.getpnl()


if __name__ == "__main__":
    Bot().run()