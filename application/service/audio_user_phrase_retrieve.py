
from application.entity.artifact import Artifact
from application.repository import AudioConverter, Mysql, Storage
from application.service import Service
from werkzeug import exceptions
import attr

@attr.s(auto_attribs=True)
class AudioUserPhraseRetrieveParams:
  user_id: int
  phrase_id: int
  audio_format: str

class AudioUserPhraseRetrieve(Service):
  def __init__(self, storage: Storage, audio_converter: AudioConverter, mysql: Mysql):
    super().__init__()
    self.audio_converter = audio_converter
    self.storage = storage
    self.mysql = mysql

  def process(self, params: AudioUserPhraseRetrieveParams):
    origin_format = 'wav'
    dest_format = params.audio_format
    if not self.audio_converter.is_available(origin_format, dest_format):
      raise exceptions.BadRequest('requested format is not supported for particular audio')

    artifact: Artifact = self.mysql.artifact_get(
      params.user_id, params.phrase_id
    )
    if artifact is None:
      raise exceptions.NotFound('artifact not found for given user id and phrase id')

    artifact.data = self.storage.retrieve(artifact.name)
    
    artifact.data = self.audio_converter.convert(artifact.data, origin_format, dest_format)
    artifact.mimetype = 'audio/m4a'

    return artifact.__dict__