# Tinkoff Python Speech API examples

### Usage
#### Install from [PyPi](https://pypi.org/project/tinkoff-voicekit-client/)
```bash
pip install tinkoff-voicekit-client
```


#### Common
Before using you must have *API_KEY* and *SECRET_KEY*. You can get the keys by leaving a request on our [website](https://voicekit.tinkoff.ru/).

Examples of using [VoiceKit](https://voicekit.tinkoff.ru/) client:
* [Recognition examples](#####-Example-of-using-STT)
* [Synthesize examples](#####-Example-of-using-TTS)

Call documentation for public methods
```python
client.something_method.__doc__
```
Methods initialize using config (Python dict) which satisfies one of the next json schema.

#### Recogniton (STT)
Base types schema:
```Python
types_value_definitions = {
        "StringArray": {
            "type": "array",
            "items": {
                "type": "string",
            }
        },
        "AudioEncoding": {
            "type": "string",
            "enum": ["LINEAR16", "ALAW", "MULAW", "LINEAR32F", "RAW_OPUS", "MPEG_AUDIO"]
        },
        "VoiceActivityDetectionConfig": {
            "type": "object",
            "properties": {
                "min_speech_duration": {"type": "number"},
                "max_speech_duration": {"type": "number"},
                "silence_duration_threshold": {"type": "number"},
                "silence_prob_threshold": {"type": "number"},
                "aggressiveness": {"type": "number"},
            }
        },
        "SpeechContext": {
            "type": "object",
            "properties": {
                "phrases": {"$ref": "#definitions/StringArray"},
                "words": {"$ref": "#definitions/StringArray"}
            }
        },
        "InterimResultsConfig": {
            "type": "object",
            "properties": {
                "enable_interim_results": {"type": "boolean"},
                "interval": {"type": "number"}
            }
        }
    }
```

Recognition config schema:
```Python
recognition_config_schema = {
        "type": "object",
        "definitions": definitions,
        "properties": {
            "encoding": {"$ref": "#/definitions/AudioEncoding"},
            "sample_rate_hertz": {"type": "number"},
            "language_code": {"type": "string"},
            "max_alternatives": {"type": "number"},
            "speech_contexts": {
                "type": "array",
                "items": {
                    "$ref": "#/definitions/SpeechContext"
                }
            },
            "enable_automatic_punctuation": {"type": "boolean"},
            "model": {"type": "string"},
            "num_channels": {"type": "number"},
            "do_not_perform_vad": {"type": "boolean"},
            "vad_config": {"$ref": "#/definitions/VoiceActivityDetectionConfig"}
        },
        "required": [
            "sample_rate_hertz",
            "num_channels",
            "encoding",
        ],
        "additionalProperties": False
    }
```

Streaming recognition config schema:
```Python
streaming_recognition_config_schema = {
        "type": "object",
        "definitions": definitions,
        "properties": {
            "config": recognition_config_schema,
            "single_utterance": {"type": "boolean"},
            "interim_results_config": {"$ref": "#/definitions/InterimResultsConfig"}
        },
        "additionalProperties": False
    }
```

##### Example of using STT
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
Example of Voice Activity Detection configuration
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
Base types schema:
```Python
types_value_definitions = {
        "AudioEncoding": {
            "type": "string",
            "enum": ["LINEAR16", "ALAW", "MULAW", "LINEAR32F", "RAW_OPUS"]
        },
        "SynthesisInput": {
            "type": "object",
            "properties": {
                "text": {"type": "string"}
            }
        }
    }
```

Streaming synthesis schema:
```Python
streaming_synthesize_config_schema = {
        "type": "object",
        "definitions": definitions,
        "properties": {
            "audio_encoding": {"$ref": "#/definitions/AudioEncoding"},
            "speaking_rate": {"type": "number"},
            "sample_rate_hertz": {"type": "number"}
        },
        "required": [
            "sample_rate_hertz",
            "audio_encoding",
        ],
        "additionalProperties": False
    }
```

Example of input file:
```
Я жду вашего ответа. Вы готовы сделать перевод?
# Давайте уточним получателя. Как его зовут?
```
commented lines # will not be synthesis

##### Example of using TTS
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
```
