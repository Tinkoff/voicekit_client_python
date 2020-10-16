from jsonschema import validate

from tinkoff_voicekit_client.STT.helper_stt import (
    get_proto_request,
    get_proto_longrunning_request,
    create_stream_requests
)
from tinkoff_voicekit_client.speech_utils.BaseClient.base_client import BaseClient
from tinkoff_voicekit_client.speech_utils.apis.tinkoff.cloud.stt.v1.stt_pb2_grpc import SpeechToTextStub
from tinkoff_voicekit_client.speech_utils.config_data import client_config
from tinkoff_voicekit_client.speech_utils.core import get_buffer, dict_generator, response_format
from tinkoff_voicekit_client.speech_utils.metadata import Metadata
from tinkoff_voicekit_client.uploader import Uploader


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

    def __init__(
            self,
            api_key: str,
            secret_key: str,
            host: str = client_config["host_stt"],
            port: int = client_config["port"],
            ssl_channel: bool = True,
            ca_file: str = None,
            uploader_config: dict = None
    ):
        """
        Create client for speech recognition.
            :param api_key: client public api key
            :param secret_key: client secret api key
            :param host: Tinkoff Voicekit speech recognition host url
            :param port: Tinkoff Voicekit speech recognition port, default value: 443
            :param ca_file: optional certificate file
            :uploader_config: config for Uploader
        """
        super().__init__(host, port, ssl_channel, ca_file)
        self._metadata = Metadata(api_key, secret_key, aud="tinkoff.cloud.stt")
        self._api_key = api_key
        self._secret_key = secret_key
        self._stub = SpeechToTextStub(self._channel)

        uploader_config = {} if uploader_config is None else uploader_config
        self._uploader = Uploader(self._api_key, self._secret_key, **uploader_config)

    def recognize(self, source, config, metadata=None, dict_format=True):
        """
        Recognize whole audio and then return all responses.
            :param source: path to audio file or buffer with audio
            :param config: dict conforming to recognition_config_schema
            :param dict_format: dict response instead of proto object
            :param metadata: configure own metadata
        """
        validate(config, ClientSTT.recognition_config_schema)
        buffer = get_buffer(source)

        response = self._stub.Recognize(
            get_proto_request(buffer, config),
            metadata=metadata if metadata else self._metadata.metadata
        )
        return response_format(response, dict_format)

    def streaming_recognize(self, source, config, dict_format=True, metadata=None):
        """
        Recognize audio in streaming mode.
        Stream audio chunks to server and get streaming responses.
            :param source: path to audio file or audio stream
            :param config: dict conforming to streaming_recognition_config_schema
            :param dict_format: dict response instead of proto object
            :param metadata: configure own metadata
        """
        validate(config, ClientSTT.streaming_recognition_config_schema)
        buffer = get_buffer(source)

        responses = self._stub.StreamingRecognize(
            create_stream_requests(buffer, config),
            metadata=metadata if metadata else self._metadata.metadata
        )
        return dict_generator(responses, dict_format)

    def longrunning_recognize(self, source, config, dict_format=True, metadata=None):
        """
        Recognize audio in long running mode.
            :param source: uri or buffer source
            :param config: dict conforming to long_running_recognition_schema
            :param dict_format: dict response instead of proto object
            :param metadata: configure own metadata
        """
        validate(config, ClientSTT.long_running_recognition_config_schema)
        if self._uploader.is_storage_uri(source):
            buffer = source
        else:
            buffer = get_buffer(source)

        response = self._stub.LongRunningRecognize(
            get_proto_longrunning_request(buffer, config),
            metadata=metadata if metadata else self._metadata.metadata
        )
        return response_format(response, dict_format)

    def longrunning_recognize_with_uploader(
            self,
            source,
            config: dict,
            object_name: str = None,
            dict_format=True, metadata=None
    ):
        """
        Recognize audio in long running mode.
            :param source: path to audio or fileobj
            :param config: dict conforming to long_running_recognition_schema
            :param object_name: name for object in storage (default: 'default_name_<utcnow>')
            :param dict_format: dict response instead of proto object
            :param metadata: configure own metadata
        """
        validate(config, ClientSTT.long_running_recognition_config_schema)
        uri = self._uploader.upload(source, object_name)

        response = self._stub.LongRunningRecognize(
            get_proto_longrunning_request(uri, config),
            metadata=metadata if metadata else self._metadata.metadata
        )
        return response_format(response, dict_format), uri
