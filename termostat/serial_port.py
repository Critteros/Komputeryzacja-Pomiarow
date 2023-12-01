import serial
import serial.tools.list_ports

BAUD_RATE = 9600
PARITY = serial.PARITY_NONE
BYTESIZE = serial.EIGHTBITS
STOPBITS = serial.STOPBITS_ONE
XONXOFF = False


class SerialPort(serial.Serial):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.baudrate = PARITY
        self.parity = PARITY
        self.bytesize = BYTESIZE
        self.stopbits = STOPBITS
        self.xonxoff = XONXOFF


def get_port_list():
    ports = serial.tools.list_ports.comports()

    # for port, desc, hwid in sorted(ports):
    #     print("{}: {} [{}]".format(port, desc, hwid))

    # if port empty return example list
    if not ports:
        return ["COM1", "COM2", "COM3"]
