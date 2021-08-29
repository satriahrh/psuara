from application.repository.storage import FileStorage
from application.repository import AudioConverter
from time import time
from os import path
import subprocess

class Ffmpeg(AudioConverter):
  def __init__(self, temp_dir: str='temp') -> None:
      super().__init__()
      self.temp_basedir = temp_dir
      self.file_storage = FileStorage(self.temp_basedir)
      self.convertor = {
        'm4a': {
          'wav': self.__m4a_to_wav
        },
        'wav': {
          'm4a': self.__wav_to_m4a
        }
      }

  def is_available(self, origin_format: str, destination_format: str) -> bool:
    if self.convertor[origin_format] is None:
      return False
    if self.convertor[origin_format][destination_format] is None:
      return False
    return True

  def convert(self, data: bytes, origin_format: str, destination_format: str, **kwargs) -> bytes:
    return self.convertor[origin_format][destination_format](data)

  def __wav_to_m4a(self, data: bytes) -> bytes:
    # https://stackoverflow.com/questions/19774975/unknown-encoder-libfaac

    temp_in_filename, temp_in_filepath = self.__generate_temp_filename_and_filepath('wav')
    temp_out_filename, temp_out_filepath = self.__generate_temp_filename_and_filepath('m4a')

    try:
      self.file_storage.store(temp_in_filename, data)

      subprocess.run(
        ['ffmpeg', '-i', temp_in_filepath, '-c:a', 'aac', temp_out_filepath]
      )

      return self.file_storage.retrieve(temp_out_filename)
    finally:
      self.file_storage.remove(temp_in_filename)
      self.file_storage.remove(temp_out_filename)

  def __m4a_to_wav(self, data: bytes) -> bytes:
    temp_in_filename, temp_in_filepath = self.__generate_temp_filename_and_filepath('m4a')
    temp_out_filename, temp_out_filepath = self.__generate_temp_filename_and_filepath('wav')

    try:  
      self.file_storage.store(temp_in_filename, data)

      subprocess.run(
        ['ffmpeg', '-i', temp_in_filepath, temp_out_filepath]
      )

      return self.file_storage.retrieve(temp_out_filename)
    finally:
      self.file_storage.remove(temp_in_filename)
      self.file_storage.remove(temp_out_filename)

  def __generate_temp_filename_and_filepath(self, extension):
    filename = '{hash}-ffmpeg.{ext}'.format(
      hash=hash(time()),
      ext=extension
    )
    return filename, path.join(self.temp_basedir, filename)
