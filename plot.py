import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
style.use('seaborn') # setting style for all instances


class Plot:


    def __init__(self, chart_data: list) -> None:
        """Constuctor initializes figure and axis"""

        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
        self.graph_data = chart_data # the log reference will be an instance variable stored in trade instance


    def animate(self, i) -> None:
        """Animation method to be passed into FuncAnimation"""

        xs = []
        ys = []
        for pair in self.graph_data:
            xs.append(pair[0])
            ys.append(pair[1])

        self.ax1.clear()
        self.ax1.plot(xs, ys)


    def run(self):
        """Creates instantiates plot GUI"""

        # setting refresh time to 2500ms
        anim = animation.FuncAnimation(self.fig, self.animate, interval=2500)
        plt.show()

    def showFinal(self):
        plt.show