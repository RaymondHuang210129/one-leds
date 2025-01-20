# OneLeds

A cross-platform application for controlling LED light strips with versatile configurations and features.  

## Table of Contents  

1. [About](#about)  
2. [Features](#features)  
3. [Installation](#installation)  
   - [Hardware Configurations](#hardware-configurations)  
   - [App Configurations](#app-configurations)
4. [Usage](#usage)
   - [ExampleApp](#exampleapp)
   - [MusicDance](#musicdance)
5. [Contributing](#contributing)  
6. [License](#license)  

## About  

**LEDs Server** is a Python-based project that provides a unified solution for controlling LED light strips, regardless of the connection method or platform.  

This project is divided into two main components:  

### 1. LED Control Modes  
- **Direct Control Mode** (`ControlInstanceDirect`):  
  Directly controls LED strip colors using GPIO pins on microcomputers like Raspberry Pi.  

- **Remote Control Mode** (`ControlInstanceRemote`):  
  Controls LED strip colors by sending UDP packets, enabling use on any platform (macOS, Windows, Linux).  

### 2. LED Applications  
- **ExampleApp**:  
  Offers dynamic color effects.  

- **ColorServer**:  
  Designed for microcomputers to control LED strips by receiving UDP packets.  

- **MusicDance**:  
  Cross-platform app for real-time audio-visual synchronization, capturing device audio output to control LED colors.  

## Features  

### 1. Versatile Control Modes  
- Supports both microcomputers with GPIO pins and general computers.  
- Allows users to configure LED strips either directly attached to a microcomputer or via MCUs receiving UDP packets.  
- Developers can extend functionality by inheriting from the `ControlInstance` class.  

### 2. Multi-LED Strip Support  
- Control multiple LED strip instances simultaneously, defined in a configuration file.  
- Supports hybrid setups, combining different control modes.  
- No software limitation on the number of LED strips; limitations depend on hardware resources (e.g., PWM channels, router throughput).  

### 3. Unified Application Framework  
- Built on the `App` base class, providing consistent access to all LED strip instances (`self._instances`).  
- Developers can create new applications easily using this framework.  

## Installation  

### Hardware Configurations  

Users can connect LED strips either directly to a microcomputer or via an MCU.  

#### Configuration 1: Direct Connection to a Microcomputer  

- **Setup**:  
  - Attach LED strips to the PWM pins of a microcomputer (e.g., Raspberry Pi).  
  - Run the program locally on the microcomputer.  

- **How it Works**:  
  - The microcomputer directly controls the LED strips through its GPIO pins.  

- **Config File**:  
  - Define LED strip instances in the config file with the following parameters:  
    - Set the `implementation` field to the `DirectAccess` schema.  
    - Specify hardware-specific settings such as GPIO pins and PWM parameters.  

- **Limitations**:  
  - Some microcomputers, such as Raspberry Pi, share hardware resources between PWM controllers and audio output.  
  - If both PWM channels are used, applications like `MusicDance` that interact with real-time audio may not function.  

#### Configuration 2: MCU Connection with Remote Control  

- **Setup**:  
  - Connect LED strips to an MCU (e.g., ESP32).  
  - Program the MCU to listen for UDP packets and control the LED strips accordingly.  

- **How it Works**:  
  - Each UDP packet contains RGB color data for an LED strip.  
  - The payload is structured such that each LED's color is represented by 3 bytes (RGB).  
  - For a strip with `N` LEDs, the payload length must be `3 * N` bytes.  
  - The MCU decodes the payload and updates the LED strip colors.  

- **Multiple LED Strips per MCU**:  
  - An MCU can control multiple LED strips by assigning a unique UDP port to each strip.  
  - The MCU listens to all assigned ports and processes packets independently for each strip.  

- **Config File**:  
  - Define LED strip instances in the config file with the following parameters:  
    - Set the `implementation` field to the `RemoteAccess` schema.  
    - Specify the IP address and port number for each LED strip.  

- **Network Requirements**:  
  - All MCUs and the controlling computer must connect to the same network.  
  - The computer runs the program and sends UDP packets to the MCUs to control the LED strips remotely.  

#### Configuration 3: Hybrid Setup  
- Combine **Configuration 1** and **Configuration 2** for greater flexibility.  
- Microcomputers must run the `ColorServer` app, connect to the same network, and have main computer running the program if controlled remotely.

### App Configurations

App configurations are defined under `app_configs` section of config file. Users should have those configurations matching `AppConfig` schema.

For each application specifically:

#### ExampleApp
- `integer sleep_ms`: The interval between each frame of color change.
- `boolean fixed_color`: Whether to enable fix color mode.
- `boolean color_wipe`: Whether to enable color wipe effect.
- `boolean theater_chase`: Whether to enable theater chase effect.
- `boolean rainbow`: Whether to enable rainbow mode.
- `boolean rainbow_cycle`: Whether to enable rainbow cycle effect.
- `boolean theater_chase_rainbow`: Whether to enable theater chase rainbow effect.

#### MusicDance
- `integer chunk_size`: The number of sample points the program needs to collect from the sound device in order to analyze the sound.
- `integer compute_max_frequency`: The maximum frequency of the sound wave that the app need to consider. See [Usage](#usage) for detail.
- `integer decay_rate`: The decay speed of peak hold indicator. See [Usage](#usage) for detail.
- `integer attack_threshold`: The threshold of increasing maginitude of kick's frequencies to consider a kick transient happens
- `integer kick_max_frequency`: Analyze kick events on the sound frequencies under this value
- `integer color_change_cool_down_period`: The cool down time that color don't change before it elapses
  
#### ColorServer
- `integer listen_port`: The port number to receive UDP packets

## Usage

Basic usage:
```sh
poetry shell
python -m one_leds --config config.json --app ExampleApp
```

If `--config` not specified, it runs with default configuration specified in `config/default.json`.

All apps defined in `one_leds/apps` should be imported in `__main__.py` for users to specify the app to execute. This is done by reflection.

### ExampleApp

This app provides basic dynamic effects. Users need to set at least one of the boolean field under `example_app` to `true`. If multiple fields are set to `true`, then those dynamic effects will appear in turns.

### MusicDance

This app syncs LED strips with the computer's audio output in real-time.

Each LED unit on a strip corresponds to a specific frequency range of the sound. The brightness of the LED unit with the lowest index reflects the magnitude of the lowest frequency calculated via FFT, while the LED with the highest index reflects the magnitude of the `compute_max_frequency` value specified in the config file.

The LED strip supports six colors. When the program detects a drum beat in the audio, the color changes. A drum beat is triggered when the magnitude of any frequency below `kick_max_frequency` in the current audio chunk exceeds the peak hold indicator by more than the `attack_threshold`.

The peak hold indicator works as follows:
- If the magnitude is below the current indicator, the indicator decays by `decay_rate`.  
- If the magnitude exceeds the current indicator, the indicator updates to match the magnitude.

Adjusting `kick_max_frequency`, `attack_threshold`, and `decay_rate` can modify the program's sensitivity to drum detection. Higher sensitivity (with larger `kick_max_frequency`, smaller `attack_threshold`, and larger `decay_rate`) may cause the program to mistake other sound variations for drum beats.

To prevent frequent color changes, a `color_change_cool_down_period` can be set, during which the program ignores drum beats after detecting one.

#### macOS

To capture audio output on macOS, the [BlackHole](https://github.com/ExistentialAudio/BlackHole) driver is required. After installation, create a multi-output device that includes the BlackHole 2ch device. The program captures audio samples from the BlackHole 2ch input.

The frame rate of the LED strip depends on the `chunk_size` and the sample rate of the BlackHole 2ch device. Typically, the frame rate is calculated as:

```math
\text{Frame Rate} = \frac{\text{Sample Rate}}{\text{Chunk Size}}
```

Thus, reducing the `chunk_size` or increasing the sample rate can improve the frame rate.  

However, there is a limitation when reducing `chunk_size` due to macOS's internal sample buffer size of 4096 samples. If the `chunk_size` is set to a fraction of the buffer size, the frame rate will not increase beyond what is achieved with `chunk_size` equal to the buffer size. This is because the operating system delivers 4096 samples to the Python library each time. The library splits these samples into smaller chunks and processes them in rapid succession, but only the last chunk's color will persist on the LED strip for every 4096 samples.

To effectively increase the LED strip's frame rate, increase the sample rate of the BlackHole 2ch device. For example, a `chunk_size` of 8192 with a sample rate of 192 kHz yields approximately 45 FPS.

#### Windows

The availability of a loopback device on the Windows platform depends on the sound card driver. The current implementation supports Realtek sound cards. Contributions to support additional devices are appreciated.

## Contributing  

Contributions are welcome! Please follow these steps:  
1. Fork the repository.  
2. Create a new branch (`git checkout -b feature-name`).  
3. Commit your changes (`git commit -m "Add feature-name"`).  
4. Push the branch (`git push origin feature-name`).  
5. Submit a pull request.  

## Credit
Thanks for Tim's [documentation](https://core-electronics.com.au/guides/fully-addressable-rgb-raspberry-pi/) explaining the basic LED strip installation on Rasepberry PI 4 and providing Tony DiCola's the example code.
The `ExampleApp` under this project is written based on their implementation.

## License  

This project is licensed under the [MIT License](LICENSE).  
