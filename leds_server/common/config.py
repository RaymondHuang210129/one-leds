from pydantic import BaseModel, Field
from typing import List, Union
import json


class GammaCorrection(BaseModel):
    red_gamma: float
    red_max: int
    green_gamma: float
    green_max: int
    blue_gamma: float
    blue_max: int


class Direct(BaseModel):
    led_pin: int
    led_signal_freq_hz: int
    led_dma_channel: int
    invert_signal: bool
    pwm_channel: int


class Remote(BaseModel):
    ip: str
    port: int


class ControlInstanceConfig(BaseModel):
    led_count: int
    color_correction: GammaCorrection
    implementation: Union[Direct, Remote] = Field(union_mode='left_to_right')


def parse_config(input: json) -> List[ControlInstanceConfig]:
    instances = [ControlInstanceConfig(**item) for item in input]
    return instances
