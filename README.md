# LEDs Server  

A cross-platform application for controlling LED light strips with versatile configurations and features.  

## Table of Contents  

1. [About](#about)  
2. [Features](#features)  
3. [Installation](#installation)  
   - [Hardware Configurations](#hardware-configurations)  
4. [Usage](#usage)  
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

## Usage

```sh
poetry shell
python -m led_server --config config.json --app MusicDance
```

If `--config` not specified, it runs with default configuration specified in `config/default.json`.

All apps defined in `led_server/apps` should be imported in `__main__.py` for users to specify the app. This is done by reflection.

## Contributing  

Contributions are welcome! Please follow these steps:  
1. Fork the repository.  
2. Create a new branch (`git checkout -b feature-name`).  
3. Commit your changes (`git commit -m "Add feature-name"`).  
4. Push the branch (`git push origin feature-name`).  
5. Submit a pull request.  

## License  

This project is licensed under the [MIT License](LICENSE).  
