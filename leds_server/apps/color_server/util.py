from leds_server.common.color import Color
from typing import List
import struct
import re
import socket


def udp_payload_to_colors(payload: bytes) -> List[Color]:
    padding_length: int = (3 - len(payload) % 3) % 3
    padded_payload = payload + b'\x00' * padding_length
    byte_list = struct.unpack(f'{len(padded_payload)}B', padded_payload)
    colors = [Color(red=byte_list[index], green=byte_list[index+1],
                    blue=byte_list[index+2]) for index in range(0, len(byte_list), 3)]
    return colors


class UDPPacketReceiver:
    def __init__(self, ip: str, port: int):
        if not re.search("^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$", ip):
            raise ValueError("Misformatted IPv4 address")
        if port < 1024 or port > 65535:
            raise ValueError("Unacceptable port number")

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((ip, port))

    def receive(self) -> bytes:
        # Maximum UDP payload of single packet when MTU is 1472
        data, _ = self._sock.recvfrom(1444)
        return data
