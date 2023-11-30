import serial

BAUD_RATE = 9600
PARITY = serial.PARITY_NONE
BYTESIZE = serial.EIGHTBITS
STOPBITS = serial.STOPBITS_ONE
XONXOFF = False


class Serial(serial.Serial):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.baudrate = PARITY
        self.parity = PARITY
        self.bytesize = BYTESIZE
        self.stopbits = STOPBITS
        self.xonxoff = XONXOFF
