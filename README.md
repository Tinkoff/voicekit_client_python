# Tinkoff Python [VoiceKit](https://voicekit.tinkoff.ru/) API Library
[![Downloads](https://pepy.tech/badge/tinkoff-voicekit-client)](https://pepy.tech/project/tinkoff-voicekit-client)
[![Maintainability](https://api.codeclimate.com/v1/badges/263d75fe1c9d4f2bfd1a/maintainability)](https://codeclimate.com/github/TinkoffCreditSystems/voicekit_client_python/maintainability)

### Usage
#### Install from [PyPi](https://pypi.org/project/tinkoff-voicekit-client/)
```bash
pip install tinkoff-voicekit-client
```


#### Common
Before using you must have *API_KEY* and *SECRET_KEY*. You can get the keys by leaving a request on our [website](https://voicekit.tinkoff.ru/).

[Documentation](https://voicekit.tinkoff.ru/docs/)

[Type schema](docs/SCHEMA.md)

Examples of using [VoiceKit](https://voicekit.tinkoff.ru/) client:
* [Recognition examples](#example-of-using-stt)
* [Synthesize examples](#synthesize-tts)
* [Operation examples](#example-of-using-operations)
* [Uploader examples](#example-of-using-uploader)

Call documentation for public methods
```python
from tinkoff_voicekit_client import ClientSTT

API_KEY = "my_api_key"
SECRET_KEY = "my_secret_key"

client = ClientSTT(API_KEY, SECRET_KEY)

client.something_method.__doc__
```
Methods initialize using config (Python dict) which satisfies one of the next json schema.

#### Recogniton (STT)
##### Example of using STT
* recognize
```python
from tinkoff_voicekit_client import ClientSTT

API_KEY = "my_api_key"
SECRET_KEY = "my_secret_key"

client = ClientSTT(API_KEY, SECRET_KEY)

audio_config = {
    "encoding": "LINEAR16",
    "sample_rate_hertz": 8000,
    "num_channels": 1
}

# recognise method call
response = client.recognize("path/to/audio/file", audio_config)
print(response)
```
* streaming recognize
```python
from tinkoff_voicekit_client import ClientSTT

API_KEY = "my_api_key"
SECRET_KEY = "my_secret_key"

client = ClientSTT(API_KEY, SECRET_KEY)

audio_config = {
    "encoding": "LINEAR16",
    "sample_rate_hertz": 8000,
    "num_channels": 1
}
stream_config = {"config": audio_config}

# recognise stream method call
with open("path/to/audio/file", "rb") as source:
    responses = client.streaming_recognize(source, stream_config)
    for response in responses:
        print(response)
```
* long running recognize with uploader
```python
from tinkoff_voicekit_client import ClientSTT

API_KEY = "my_api_key"
SECRET_KEY = "my_secret_key"

client = ClientSTT(API_KEY, SECRET_KEY)

audio_config = {
    "encoding": "LINEAR16",
    "sample_rate_hertz": 8000,
    "num_channels": 1
}

request = {
    "config": audio_config,
    "group": "group_name"
}

file_path = "path/to/file"
audio_name_for_storage = "pretty name"

# this method automatically upload audio to long running storage and return uri
print(client.longrunning_recognize_with_uploader(file_path, request, audio_name_for_storage))
```
Example of [Voice Activity Detection](https://voicekit.tinkoff.ru/docs/stttutorial#example-customized-vad) configuration
```Python
vad = {}
vad["min_speech_duration"] = min_speech_duration
vad["max_speech_duration"] = max_speech_duration
vad["silence_duration_threshold"] = silence_duration_threshold
vad["silence_prob_threshold"] = silence_prob_threshold
vad["aggressiveness"] = aggressiveness

my_config = {}
my_config["vad"] = vad
```

#### Synthesize (TTS)
Example of input file:
```
Я жду вашего ответа. Вы готовы сделать перевод?
# Давайте уточним получателя. Как его зовут?
```
commented lines # will not be synthesis

##### Example of using TTS
* default
```python
from tinkoff_voicekit_client import ClientTTS

API_KEY = "api_key"
SECRET_KEY = "secret_key"

client = ClientTTS(API_KEY, SECRET_KEY)
audio_config = {
    "audio_encoding": "LINEAR16",
    "sample_rate_hertz": 48000
}


# use it if you want work with proto results
# audio file
rows_responses = client.streaming_synthesize("path/to/file/with/text", audio_config)
# text
rows_responses = client.streaming_synthesize("Мой красивый текст", audio_config)

# use it if you want get audio file results
# audio file
client.synthesize_to_audio_wav("path/to/file/with/text", audio_config, "output/dir")
# text
client.synthesize_to_audio_wav("Мой красивый текст", audio_config, "output/dir")
# ssml. There are only tag <speak>
client.synthesize_to_audio_wav("<speak>Мой красивый текст</speak>", audio_config, "output/dir", ssml=True)
```
* change voice
```python
from tinkoff_voicekit_client import ClientTTS

API_KEY = "api_key"
SECRET_KEY = "secret_key"

client = ClientTTS(API_KEY, SECRET_KEY)
config = {
        "audio_encoding": "RAW_OPUS",
        "sample_rate_hertz": 48000,
        "voice": {"name": "alyona"}
    }
client.synthesize_to_audio_wav("Приве! Меня зовут Алена.", config)
```

#### Example of using Operations
* get operation by id
```python
from tinkoff_voicekit_client import ClientOperations
API_KEY = "my_api_key"
SECRET_KEY = "my_secret_key"

operations = ClientOperations(API_KEY, SECRET_KEY)

running_operation_id = "42"

print(operations.get_operation({"id": running_operation_id}))
```
* cancel operation by id
```python
from tinkoff_voicekit_client import ClientOperations
API_KEY = "my_api_key"
SECRET_KEY = "my_secret_key"

operations = ClientOperations(API_KEY, SECRET_KEY)
operation_filter = {"exact_id": "31"}

# return empty dict on success
print(operations.cancel_operation(operation_filter))
```

#### Example of using Uploader
```python
from tinkoff_voicekit_client import Uploader
API_KEY = "my_api_key"
SECRET_KEY = "my_secret_key"

uploader = Uploader(API_KEY, SECRET_KEY)
path = "path/to/file"

print(uploader.upload(path, "object_name"))
```