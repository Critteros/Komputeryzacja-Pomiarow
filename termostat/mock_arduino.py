import time
import random


class MockArduino:
    def __init__(self) -> None:
        self.temp = 24.0

    def read(self):
        time.sleep(1)
        temp = self.temp
        self.temp += random.randint(-20, 20) / 10

        return str(temp).encode()

    def readline(self):
        return self.read()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def open(self):
        pass

    def close(self):
        pass
