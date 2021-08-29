from application.repository import Storage
from os import path, remove

class FileStorage(Storage):
  def __init__(self, basedir: str):
    self.basedir = basedir

  def store(self, name: str, data: bytes) -> None:
    filepath = path.join(self.basedir, name)
    with open(filepath, 'wb') as file:
      file.write(data)

  def retrieve(self, name: str) -> bytes:
    filepath = path.join(self.basedir, name)
    
    ret = bytes
    with open(filepath, 'rb') as file:
      ret = file.read()
      
    return ret
  
  def remove(self, name: str):
    filepath= path.join(self.basedir, name)
    if path.exists(filepath):
      remove(filepath)