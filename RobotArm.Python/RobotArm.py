import socket
from socket import AF_INET, SOCK_STREAM

class ProtocolError(Exception):
    pass

class SocketError(Exception):
    pass

class TimeoutError(Exception):
    pass

class RobotArm:
    def __init__(self, address, port):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self._sock.connect((address, port))
        except:
            raise SocketError("Could not connect to the socket")

        self._sock.settimeout(60)
        self._timeout = 60
        self._speed = 0.5
        self._receive()
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._sock.close()
        return isinstance(value, TypeError)

    def _send(self, command):
        try:
            self._sock.sendall(str.encode(command))
        except:
            raise SocketError("Connection has been lost")
        return self._receive()

    def _receive(self):
        try:
            data = self._sock.recv(4096)
        except socket.timeout:
            raise TimeoutError("Connection timed out")
        except socket.error:
            raise SocketError("Connection has been lost")

        str = data.decode("utf-8")
        print(str)

        if str != "none" and str != "red" and str != "blue" and str != "green" and str != "white" and str != "hello" and str != "ok" and str != "bye":
            raise ProtocolError("Server responded wrong")

        return str

    def close(self):
        self._sock.close()

    def move_left(self):
        self._send("move left")

    def move_right(self):
        self._send("move right")

    def grab(self):
        self._send("grab")

    def drop(self):
        self._send("drop")

    def scan(self):
        return self._send("scan")


    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if (value < 0 or value > 1):
            raise ValueError("speed cant be lower than 0 or higher than 1")
        self._send(str("speed " + str(value)))
        self._speed = value

    @property
    def timeout(self):
        return self._speed

    @timeout.setter
    def timeout(self, value):
        self._sock.settimeout(value)
        self._timeout = value