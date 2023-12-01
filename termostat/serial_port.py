import serial
import serial.tools.list_ports
from loguru import logger

BAUD_RATE = 9600
PARITY = serial.PARITY_NONE
BYTESIZE = serial.EIGHTBITS
STOPBITS = serial.STOPBITS_ONE
XONXOFF = False


class SerialPort(serial.Serial):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.baudrate = BAUD_RATE
        self.parity = PARITY
        self.bytesize = BYTESIZE
        self.stopbits = STOPBITS
        self.xonxoff = XONXOFF
        logger.debug(kwargs)


def get_port_list():
    ports = serial.tools.list_ports.comports()

    if not ports:
        return ["COM1", "COM2", "COM3"]
    
    return [port for port,_,_ in ports]
