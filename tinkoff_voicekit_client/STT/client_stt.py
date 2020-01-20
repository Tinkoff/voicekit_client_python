from google.protobuf.json_format import MessageToDict
from jsonschema import validate

from tinkoff_voicekit_client.STT.helper_stt import get_proto_request, get_buffer, dict_generator, create_stream_requests
from tinkoff_voicekit_client.speech_utils.BaseClient.base_client import BaseClient
from tinkoff_voicekit_client.speech_utils.apis.stt_pb2_grpc import SpeechToTextStub
from tinkoff_voicekit_client.speech_utils.config_data import client_config
from tinkoff_voicekit_client.speech_utils.metadata import Metadata


class ClientSTT(BaseClient):
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

    def __init__(
            self,
            api_key: str,
            secret_key: str,
            host: str = client_config["host_stt"],
            port: int = client_config["port"],
            ca_file: str = None
    ):
        """
        Create client for speech recognition.
            :param api_key: client public api key
            :param secret_key: client secret api key
            :param host: Tinkoff Voicekit speech recognition host url
            :param port: Tinkoff Voicekit speech recognition port, default value: 443
            :param ca_file: optional certificate file
        """
        super().__init__()
        self._metadata = Metadata(api_key, secret_key, aud="STT")
        self._api_key = api_key
        self._secret_key = secret_key
        self._channel = self._make_channel(host, port, ca_file)
        self._stub = SpeechToTextStub(self._channel)

    def recognize(self, source, config):
        """
        Recognize whole audio and then return all responses.
            :param source: path to audio file or buffer with audio
            :param config: dict conforming to recognition_config_schema
        """
        validate(config, ClientSTT.recognition_config_schema)
        buffer = get_buffer(source)

        if not self._metadata.is_fresh_jwt():
            self._metadata.refresh_jwt()

        response = self._stub.Recognize(
            get_proto_request(buffer, config),
            metadata=self._metadata.metadata
        )

        return MessageToDict(
            response,
            including_default_value_fields=True,
            preserving_proto_field_name=True
        )["results"]

    def streaming_recognize(self, source, config):
        """
        Recognize audio in streaming mode.
        Stream audio chunks to server and get streaming responses.
            :param source: path to audio file or audio stream
            :param config: dict conforming to streaming_recognition_config_schema
        """
        validate(config, ClientSTT.streaming_recognition_config_schema)
        buffer = get_buffer(source)

        if not self._metadata.is_fresh_jwt():
            self._metadata.refresh_jwt()

        responses = self._stub.StreamingRecognize(
            create_stream_requests(buffer, config),
            metadata=self._metadata.metadata
        )

        return dict_generator(responses)

