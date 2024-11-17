from pydantic import BaseModel, ValidationError
from typing import List
import json

class ControlInstanceConfig(BaseModel):
    led_pin: int
    led_signal_freq_hz: int
    led_dma_channel: int
    invert_signal: bool
    pwm_channel: int
    led_count: int

def parse_config(input: json) -> List[ControlInstanceConfig]:
    instances = [ControlInstanceConfig(**item) for item in input]
    return instances
