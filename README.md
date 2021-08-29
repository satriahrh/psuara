# psuara

## Requirements

1. Mysql 5.7
2. Directory `tmp` and `storage`
3. FFMPEG

   `brew install ffmpeg` or `apt-get install ffmpeg libavcodec-extra` 

## Usages

### Audio User Phrase Retrieval

```
curl --request POST 'http://127.0.0.1:5000/audio/user/1/phrase/1' --form 'audio_file=@"./test_audio_file_1.m4a"'
```

### Audio User Phrase Uploader

```
curl --request GET 'http://127.0.0.1:5000/audio/user/1/phrase/1/m4a' -o './test_response_file_1_1.m4a'
```

## How to Run

### Mysql

To run the service, you may have mysql running locally, or somewhere.
Then you need to adjust the mysql config on `.env`.

After that, you need to make database migration using following schema migration.

```
-- psuara.artifacts definition

CREATE TABLE `artifacts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `mimetype` varchar(255) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `phrase_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
```

### Docker Run

Assuming you already build the applicatin, tagged `psuara`.

```
docker build -t psuara .
```

Before running below command, make sure you have directory `storage` and `temp` under current directory.

```
docker run -v $PWD:/app-data --env-file .env -p 127.0.0.1:5000:5000/tcp --network="bridge" psuara
```
