from leds_server.common.control_instance import ControlInstance
from leds_server.common.app import App
from leds_server.common.color import Color
from typing import List
from .util import UDPPacketReceiver, udp_payload_to_colors


class ColorServer(App):
    def __init__(self, instances: List[ControlInstance]):
        App.__init__(self, instances)
        self._udp_port = 5005

    def get_info(self) -> str:
        return "Light Strip Color Server"

    def begin(self) -> None:
        receiver: UDPPacketReceiver = UDPPacketReceiver(
            "0.0.0.0", self._udp_port)
        while True:
            payload: bytes = receiver.receive()
            colors: List[Color] = udp_payload_to_colors(payload)
            self._instances[0].set_colors(colors)
