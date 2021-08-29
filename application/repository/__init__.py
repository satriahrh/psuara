from abc import ABC, abstractmethod
from application.entity.artifact import Artifact

class AudioConverter(ABC):
  @abstractmethod
  def convert(self, data: bytes, origin_format: str, destination_format: str, **kwargs) -> bytes:
    pass

  @abstractmethod
  def is_available(self, origin_format: str, destination_format: str) -> bool:
    pass

class Storage(ABC):
  @abstractmethod
  def store(self, name: str, data: bytes) -> None:
    pass

  @abstractmethod
  def retrieve(self, name: str) -> bytes:
    pass


  @abstractmethod
  def remove(self, name: str):
    pass

class Mysql(ABC):
  @abstractmethod
  def artifact_create(self, artifact: Artifact) -> Artifact:
    pass

  @abstractmethod
  def artifact_get(self, user_id: int, phrase_id: int) -> Artifact:
    pass