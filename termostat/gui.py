import sys
import signal

from qtmodern import styles
from loguru import logger

from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QPushButton, QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import QThreadPool
from PyQt6 import uic

from .psu import PSU

from .plot import Plot

from .sensor import SensorWorker, SensorData, Sensor
from .serial_port import get_port_list


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # load ui
        self.ui = uic.loadUi('D:\\IS\\Piatek08_00\\project\\termostat\\main.ui', self)
        self.resize(888, 600)

        # add plot
        self.plot = Plot()
        self.ui.gridLayout_4.addWidget(self.plot, 2, 1, 1, 1)
        self.plot.setStyleSheet("background-color:transparent;")

        # init threadpool
        self.threadpool = QThreadPool()
        self.arduino_thread = None

        # window events
        self.init_controls()
        self.subscribe_to_window_events()

    def init_controls(self):
        ports = get_port_list()

        self.ui.comboBox_psu_port.addItems(ports)
        self.ui.comboBox_arduino_port.addItems(ports)

        self.ui.lineEdit_target_t.setValidator(QIntValidator(20, 50, self))
        # self.ui.comboBox_psu_port.setCurrentIndex(0)
        # self.ui.comboBox_arduino_port.setCurrentIndex(0)

    def subscribe_to_window_events(self):
        self.ui.pushButton_start.clicked.connect(self.start_plot)
        self.ui.pushButton_stop.clicked.connect(self.stop_arduino)

    def start_plot(self):
        self.disable_controls()

        # clear port
        self.plot.clear_plot()

        # start worker
        psu_port = self.ui.comboBox_psu_port.currentText()
        arduino_port = self.ui.comboBox_arduino_port.currentText()

        logger.debug(f"Starting arduino on port {arduino_port}")
        self.arduino_thread = SensorWorker(Sensor(arduino_port), PSU(psu_port))
        self.arduino_thread.setAutoDelete(True)
        self.arduino_thread.signals.data.connect(self.on_arduino_data)
        self.arduino_thread.signals.error.connect(self.on_worker_error)
        self.arduino_thread.signals.finished.connect(
            lambda: logger.debug("Arduino thread finished")
        )

        self.threadpool.start(self.arduino_thread)

    def stop_arduino(self):
        # stop worker
        self.arduino_thread.stop_worker()

        # unblock controls
        self.enable_controls()

    def enable_controls(self):
        self.ui.comboBox_psu_port.setEnabled(True)
        self.ui.comboBox_arduino_port.setEnabled(True)
        self.ui.lineEdit_target_t.setEnabled(True)
        self.ui.pushButton_save.setEnabled(True)
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)

    def disable_controls(self):
        self.ui.comboBox_psu_port.setEnabled(False)
        self.ui.comboBox_arduino_port.setEnabled(False)
        self.ui.lineEdit_target_t.setEnabled(False)
        self.ui.pushButton_save.setEnabled(False)
        self.ui.pushButton_start.setEnabled(False)
        self.ui.pushButton_stop.setEnabled(True)

    def on_worker_error(self, data):
        exctype, value, traceback = data
        logger.error(f"Error: {exctype}, {value}, {traceback}")

    def on_arduino_data(self, data: SensorData):
        logger.debug(f"Arduino data: {data}")
        self.plot.add_point(data.time, data.temp)

    def closeEvent(self, event):
        logger.debug("Closing")
        if self.arduino_thread:
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

    app.exec()
