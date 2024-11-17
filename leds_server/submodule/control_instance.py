from rpi_ws281x import *
from .config import ControlInstanceConfig
from .color import Color
from typing import List

class ControlInstance:
    def __init__(self, config_instance: ControlInstanceConfig):
        self._led_pin: int = config_instance.led_pin
        self._led_signal_freq_hz: int = config_instance.led_signal_freq_hz
        self._led_dma_channel: int = config_instance.led_dma_channel
        self._invert_signal: bool = config_instance.invert_signal
        self._pwm_channel: int = config_instance.pwm_channel
        self.led_count: int = config_instance.led_count

    def initialize(self) -> None:
        self._instance: Adafruit_NeoPixel = Adafruit_NeoPixel(self.led_count,
                                                              self._led_pin,
                                                              self._led_signal_freq_hz,
                                                              self._led_dma_channel,
                                                              self._invert_signal)
        self._instance.begin()
        self._colors: List[Color] = [Color() for _ in range(self.led_count)]
        self.show()

    def set_colors(self, colors: List[Color]):
        if len(colors) < self.led_count:
            colors.extend([Color() for _ in range(self.led_count - len(colors))])
            self._colors = colors
        elif len(colors) > self.led_count:
            self._colors = colors[0:self.led_count]
        else:
            self._colors = colors
        self.show()
        
    def set_color(self, index: int, color: Color):
        if index >= 0 and index < self.led_count:
            self._colors[index] = color
        self.show()

    def get_colors(self):
        return self._colors
    
    def get_color(self, index: int):
        return self._colors[index]

    def show(self):
        for index, color in enumerate(self._colors):
            self._instance.setPixelColorRGB(index, color.red, color.green, color.blue)
        self._instance.show()
