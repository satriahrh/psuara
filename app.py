from application.repository.audio_converter import Ffmpeg
from application.repository.mysql import MysqlConnector
from application.repository.storage import FileStorage
from application.service.audio_user_phrase_retrieve import AudioUserPhraseRetrieve, AudioUserPhraseRetrieveParams
from application.service.audio_user_phrase_upload import AudioUserPhraseUpload, AudioUserPhraseUploadParams
from flask import Flask, json, make_response, request, jsonify
import os

ffmpeg = Ffmpeg(
  'temp',
)
file_storage = FileStorage(
  'storage',
)
mysql_connector = MysqlConnector(
  os.getenv('MYSQL_HOST', 'localhost'),
  os.getenv('MYSQL_USER', 'root'),
  os.getenv('MYSQL_PASSWORD', 'rootpw'),
  os.getenv('MYSQL_DATABASE', 'psuara'),
  os.getenv('MYSQL_PORT', '3306')
)

audio_user_phrase_retrieve = AudioUserPhraseRetrieve(file_storage, ffmpeg, mysql_connector)
audio_user_phrase_upload = AudioUserPhraseUpload(file_storage, ffmpeg, mysql_connector)

app = Flask(__name__)

@app.errorhandler(Exception)
def handle_error(e):
  response = e.get_response()
  response.data = json.dumps({
    "code": e.code,
    "name": e.name,
    "description": e.description,
  })
  response.content_type = "application/json"
  return response

@app.route("/audio/user/<int:user_id>/phrase/<int:phrase_id>", methods=['POST'])
def handler_audio_user_phrase_upload(user_id, phrase_id):
  result = audio_user_phrase_upload.process(AudioUserPhraseUploadParams(
    user_id= user_id,
    phrase_id= phrase_id,
    file= request.files['audio_file'],
  ))

  return jsonify(result)

@app.route("/audio/user/<int:user_id>/phrase/<int:phrase_id>/<string:audio_format>", methods=['GET'])
def handler_audio_user_phrase_retrieve(user_id, phrase_id, audio_format):
  result = audio_user_phrase_retrieve.process(AudioUserPhraseRetrieveParams(
    user_id=user_id,
    phrase_id=phrase_id,
    audio_format=audio_format
  ))

  response = make_response(result['data'])
  response.headers.set('Content-Type', result['mimetype'])
  response.headers.set(
    'Content-Disposition', 'attachment',
    filename=result['name'],
  )

  return response
