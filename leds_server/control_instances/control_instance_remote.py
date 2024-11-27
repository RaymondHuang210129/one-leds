from leds_server.common.control_instance import ControlInstance
from leds_server.common.config import ControlInstanceConfig
import socket
import time


class ControlInstanceRemote(ControlInstance):
    def __init__(self, config_instance: ControlInstanceConfig):
        ControlInstance._init(self, config_instance)
        self._ip = config_instance.implementation.ip
        self._port = config_instance.implementation.port

    def initialize(self) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return

    def show(self) -> None:
        payload: bytearray = bytearray()
        for color in self._colors:
            payload.append(self._red_lut[color.red])
            payload.append(self._green_lut[color.green])
            payload.append(self._blue_lut[color.blue])
        self._socket.sendto(payload, (self._ip, self._port))
