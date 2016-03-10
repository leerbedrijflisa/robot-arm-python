import socket
from socket import AF_INET, SOCK_STREAM
from enum import Enum

class ProtocolError(Exception):
    pass

class SocketError(Exception):
    pass

class TimeoutError(Exception):
    pass

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
        self._connection_open = True

        try:
            self._sock.connect((address, port))
        except:
            self.raise_socket_error()

        self._sock.settimeout(60)
        self._timeout = 60
        
        self._speed = 0.5
        response = self._receive()
        if response != "hello":
            self.raise_protocol_error(response, "hello")

        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._connection_open = False
        self._sock.close()
        return False

    def _send(self, command):
        try:
            command += "\n"
            self._sock.sendall(str.encode(command))
        except:
            self.raise_socket_error()
        return self._receive()

    def _receive(self):
        try:
            data = self._sock.recv(4096)
        except socket.timeout:
            self.raise_timeout_error()
        except socket.error:
            self.raise_socket_error()

        return data.decode("utf-8")


    def close(self):
        self._connection_open = False
        self._sock.close()

    def move_left(self):
        response = self._send("move left")
        if response != "ok" and response != "bye":
            self.raise_protocol_error(response, "ok")

    def move_right(self):
        response = self._send("move right")
        if response != "ok" and response != "bye":
            self.raise_protocol_error(response, "ok")

    def grab(self): 
        response = response = self._send("grab")
        if response != "ok" and response != "bye":
            self.raise_protocol_error(response, "ok")

    def drop(self):
        response = self._send("drop")
        if response != "ok" and response != "bye":
            self.raise_protocol_error(response, "ok")

    def scan(self):
        response = self._send("scan")
        if response != "none" and response != "red"  and response != "blue" and response != "green" and response != "white" and response != "bye":
            self.raise_protocol_error(response, "a color")

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
            self.raise_value_error(0, 1)
        self._send(str("speed " + str(value)))
        self._speed = value

    @property
    def timeout(self):
        return self._speed

    @timeout.setter
    def timeout(self, value):
        self._sock.settimeout(value)
        self._timeout = value



    def raise_protocol_error(self, response, expected):
        raise ProtocolError("Server responded with '{0}' but expected {1}.".format(response, expected))
     
    def raise_socket_error(self):
        if not self._connection_open:
            raise SocketError("You already closed the connection with the server.")
        else:
            raise SocketError("Could not connect to the RobotArm Server. Is the RobotArm Server running on ip '{0}' and port '{1}'?".format(self._ip, self._port))

    def raise_timeout_error(self):
        raise TimeoutError("The RobotArm server took more than '{0}' seconds to respond.".format(self._timeout))

    def raise_value_error(self, min, max):
        raise ValueError("speed cant be lower than {0} or higher than {1}", min, max)