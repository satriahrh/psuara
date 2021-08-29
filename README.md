# psuara

## Requirements

1. Mysql 5.7
2. Directory `tmp` and `storage`
3. FFMPEG

   `brew install ffmpeg` or `apt-get install ffmpeg libavcodec-extra` 

## Usages

### Audio User Phrase Retrieval

```
curl --request POST 'http://localhost:5000/audio/user/1/phrase/1' --form 'audio_file=@"./test_audio_file_1.m4a"'
```

### Audio User Phrase Uploader

```
curl --request GET 'http://localhost:5000/audio/user/1/phrase/1/m4a' -o './test_response_file_1_1.m4a'
```
