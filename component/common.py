from abc import ABC, abstractmethod

class P(ABC):
    def __init__(self, sub_process_type: str, **kwargs):
        self.sub_process_type = sub_process_type
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def generate_gcode(self) -> str:
        pass
