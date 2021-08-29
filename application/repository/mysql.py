from mysql.connector.cursor_cext import CMySQLCursor
from application.entity.artifact import Artifact
from application.repository import Mysql
from mysql import connector

class MysqlConnector(Mysql):
  def __init__(self, host: str, user: str, password: str, database: str, port: str):
    self.cnx = connector.connect(host=host, user=user, password=password, database=database, port=port)      

  def artifact_create(self, artifact: Artifact) -> Artifact:
    cursor = self.cnx.cursor()
    try:
      cursor.execute(
        """INSERT INTO artifacts
        (name, mimetype, user_id, phrase_id)
        VALUES (%s, %s, %s, %s)""",
        (artifact.name, artifact.mimetype, artifact.user_id, artifact.phrase_id),
      )
      artifact.id = cursor.lastrowid
      self.cnx.commit()
    finally:
      cursor.close()

    return artifact

  def artifact_get(self, user_id: int, phrase_id: int) -> Artifact:
    ret: Artifact
    cursor: CMySQLCursor = self.cnx.cursor()
    try:
      cursor.execute(
        """SELECT id, name, mimetype, user_id, phrase_id
        FROM artifacts
        WHERE user_id = %s AND phrase_id = %s
        ORDER BY id DESC
        LIMIT 1""",
        (user_id, phrase_id),
      )
      row = cursor.fetchone()
      if type(row) == tuple:
        ret = Artifact(
          row[0], row[1], row[2], row[3], row[4], None,
        )
      else:
        ret = None
      
    finally:
      cursor.close()

    return ret
