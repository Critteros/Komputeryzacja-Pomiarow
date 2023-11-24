import serial, time


class Sensor:

    def __init__(self,com_port, baud_rate = 9600):
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.serial_port = serial.Serial(port=com_port)
        self.serial_port.baudrate = baud_rate
        self.serial_port.parity = serial.PARITY_NONE
        self.serial_port.bytesize = serial.EIGHTBITS
        self.serial_port.stopbits = serial.STOPBITS_ONE
        self.serial_port.xonxoff = False  # Disable software flow control8

    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.serial_port.close()

    def read(self):
        response = self.serial_port.readline().decode().strip()
        return float(response)