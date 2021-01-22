definitions = {
    "AudioEncoding": {
        "type": "string",
        "enum": ["LINEAR16", "RAW_OPUS"]
    },
    "SynthesisInput": {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "ssml": {"type": "string"}
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

streaming_synthesize_config_schema = {
    "type": "object",
    "definitions": definitions,
    "properties": {
        "audio_encoding": {"$ref": "#/definitions/AudioEncoding"},
        "speaking_rate": {"type": "number"},
        "sample_rate_hertz": {"type": "number"},
        "voice": {"$ref": "#/definitions/Voice"}
    },
    "required": [
        "audio_encoding",
        "sample_rate_hertz"
    ],
    "additionalProperties": False
}
