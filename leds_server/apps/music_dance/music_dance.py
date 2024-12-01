from leds_server.common.control_instance import ControlInstance
from leds_server.common.app import App
from leds_server.common.color import Color
from leds_server.common.config import AppConfig, MusicDanceConfig
import time
from typing import List, Dict, Tuple
import sounddevice as sd
import numpy as np


def get_loopback_device_index() -> Tuple[int, float]:
    devices: sd.DeviceList = sd.query_devices()
    for device in devices:
        if device['name'] == "BlackHole 2ch":
            return (device['index'], device['default_samplerate'])
    raise ValueError("Blackhole loopback device not found")


colors = [
    (1, 0, 0),
    (0.5, 0.5, 0),
    (0, 1, 0),
    (0, 0.5, 0.5),
    (0, 0, 1),
    (0.5, 0, 0.5),
]


class MusicDance(App):
    def __init__(self, instances: List[ControlInstance], app_config: AppConfig):
        App.__init__(self, instances)
        self._config: MusicDanceConfig = app_config.music_dance

        index, sample_rate = get_loopback_device_index()
        sd.default.device = (index, None)
        self._sample_rate: int = int(sample_rate)

    def get_info(self) -> str:
        return "Dancing LED with Realtime Sound Output"

    def _to_frequency_domain(self, time_series: np.ndarray[float]):
        freq_series: np.ndarray[np.complex128] = np.fft.rfft(time_series)
        frequencies: np.ndarray[float] = np.fft.rfftfreq(
            len(time_series), 1 / self._sample_rate)
        magnitudes = np.abs(freq_series)
        return frequencies, magnitudes

    def _audio_callback(self, indata: np.ndarray, frames: int, timestamp, status) -> None:
        frequencies, magnitudes = self._to_frequency_domain(indata[:, 0])

        kick_detected = False

        for freq_index in range(self._max_frequency_index):
            new_brightness: int = int(min(255, magnitudes[freq_index]))

            # Decay peak hold
            self._peak_brightness_hold[freq_index] = max(
                self._peak_brightness_hold[freq_index] - self._config.decay_rate, 0)

            # Detect kick
            if (frequencies[freq_index] < self._config.kick_max_frequency and
                    new_brightness - self._peak_brightness_hold[freq_index] > self._config.attack_threshold):
                kick_detected = True

            # Push up the peak hold if the brightness increases
            if new_brightness > self._peak_brightness_hold[freq_index]:
                self._peak_brightness_hold[freq_index] = new_brightness

        # Change color if kick detected and has cool down timer decrement to 0
        if kick_detected and self._color_change_cool_down_timer == 0:
            self._color_change_cool_down_timer = self._config.color_change_cool_down_period
            self._current_color_id = (self._current_color_id + 1) % 6
        else:
            self._color_change_cool_down_timer = max(
                self._color_change_cool_down_timer - 1, 0)

        for led_index in range(0, self._instances[0].led_count):
            mapped_freq_index: int = int(
                self._max_frequency_index * (led_index / self._instances[0].led_count))
            self._instances[0].set_color(led_index, Color(
                int(self._peak_brightness_hold[mapped_freq_index]
                    * colors[self._current_color_id][0]),
                int(self._peak_brightness_hold[mapped_freq_index]
                    * colors[self._current_color_id][1]),
                int(self._peak_brightness_hold[mapped_freq_index]
                    * colors[self._current_color_id][2]),
            ))

        self._instances[0].show()

    def begin(self) -> None:
        self._max_frequency_index = int(
            self._config.chunk_size * (self._config.compute_max_frequency / self._sample_rate))
        self._peak_brightness_hold = [0] * self._max_frequency_index
        self._current_color_id = 0
        self._color_change_cool_down_timer = 0

        with sd.InputStream(channels=1, samplerate=self._sample_rate, callback=self._audio_callback,
                            blocksize=self._config.chunk_size):
            while True:
                time.sleep(10)
