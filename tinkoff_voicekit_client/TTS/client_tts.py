import os

from jsonschema import validate

from tinkoff_voicekit_client.TTS.configurator_codec import configuration
from tinkoff_voicekit_client.TTS.helper_tts import get_utterance_generator, get_config, get_encoder, save_synthesize_wav
from tinkoff_voicekit_client.speech_utils.BaseClient.base_client import BaseClient
from tinkoff_voicekit_client.speech_utils.apis.tts_pb2 import SynthesizeSpeechRequest
from tinkoff_voicekit_client.speech_utils.apis.tts_pb2_grpc import TextToSpeechStub
from tinkoff_voicekit_client.speech_utils.config_data import client_config
from tinkoff_voicekit_client.speech_utils.metadata import Metadata


class ClientTTS(BaseClient):
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
        }
    }

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

    def __init__(
            self,
            api_key: str,
            secret_key: str,
            host: str = client_config["host_tts"],
            port: int = client_config["port"],
            ca_file: str = None
    ):
        """
        Create client for speech synthesis.
            :param api_key: client public api key
            :param secret_key: client secret api key
            :param host: Tinkoff Voicekit speech synthesize host url
            :param port: Tinkoff Voicekit speech synthesize port, default value: 443
            :param ca_file: optional certificate file
        """
        super().__init__()
        configuration()
        self._metadata = Metadata(api_key, secret_key, aud="TTS")
        self._channel = self._make_channel(host, port, ca_file)
        self._stub = TextToSpeechStub(self._channel)

    def streaming_synthesize(
            self,
            text_source: str,
            config: dict,
            text_encoding: str = "utf-8",
            ssml: bool = False
    ):
        """
        Description:
        return generator by StreamingSynthesizeSpeechResponses from each text line in file or text string.
            :param text_source: path to file with text or string with text
            :param config: dict conforming to streaming_synthesize_config_schema
            :param text_encoding: text encoding
            :param ssml: enable ssml text source
        """
        validate(config, ClientTTS.streaming_synthesize_config_schema)

        generate_utterances = get_utterance_generator(text_source)

        request = SynthesizeSpeechRequest()
        request.audio_config.CopyFrom(get_config(config))

        for text in generate_utterances(text_source, text_encoding):
            if not self._metadata.is_fresh_jwt():
                self._metadata.refresh_jwt()

            if ssml:
                request.input.ssml = text
            else:
                request.input.text = text
            yield self._stub.StreamingSynthesize(request, metadata=self._metadata.metadata)

    def synthesize_to_audio_wav(
            self,
            text_source: str,
            config: dict,
            output_dir: str = os.curdir,
            text_encoding: str = "utf-8",
            ssml: bool = False
    ):
        """
        Description:
        Generate audio for each text line from your text source and save it in wav format.
            :param text_source: path to file with text or string with text
            :param config: dict conforming to streaming_synthesize_config_schema
            :param output_dir: path to output directory where to store synthesized audio
            :param text_encoding: text encoding
            :param ssml: enable ssml text source
        """
        rows_responses = self.streaming_synthesize(text_source, config, text_encoding, ssml)
        os.makedirs(output_dir, exist_ok=True)

        for index, row_response in enumerate(rows_responses):
            audio_chunks = []
            get_chunk = get_encoder(config["audio_encoding"], config["sample_rate_hertz"])
            for response in row_response:
                audio_chunks += get_chunk(response.audio_chunk)

            save_synthesize_wav(bytes(audio_chunks),
                                os.path.join(output_dir, f"{index}.wav"),
                                config["sample_rate_hertz"])
