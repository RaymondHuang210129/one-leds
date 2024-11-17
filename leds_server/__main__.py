import argparse
from leds_server.submodule.config import parse_config, ControlInstanceConfig
from leds_server.submodule.control_instance import ControlInstance
from leds_server.apps.example_app import ExampleApp
from typing import List
import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "default.json")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=DEFAULT_CONFIG_PATH, help="Path to config file")
    parser.add_argument('--app', type=str, required=True, help="App name to execute")
    args = parser.parse_args()

    print("path: ", args.config)

    with open(args.config, 'r') as file:
        configs: List[ControlInstanceConfig] = parse_config(json.load(file))

    instances = [ControlInstance(config) for config in configs]
    for instance in instances:
        instance.initialize()

    if args.app in globals() and isinstance(globals()[args.app], type):
        app = globals()[args.app](instances)
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
