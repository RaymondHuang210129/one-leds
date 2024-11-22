from leds_server.common.control_instance import ControlInstance
from leds_server.common.app import App
from leds_server.common.color import Color
import time
from typing import List


class ExampleApp(App):
    def __init__(self, instances: List[ControlInstance]):
        App.__init__(self, instances)
        self._sleep_ms = 50

    def get_info(self) -> str:
        return "Example App"

    def begin(self) -> None:
        while True:
            # self._fix_color(Color(255, 0, 128))
            # self._color_wipe(Color(255, 0, 0))
            # self._color_wipe(Color(0, 255, 0))
            # self._color_wipe(Color(0, 0, 255))
            # self._theater_chase(Color(127, 0, 0))
            # self._theater_chase(Color(0, 127, 0))
            # self._theater_chase(Color(0, 0, 127))
            # self._rainbow()
            self._rainbow_cycle()
            # self._theater_chase_rainbow()

    def _sleep(self) -> None:
        time.sleep(self._sleep_ms/1000.0)

    def _color_wipe(self, color: Color) -> None:
        for index in range(self._instances[0].led_count):
            self._instances[0].set_color(index, color)
            self._instances[0].show()
            self._sleep()

    def _theater_chase(self, color: Color) -> None:
        colors = [Color() for _ in range(self._instances[0].led_count)]
        for iteration in range(10):
            for length in range(3):
                for index in range(0, self._instances[0].led_count, 3):
                    if length + index >= self._instances[0].led_count:
                        continue
                    colors[length+index] = color
                self._instances[0].set_colors(colors)
                self._instances[0].show()
                for index in range(0, self._instances[0].led_count, 3):
                    if length + index >= self._instances[0].led_count:
                        continue
                    colors[length+index] = Color()

    def _wheel(self, index: int) -> None:
        if index < 85:
            return Color(index * 3, 255 - index * 3, 0)
        elif index < 170:
            index -= 85
            return Color(255 - index * 3, 0, index * 3)
        else:
            index -= 170
            return Color(0, index * 3, 255 - index * 3)

    def _rainbow(self) -> None:
        colors = [Color() for _ in range(self._instances[0].led_count)]
        for iteration in range(256):
            for index in range(self._instances[0].led_count):
                colors[index] = self._wheel((iteration+index) & 255)
            self._instances[0].set_colors(colors)
            self._instances[0].show()
            self._sleep()

    def _rainbow_cycle(self) -> None:
        colors = [Color() for _ in range(self._instances[0].led_count)]
        for interation in range(256):
            for index in range(self._instances[0].led_count):
                colors[index] = self._wheel(
                    (int(index * 256 / self._instances[0].led_count) + interation) & 255)
            self._instances[0].set_colors(colors)
            self._instances[0].show()
            self._sleep()

    def _theater_chase_rainbow(self) -> None:
        colors = [Color() for _ in range(self._instances[0].led_count)]
        for iteration in range(256):
            for length in range(3):
                for index in range(0, self._instances[0].led_count, 3):
                    if length + index >= self._instances[0].led_count:
                        continue
                    colors[index+length] = self._wheel((iteration+index) % 255)
                self._instances[0].set_colors(colors)
                self._instances[0].show()
                self._sleep()
                for index in range(0, self._instances[0].led_count, 3):
                    if length + index >= self._instances[0].led_count:
                        continue
                    colors[index+length] = Color()

    def _fix_color(self, color: Color):
        colors = [color for _ in range(self._instances[0].led_count)]
        self._instances[0].set_colors(colors)
        self._instances[0].show()
        self._sleep()
