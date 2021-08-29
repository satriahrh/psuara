from application.entity.artifact import Artifact
from werkzeug import exceptions
from application.repository import AudioConverter, Mysql, Storage
from application.service import Service
from werkzeug.datastructures import FileStorage
from pathlib import Path
from time import time
import attr

@attr.s(auto_attribs=True)
class AudioUserPhraseUploadParams:
  user_id: int
  phrase_id: int
  file: FileStorage

class AudioUserPhraseUpload(Service):
  def __init__(self, storage: Storage, audio_converter: AudioConverter, mysql: Mysql):
    super().__init__()
    self.audio_converter = audio_converter
    self.mysql = mysql
    self.storage = storage

  def process(self, params: AudioUserPhraseUploadParams):
    path = Path(params.file.filename)

    if path.suffix == '':
      raise exceptions.UnprocessableEntity('cannot detect audio format')

    dest_format = 'wav'
    if not self.audio_converter.is_available(path.suffix[1:], dest_format):
      raise exceptions.UnprocessableEntity('unable to store the audio file due to unsupported format')
    
    origin_bytes = params.file.read()
    params.file.close

    dest_bytes = self.audio_converter.convert(origin_bytes, path.suffix[1:], dest_format)

    dest_filename = '{}.{}'.format(
      abs(
        hash(
          '{}{}{}'.format(
            time(),
            params.user_id,
            params.phrase_id,
          ),
        ),
      ),
      dest_format,
    )
    self.storage.store(dest_filename, dest_bytes)

    artifact = self.mysql.artifact_create(Artifact(
      None, dest_filename, 'audio/wav', params.user_id, params.phrase_id, None
    ))

    return artifact.__dict__