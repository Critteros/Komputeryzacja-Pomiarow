from PyQt6.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
from typing import NamedTuple
import traceback
import sys
import time
from loguru import logger

from .debug import DEBUG

from .serial import Serial


class Sensor:
    def __init__(self, com_port):
        # self.serial_port = Serial(port=com_port)
        if DEBUG:
            from .mock_arduino import MockArduino

            self.serial_port = MockArduino()
        else:
            self.serial_port = Serial(port=com_port)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.serial_port.close()

    def read(self):
        response = self.serial_port.readline().decode().strip()
        return float(response)


class SensorData(NamedTuple):
    time: float
    temp: float


class SensorWorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    data = pyqtSignal(SensorData)


class SensorWorker(QRunnable):
    def __init__(self, sensor: Sensor) -> None:
        super().__init__()
        self.signals = SensorWorkerSignals()
        self.sensor = sensor
        self.running = True

    @pyqtSlot()
    def run(self) -> None:
        start_time = time.time()
        try:
            while self.running:
                logger.debug("Reading from sensor in a thread")
                temp = self.sensor.read()
                self.signals.data.emit(SensorData(time.time() - start_time, temp))
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()

    @pyqtSlot()
    def stop_worker(self):
        logger.debug("Stopping arduino thread")
        self.running = False
