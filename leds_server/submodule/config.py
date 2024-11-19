from pydantic import BaseModel, ValidationError
from typing import List
import json

class GammaCorrection(BaseModel):
    red_gamma: float
    red_max: int
    green_gamma: float
    green_max: int
    blue_gamma: float
    blue_max: int

class ControlInstanceConfig(BaseModel):
    led_pin: int
    led_signal_freq_hz: int
    led_dma_channel: int
    invert_signal: bool
    pwm_channel: int
    led_count: int
    color_correction: GammaCorrection


def parse_config(input: json) -> List[ControlInstanceConfig]:
    instances = [ControlInstanceConfig(**item) for item in input]
    return instances
