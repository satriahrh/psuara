from abc import ABC, abstractmethod
from typing import Any

class Service(ABC):
  @abstractmethod
  def process(self, params) -> dict[str, Any]:
    pass
