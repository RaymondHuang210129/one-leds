from one_leds.common.control_instance import ControlInstance
from one_leds.common.config import ControlInstanceConfig
import socket
import time


class ControlInstanceRemote(ControlInstance):
    def __init__(self, config_instance: ControlInstanceConfig):
        ControlInstance._init(self, config_instance)
        self._ip = config_instance.implementation.ip
        self._port = config_instance.implementation.port
        self._count = config_instance.led_count

    def initialize(self) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return

    def show(self) -> None:
        payload: bytearray = bytearray(self._count * 3)
        for index, color in enumerate(self._colors):
            payload[index * 3] = self._red_lut[color.red]
            payload[index * 3 + 1] = self._green_lut[color.green]
            payload[index * 3 + 2] = self._blue_lut[color.blue]
        self._socket.sendto(payload, (self._ip, self._port))
