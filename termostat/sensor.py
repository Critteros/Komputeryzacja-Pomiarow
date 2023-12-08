from PyQt6.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
from typing import NamedTuple
import traceback
import sys
import time
from loguru import logger

from .psu import PSU

from .debug import DEBUG

from .serial_port import SerialPort


class Sensor:
    def __init__(self, com_port):
        # self.serial_port = Serial(port=com_port)
        if DEBUG:
            from .mock_arduino import MockArduino

            self.serial_port = MockArduino()
        else:
            self.serial_port = SerialPort(port=com_port)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.serial_port.close()

    def close(self):
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


TARGET_VOLTAGE = 8.0
MAX_WT = 16.0


class SensorWorker(QRunnable):
    def __init__(
        self, sensor: Sensor, psu: PSU, filename: str | None, target_t: float
    ) -> None:
        super().__init__()
        self.signals = SensorWorkerSignals()
        self.psu = psu
        self.sensor = sensor
        self.filename = filename
        self.target_t = target_t
        self.running = True

    @pyqtSlot()
    def run(self) -> None:
        start_time = time.time()
        self.psu.set_output(True)

        file = None

        # open file
        if self.filename:
            file = open(self.filename, "w")

        try:
            while self.running:
                logger.debug("Reading from sensor in a thread")
                temp = self.sensor.read()
                self.signals.data.emit(SensorData(time.time() - start_time, temp))

                if file:
                    file.write(f"{time.time() - start_time},{temp}\n")
                    file.flush()

                if temp < self.target_t:
                    current = MAX_WT / TARGET_VOLTAGE
                    logger.debug(f"Setting wattage to {current*TARGET_VOLTAGE}")
                    self.psu.set_current(current)

                if temp > self.target_t:
                    logger.debug("Setting wattage to 0")
                    self.psu.set_current(0.0)

        except ValueError:
            pass
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.psu.close()
            self.sensor.close()
            if file:
                file.close()

    @pyqtSlot()
    def stop_worker(self):
        logger.debug("Stopping arduino thread")
        self.running = False
        self.signals.finished.emit()
