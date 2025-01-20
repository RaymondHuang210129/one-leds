from pydantic import BaseModel, Field
from typing import List, Union, Tuple
import json


class GammaCorrection(BaseModel):
    red_gamma: float
    red_max: int
    green_gamma: float
    green_max: int
    blue_gamma: float
    blue_max: int


class DirectAccess(BaseModel):
    led_pin: int
    led_signal_freq_hz: int
    led_dma_channel: int
    invert_signal: bool
    pwm_channel: int


class RemoteAccess(BaseModel):
    ip: str
    port: int


class ControlInstanceConfig(BaseModel):
    led_count: int
    color_correction: GammaCorrection
    implementation: Union[DirectAccess, RemoteAccess] = Field(
        union_mode='left_to_right')


class ExampleAppConfig(BaseModel):
    sleep_ms: int
    fixed_color: bool
    color_wipe: bool
    theater_chase: bool
    rainbow: bool
    rainbow_cycle: bool
    theater_chase_rainbow: bool


class ColorServerConfig(BaseModel):
    listen_port: int


class MusicDanceConfig(BaseModel):
    chunk_size: int
    compute_max_frequency: int
    decay_rate: int
    attack_threshold: int
    kick_max_frequency: int
    color_change_cool_down_period: int


class AppConfig(BaseModel):
    example_app: ExampleAppConfig
    color_server: ColorServerConfig
    music_dance: MusicDanceConfig


class Config(BaseModel):
    light_strips: List[ControlInstanceConfig]
    app_configs: AppConfig


def parse_config(input: json) -> Tuple[List[ControlInstanceConfig], AppConfig]:
    config: Config = Config.model_validate(input)
    instances = [light_strip for light_strip in config.light_strips]
    return instances, config.app_configs
