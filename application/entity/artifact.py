from typing import TypedDict, overload
import attr

@attr.s(auto_attribs=True)
class Artifact:
  id: int
  name: str
  mimetype: str
  user_id: int
  phrase_id: int
  data: bytes
