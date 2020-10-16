#### Recogniton (STT)
Base types schema:
```Python
definitions = {
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

* Recognition config schema:
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
        "enable_denormalization": {"type": "boolean"},
        "enable_rescoring": {"type": "boolean"},
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

* Streaming recognition config schema:
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

* Long running recognition config schema
```python
long_running_recognition_config_schema = {
    "type": "object",
    "definitions": definitions,
    "properties": {
        "config": recognition_config_schema,
        "group": {"type": "string"}
    },
    "additionalProperties": False
}

```

#### Synthesize (TTS)
Base types schema:
```Python
definitions = {
    "AudioEncoding": {
        "type": "string",
        "enum": ["LINEAR16", "RAW_OPUS"]
    },
    "SynthesisInput": {
        "type": "object",
        "properties": {
            "text": {"type": "string"}
        }
    },
    "Voice": {
        "type": "object",
        "properties": {
            "language_code": {"type": "string"},
            "name": {
                "type": "string",
                "enum": ["alyona", "oleg", "maxim", "flirt"]
            },
            "ssml_gender": {
                "type": "string",
                "enum": ["SSML_VOICE_GENDER_UNSPECIFIED", "MALE", "FEMALE", "NEUTRAL"]
            }
        }
    }
}
```

* Streaming synthesis config schema:
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

#### Operation
Base types schema:
```python
definitions = {
    "OperationStateFilter": {
        "type": "string",
        "enum": ["ENQUEUED", "PROCESSING", "DONE", "FAILED"]
    },
    "ServiceIDFilter": {
        "oneOf": [
            {"exact_service_id": {"type": "string"}},
            {"any_service_id": {"type": "object"}}
        ]
    },
    "IDFilter": {
        "oneOf": [
            {"exact_id": {"type": "string"}},
            {"any_id": {"type": "object"}}
        ]
    },
    "GroupFilter": {
        "oneOf": [
            {"exact_group": {"type": "string"}},
            {"any_group": {"type": "object"}}
        ]
    }
}

operation_filter_schema = {
    "type": "object",
    "definitions": definitions,
    "properties": {
        "service_id": {"$ref": "#/definitions/ServiceIDFilter"},
        "id": {"$ref": "#/definitions/IDFilter"},
        "group": {"$ref": "#/definitions/GroupFilter"},
        "state": {
            "type": "array",
            "items": {"$ref": "#/definitions/OperationStateFilter"}
        },
    }
}
```

* List operations config schema:
```python
list_operations_config_schema = {
    "type": "object",
    "operation_filter": operation_filter_schema,
    "properties": {
        "filter": {"$ref": "#/operation_filter"},
        "page_size": {"type": "number"},
        "page_token": {"type": "string"}
    }
}
```

* Get operation config schema
```python
get_operation_config_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"}
    }
}
```

* Wait operation config schema
```python
wait_operation_config_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "timeout": {"type": "string"}
    }
}
```

* Watch operation config schema
```python
watch_operation_config_schema = {
    "type": "object",
    "operation_filter": operation_filter_schema,
    "properties": {
        "filter": {"$ref": "#/operation_filter_schema"},
        "listen_for_updates": {"type": "boolean"}
    }
}
```