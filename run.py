from bot import Bot
from broker import PaperTrade
from plot import Plot
from multiprocessing import Process


#===============================
#   RUN
#===============================


if __name__ == '__main__':
    
    # instantiate trade instance
    ti = PaperTrade()

    # instantiate bot passing trade instance as arg
    bot = Bot(ti)

    # instntiate plotting
    plot = Plot(ti.chart_data)

    # Creating individual processes for both plot and bot
    p1 = Process(target=plot.run)
    p2 = Process(target=bot.run)

    # starting processes
    p1.start()
    p2.start()

    # join processes after completion
    p1.join()
    p2.join()