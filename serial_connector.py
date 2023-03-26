import adafruit_board_toolkit.circuitpython_serial
import serial


class SerialConnector:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.serial  = None
        self.connected = False

    def connect(self):
        if self.port is None:
            self.port = self.detect_ports()
        if self.port is None:
            return False

        try:
            self.serial  = serial.Serial(self.port, self.baudrate)
        except:
            return False

        self.connected = True
        return True

    def disconnect(self):
        if self.connected:
            self.serial .close()

    def detect_ports(self):
        try:
            comports = adafruit_board_toolkit.circuitpython_serial.repl_comports()
            if comports:
                return comports[0].device
        except:
            pass
        return None


    def write(self, message):
        if self.serial  and self.serial .is_open:
            self.serial.write(message)
            print(message)
