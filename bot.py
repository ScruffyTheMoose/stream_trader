import pytchat
from broker import PaperTrade # to initiate paper trading instance

# example chat access for reference
# print(f"{c.datetime} [{c.author.name}]- {c.message}")

def run():

    # get input for initial cash stack and initiate paper trading instance
    start_cash = input("Enter starting cash stack:")
    pt = PaperTrade(100000)

    # get input for channel ID and initiate chat instance
    channel = input("Enter stream ID:")
    chat = pytchat.create(video_id='l20Jiimi1Mc')


    # continuously evaluating new chat messages
    while ( chat.is_alive() ):

        # for each element in the continuously updated log
        for c in chat.get().sync_items():
            
            # checking if the message contains command prefix
            if c.message[0] == '!':
                print("Command recieved")

                order = c.message.split()

                command = order[0]
                ticker = order[1]

                # if buy command
                if command == '!buy':
                    pt.buy(ticker)

                # if sell command
                elif command == '!sell':
                    pt.sell(ticker)

                # no matching command, produce command error
                else:
                    pt.commandError()

            if pt.order_count % 10 == 0:
                pt.getValue()
                pt.getpnl()


if __name__ == "__main__":
    run()