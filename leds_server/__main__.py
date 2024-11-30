import argparse
from leds_server.common.config import *
from leds_server.common.control_instance import ControlInstance
from leds_server.apps.example_app.example_app import ExampleApp
from leds_server.apps.color_server.color_server import ColorServer
from leds_server.apps.music_dance.music_dance import MusicDance
from leds_server.control_instances.control_instance_direct import ControlInstanceDirect
from leds_server.control_instances.control_instance_remote import ControlInstanceRemote
from typing import List, Union
import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "default.json")


def create_control_instance(config: ControlInstanceConfig) -> Union[ControlInstanceDirect,
                                                                    ControlInstanceRemote]:
    if isinstance(config.implementation, DirectAccess):
        return ControlInstanceDirect(config)
    elif isinstance(config.implementation, RemoteAccess):
        return ControlInstanceRemote(config)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config', default=DEFAULT_CONFIG_PATH, help="Path to config file")
    parser.add_argument('--app', type=str, required=True,
                        help="App name to execute")
    args = parser.parse_args()

    print("path: ", args.config)

    with open(args.config, 'r') as file:
        instances_config, app_config = parse_config(
            json.load(file))

    instances = [create_control_instance(
        instance_config) for instance_config in instances_config]
    for instance in instances:
        instance.initialize()

    if args.app in globals() and isinstance(globals()[args.app], type):
        app = globals()[args.app](instances, app_config)
        print("Launching app: ", app.get_info())
        try:
            app.begin()
        except KeyboardInterrupt:
            for instance in instances:
                instance.initialize()
    else:
        raise RuntimeError(f"Error: '{args.app}' is not a valid class.")


if __name__ == '__main__':
    main()
