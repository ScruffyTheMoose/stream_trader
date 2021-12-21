import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
style.use('seaborn') # setting style for all instances


class Plot:


    def __init__(self, anim_log: str) -> None:
        """Constuctor initializes figure and axis"""

        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
        self.file = anim_log # the log reference will be an instance variable stored in trade instance


    def animate(self, i) -> None:
        """Animation method to be passed into FuncAnimation"""

        graph_data = open(self.file, 'r').read()
        lines = graph_data.split("\n")
        xs = []
        ys = []
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xs.append(x)
                ys.append(y)

        self.ax1.clear()
        self.ax1.plot(xs, ys)


    def run(self):
        """Creates instantiates plot GUI"""

        # setting refresh time to 2500ms
        anim = animation.FuncAnimation(self.fig, self.animate, interval=2500)
        plt.show()