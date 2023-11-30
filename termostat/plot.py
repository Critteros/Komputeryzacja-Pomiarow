from PyQt6.QtWidgets import QWidget, QVBoxLayout

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class Plot(QWidget):
    def __init__(
        self,
        max_points=50,
        x_label="Time",
        y_label="Temperature",
    ):
        super().__init__()
        layout = QVBoxLayout()

        self.setLayout(layout)
        self._figure = Figure()

        self.x_label = x_label
        self.y_label = y_label

        self._canvas = FigureCanvas(self._figure)
        layout.addWidget(self._canvas)

        self.ax = self._figure.add_subplot()
        self.reset_plot()

        self._x_data = []
        self._y_data = []
        self._max_points = max_points

    def add_point(self, x, y):
        if len(self._x_data) >= self._max_points:
            self._x_data.pop(0)
            self._y_data.pop(0)

        self._x_data.append(x)
        self._y_data.append(y)
        self.draw()

    def set_max_points(self, max_points):
        self._max_points = max_points
        self._x_data = self._x_data[-self._max_points :]
        self._y_data = self._y_data[-self._max_points :]
        self.draw()

    def reset_plot(self):
        self.ax.clear()
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.ax.autoscale_view(True, True, True)

    def draw(self):
        self.reset_plot()
        self.ax.plot(self._x_data, self._y_data)
        self.ax.relim()

        self._canvas.draw()
