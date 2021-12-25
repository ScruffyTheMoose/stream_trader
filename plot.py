import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
style.use('seaborn') # setting style for all instances


class Plot:


#===============================
#   INIT
#===============================


    # constructor initializes the figure, the axis/subplot
    # stores a reference to the live data feed from the trade instance that is passed as argument
    def __init__(self, chart_data: list) -> None:
        """Constuctor initializes figure and axis"""

        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
        self.graph_data = chart_data # the log reference will be an instance variable stored in trade instance


#===============================
#   ANIMATION
#===============================


    # will clear and redraw the plot with updated data as it is called through FuncAnimation
    def animate(self, i) -> None:
        """Animation method to be passed into FuncAnimation"""

        xs = []
        ys = []
        for pair in self.graph_data:
            xs.append(pair[0])
            ys.append(pair[1])

        self.ax1.clear()
        self.ax1.plot(xs, ys)


    # saves animation to variable and shows the plot
    def run(self):
        """Creates instantiates plot GUI"""

        # setting refresh time to 2500ms
        anim = animation.FuncAnimation(self.fig, self.animate, interval=2500)
        plt.show()


#===============================
#   ETC
#===============================


    # temporary method for testing draw vs show while using multiprocessing
    def showFinal(self):
        """If using draw, call this method to retain plot after completion of operation"""
        plt.show