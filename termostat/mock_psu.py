import re


class MockPSU:
    def __init__(self) -> None:
        self.current = 0.0
        self.voltage = 0.0
        self.next_read = b""

    def read(self):
        return self.next_read

    def read_all(self):
        return self.read()

    def write(self, encoded_str: bytes):
        command = encoded_str.decode()

        match command:
            case "ISET1?":
                self.next_read = f"{self.current}".encode()
            case "VSET1?":
                self.next_read = f"{self.voltage}".encode()
            case _ if (match_res := re.match(r"ISET1:(?P<value>[\d.]+)", command)):
                value = float(match_res.group("value"))
                self.current = value
            case _ if (match_res := re.match(r"VSET1:(?P<value>[\d.]+)", command)):
                value = float(match_res.group("value"))
                self.voltage = value
            case _:
                pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def open(self):
        pass

    def close(self):
        pass
