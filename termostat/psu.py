import time

from .serial_port import SerialPort

from .debug import DEBUG

class PSU:
    def __init__(self, com_port):
        if DEBUG:
            from .mock_psu import MockPSU

            self.serial_port = MockPSU()
        else:
            self.serial_port = SerialPort(port=com_port)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.set_output(False)
        self.serial_port.close()

    def read_voltage(self):
        # Construct the command to read the voltage
        command = "VSET1?"

        # Send the command to the Rokad Power device
        self.serial_port.write(command.encode())

        # Wait for a short time to allow the device to process the command
        time.sleep(0.1)

        # Read the response from the Rokad Power device
        response = self.serial_port.read_all().decode()

        return float(response)

    def set_output(self, enabled: bool):
        # Construct the command to set the output
        command = f"OUT{1 if enabled else 0}"

        # Send the command to the Rokad Power device
        self.serial_port.write(command.encode())

        # Wait for a short time to allow the device to process the command
        time.sleep(0.1)

    def set_voltage(self, voltage_value):
        # Construct the command to set the voltage
        command = f"VSET1:{voltage_value}"

        # Send the command to the Rokad Power device
        self.serial_port.write(command.encode())

        # Wait for a short time to allow the device to process the command
        time.sleep(0.1)

    def read_current(self):
        # Construct the command to read the voltage
        command = "ISET1?"

        # Send the command to the Rokad Power device
        self.serial_port.write(command.encode())

        # Wait for a short time to allow the device to process the command
        time.sleep(0.1)

        # Read the response from the Rokad Power device
        response = self.serial_port.read_all().decode().strip().replace("\x00", "")

        return float(response)

    def set_current(self, current_value):
        # Construct the command to set the voltage
        command = f"ISET1:{current_value:.2f}"
        print(command)

        # Send the command to the Rokad Power device
        self.serial_port.write(command.encode())

        # Wait for a short time to allow the device to process the command
        time.sleep(0.1)
