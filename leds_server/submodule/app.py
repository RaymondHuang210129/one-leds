from .control_instance import ControlInstance
from typing import List

class App:
    def __init__(self, instances: List[ControlInstance]):
        self._instances = instances

    def begin(self) -> None:
        raise NotImplementedError()
    
    def get_info(self) -> str:
        raise NotImplementedError()
