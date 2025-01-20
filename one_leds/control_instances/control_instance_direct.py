from one_leds.common.control_instance import ControlInstance
from one_leds.common.config import ControlInstanceConfig

# Conditional import
import platform
if platform.system() == "Linux" and "aarch64" in platform.machine():
    from rpi_ws281x import *


class ControlInstanceDirect(ControlInstance):
    def __init__(self, config_instance: ControlInstanceConfig):
        ControlInstance._init(self, config_instance)
        self._led_pin: int = config_instance.implementation.led_pin
        self._led_signal_freq_hz: int = config_instance.implementation.led_signal_freq_hz
        self._led_dma_channel: int = config_instance.implementation.led_dma_channel
        self._invert_signal: bool = config_instance.implementation.invert_signal
        self._pwm_channel: int = config_instance.implementation.pwm_channel

    def initialize(self) -> None:
        if platform.system() in ["Darwin", "Windows"]:
            raise NotImplementedError(
                "Direct control can't be used in Mac and Windows")
        self._instance: Adafruit_NeoPixel = Adafruit_NeoPixel(self.led_count,
                                                              self._led_pin,
                                                              self._led_signal_freq_hz,
                                                              self._led_dma_channel,
                                                              self._invert_signal)
        self._instance.begin()
        self.show()

    def show(self) -> None:
        for index, color in enumerate(self._colors):
            self._instance.setPixelColorRGB(
                index, self._red_lut[color.red], self._green_lut[color.green], self._blue_lut[color.blue])
        self._instance.show()
