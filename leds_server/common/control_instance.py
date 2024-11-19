from rpi_ws281x import *
from .config import ControlInstanceConfig, GammaCorrection
from .color import Color
from typing import List


class ControlInstance:
    def __init__(self, config_instance: ControlInstanceConfig):
        self._led_pin: int = config_instance.led_pin
        self._led_signal_freq_hz: int = config_instance.led_signal_freq_hz
        self._led_dma_channel: int = config_instance.led_dma_channel
        self._invert_signal: bool = config_instance.invert_signal
        self._pwm_channel: int = config_instance.pwm_channel

        color_correction: GammaCorrection = config_instance.color_correction
        self._red_lut: List[int] = self._create_brightness_lut(
            color_correction.red_gamma, color_correction.red_max)
        self._green_lut: List[int] = self._create_brightness_lut(
            color_correction.green_gamma, color_correction.green_max)
        self._blue_lut: List[int] = self._create_brightness_lut(
            color_correction.blue_gamma, color_correction.blue_max)

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

    def set_colors(self, colors: List[Color]) -> None:
        if len(colors) < self.led_count:
            colors.extend([Color()
                          for _ in range(self.led_count - len(colors))])
            self._colors = colors
        elif len(colors) > self.led_count:
            self._colors = colors[0:self.led_count]
        else:
            self._colors = colors
        self.show()

    def set_color(self, index: int, color: Color) -> None:
        if index >= 0 and index < self.led_count:
            self._colors[index] = color
        self.show()

    def get_colors(self) -> List[Color]:
        return self._colors

    def get_color(self, index: int) -> Color:
        return self._colors[index]

    def show(self) -> None:
        for index, color in enumerate(self._colors):
            self._instance.setPixelColorRGB(
                index, self._red_lut[color.red], self._green_lut[color.green], self._blue_lut[color.blue])
            # self._instance.setPixelColorRGB(
            #     index, color.red, color.green, color.blue)
        self._instance.show()

    def _create_brightness_lut(self, gamma: float, max: int) -> List[int]:
        lookup_table: List[int] = []
        for input in range(0, 256):
            lookup_table.append(int(pow(input / 255, gamma) * max))
        return lookup_table
