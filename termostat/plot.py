from PyQt6.QtWidgets import QWidget, QVBoxLayout

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class Plot(FigureCanvas):
    def __init__(
            self,
            max_points=50,
            x_label="Time",
            y_label="Temperature",
    ):

        self.color = 'darkgrey'
        self.y_min = 20
        self.y_max = 40

        self.fig = Figure(figsize=(5, 4), dpi=100)
        # colors
        self.fig.patch.set_alpha(0)
        self.ax = self.fig.add_subplot(111)
        self.ax.spines['top'].set_alpha(0)
        self.ax.spines['right'].set_alpha(0)
        self.ax.spines['bottom'].set_color(self.color)
        self.ax.spines['left'].set_color(self.color)
        self.ax.tick_params(axis='x', colors=self.color)
        self.ax.tick_params(axis='y', colors=self.color)
        # self.ax.set_ylim(self.y_min, self.y_max)

        super(Plot, self).__init__(self.fig)

        self.fig.tight_layout()

        self.x_label = x_label
        self.y_label = y_label

        self._x_data = []
        self._y_data = []
        self._max_points = max_points

        self.reset_plot()

    def add_point(self, x, y):
        if len(self._x_data) >= self._max_points:
            self._x_data.pop(0)
            self._y_data.pop(0)

        self._x_data.append(x)
        self._y_data.append(y)
        self.refresh()

    def set_max_points(self, max_points):
        self._max_points = max_points
        self._x_data = self._x_data[-self._max_points:]
        self._y_data = self._y_data[-self._max_points:]
        self.refresh()

    def reset_plot(self):
        self.ax.clear()
        self.ax.set_xlabel(self.x_label, color=self.color)
        self.ax.set_ylabel(self.y_label, color=self.color)
        self.ax.autoscale_view(True, True, False)
        # self.ax.set_ylim(self.y_min, self.y_max)
        self.ax.patch.set_alpha(0)

    def clear_plot(self):
            self._x_data = []
            self._y_data = []
            self.refresh()

    def refresh(self):
        self.reset_plot()
        self.ax.plot(self._x_data, self._y_data, color='slateblue')
        self.ax.relim()
        # self.ax.set_ylim(self.y_min, self.y_max)

        self.draw()
