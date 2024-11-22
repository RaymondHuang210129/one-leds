from rpi_ws281x import *
from .config import ControlInstanceConfig, GammaCorrection
from .color import Color
from typing import List, Union
from .config import Direct, Remote


class ControlInstance:
    def _init(self, config_instance: ControlInstanceConfig):
        color_correction: GammaCorrection = config_instance.color_correction
        self._red_lut: List[int] = self._create_brightness_lut(
            color_correction.red_gamma, color_correction.red_max)
        self._green_lut: List[int] = self._create_brightness_lut(
            color_correction.green_gamma, color_correction.green_max)
        self._blue_lut: List[int] = self._create_brightness_lut(
            color_correction.blue_gamma, color_correction.blue_max)
        self.led_count: int = config_instance.led_count
        self._colors: List[Color] = [Color() for _ in range(self.led_count)]

    def initialize(self) -> None:
        raise NotImplementedError()

    def set_colors(self, colors: List[Color]) -> None:
        if len(colors) < self.led_count:
            colors.extend([Color()
                          for _ in range(self.led_count - len(colors))])
            self._colors = colors
        elif len(colors) > self.led_count:
            self._colors = colors[0:self.led_count]
        else:
            self._colors = colors

    def set_color(self, index: int, color: Color) -> None:
        if index >= 0 and index < self.led_count:
            self._colors[index] = color

    def get_colors(self) -> List[Color]:
        return self._colors

    def get_color(self, index: int) -> Color:
        return self._colors[index]

    def show(self) -> None:
        raise NotImplementedError

    def _create_brightness_lut(self, gamma: float, max: int) -> List[int]:
        lookup_table: List[int] = []
        for input in range(0, 256):
            lookup_table.append(int(pow(input / 255, gamma) * max))
        return lookup_table
