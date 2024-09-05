from abc import ABC, abstractmethod
from typing import Any, Dict


class Serializable(ABC):
    @staticmethod
    @abstractmethod
    def from_dict(data: Dict[str, Any]):
        """Convert a dictionary to an instance of the class."""
        pass
