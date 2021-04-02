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
        "vad_config": {"$ref": "#/definitions/VoiceActivityDetectionConfig"},
        "profanity_filter": {"type": "boolean"}
    },
    "required": [
        "sample_rate_hertz",
        "num_channels",
        "encoding",
    ],
    "additionalProperties": False
}

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

long_running_recognition_config_schema = {
    "type": "object",
    "definitions": definitions,
    "properties": {
        "config": recognition_config_schema,
        "group": {"type": "string"}
    },
    "additionalProperties": False
}
