import socket
from socket import AF_INET, SOCK_STREAM
from enum import Enum

class ProtocolError(Exception):
    def raise_exception(response, expected):
        raise ProtocolError("Server responded with '{0}' but expected {1}.\n".format(response, expected))

class SocketError(Exception):
    def raise_exception(connection_open, ip, port):
        if not connection_open:
            raise SocketError("You already closed the connection with the server.\n")
        else:
            raise SocketError("Could not connect to the RobotArm Server. Is the RobotArm Server running on ip '{0}' and port '{1}'?\n".format(ip, port))

class TimeoutError(Exception):
    def raise_exception(timeout):
        raise TimeoutError("The RobotArm server took more than '{0}' seconds to respond.\n".format(timeout))

class ValueError(Exception):
    def raise_exception():
        raise ValueError("Speed cant be lower than 0 or higher than 1.\n")


class Colors(Enum):
    red = 1
    blue = 2
    green = 3
    white = 4
    none = 5

class Controller:
    def __init__(self, address="127.0.0.1", port=9876):
        self._ip = address
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self._sock.connect((address, port))
            self._connection_open = True
        except:
            SocketError.raise_exception(True, self._ip, self._port)

        self._sock.settimeout(60)
        self._timeout = 60
        self._speed = 0.5

        response = self._receive()
        self._check_response(response, "hello", ["hello"])

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._sock.close()
        self._connection_open = False
        return False

    def _send(self, command):
        try:
            command += "\n"
            self._sock.sendall(str.encode(command))
        except:
            SocketError.raise_exception(self._connection_open, self._ip, self._port)
        return self._receive()

    def _receive(self):
        try:
            data = self._sock.recv(4096)
        except socket.timeout:
            TimeoutError.raise_exception(self._timeout)
        except socket.error:
            SocketError.raise_exception(self._connection_open, self._ip, self._port)

        return data.decode("utf-8")

    def _check_response(self, response, expected, *allowed):
        correct_resp = False
        if any(response in a for a in allowed):
            correct_resp = True
        if not correct_resp:
            ProtocolError.raise_exception(response, expected)


    def close(self):
        self._connection_open = False
        self._sock.close()


    def move_left(self):
        response = self._send("move left")
        self._check_response(response, "ok", ["ok", "bye"])


    def move_right(self):
        response = self._send("move right")
        self._check_response(response, "ok", ["ok", "bye"])


    def grab(self): 
        response = self._send("grab")
        self._check_response(response, "ok", ["ok", "bye"])


    def drop(self):
        response = self._send("drop")
        self._check_response(response, "ok", ["ok", "bye"])


    def scan(self):
        response = self._send("scan")
        self._check_response(response, "a color", ["red", "blue", "green", "white", "none", "bye"])

        if response == "red":
            return Colors.red
        elif response == "green":
            return Colors.green
        elif response == "blue":
            return Colors.blue
        elif response == "white":
            return Colors.white
        elif response == "none":
            return Colors.none


    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if (value < 0 or value > 1):
            ValueError.raise_exception()
        self._send("speed {0}".format(value))
        self._speed = value


    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._sock.settimeout(value)
        self._timeout = value