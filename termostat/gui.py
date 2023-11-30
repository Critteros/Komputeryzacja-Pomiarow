import sys
import signal

from qtmodern import styles
from loguru import logger

from PyQt6.QtWidgets import QPushButton, QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import QThreadPool

from .plot import Plot

from .sensor import SensorWorker, SensorData, Sensor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Termostat")
        self._widget = QWidget()
        self.setMinimumSize(800, 600)
        self.setCentralWidget(self._widget)

        layout = QVBoxLayout()
        self._widget.setLayout(layout)

        self.plot = Plot()
        layout.addWidget(self.plot)

        self.threadpool = QThreadPool()

    def start_arduino(self, arduino_port: str = "COM3"):
        logger.debug(f"Starting arduino on port {arduino_port}")
        with Sensor(arduino_port) as sensor:
            self.arduino_thread = SensorWorker(sensor)
            self.arduino_thread.signals.data.connect(self.on_arduino_data)
            self.arduino_thread.signals.error.connect(self.on_worker_error)
            self.arduino_thread.signals.finished.connect(
                lambda: logger.debug("Arduino thread finished")
            )

            self.threadpool.start(self.arduino_thread)

    def on_worker_error(self, data):
        exctype, value, traceback = data
        logger.error(f"Error: {exctype}, {value}, {traceback}")

    def on_arduino_data(self, data: SensorData):
        logger.debug(f"Arduino data: {data}")
        self.plot.add_point(data.time, data.temp)

    def closeEvent(self, event):
        logger.debug("Closing")
        self.arduino_thread.stop_worker()


def on_interrupt(*args):
    logger.debug("Interrupted exiting")
    QApplication.quit()


def main():
    signal.signal(signal.SIGINT, on_interrupt)
    app = QApplication(sys.argv)

    styles.dark(app)

    window = MainWindow()
    window.show()

    window.start_arduino()
    app.exec()
