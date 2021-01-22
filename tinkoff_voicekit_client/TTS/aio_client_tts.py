import os

from jsonschema import validate

from tinkoff_voicekit_client.TTS.configurator_codec import configuration
from tinkoff_voicekit_client.TTS import config_schema
from tinkoff_voicekit_client.TTS.helper_tts import (
    get_utterance_generator,
    get_proto_synthesize_request,
    get_encoder, save_synthesize_wav
)
from tinkoff_voicekit_client.speech_utils.BaseClient import aio_client
from tinkoff_voicekit_client.speech_utils.apis.tinkoff.cloud.tts.v1.tts_pb2_grpc import TextToSpeechStub
from tinkoff_voicekit_client.speech_utils.config_data import client_config, aud
from tinkoff_voicekit_client.speech_utils.metadata import Metadata


class ClientTTS(aio_client.BaseClient):
    def __init__(
            self,
            api_key: str,
            secret_key: str,
            host: str = client_config["host_tts"],
            port: int = client_config["port"],
            ssl_channel: bool = True,
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
        super().__init__(host, port, ssl_channel, ca_file)
        configuration()
        self._metadata = Metadata(api_key, secret_key, aud=aud["tts"])
        self._stub = TextToSpeechStub(self._channel)

    async def streaming_synthesize(
            self,
            text_source: str,
            config: dict,
            ssml: bool = False,
            text_encoding: str = "utf-8",
            with_response_meta=False,
            metadata=None
    ):
        """
        Description:
        return generator by StreamingSynthesizeSpeechResponses from each text line in file or text string.
            :param text_source: path to file with text or string with text
            :param config: dict conforming to streaming_synthesize_config_schema
            :param ssml: enable ssml
            :param text_encoding: text encoding
            :param with_response_meta: return response with metadata
            :param metadata: configure own metadata
        """
        validate(config, config_schema.streaming_synthesize_config_schema)
        request = get_proto_synthesize_request(config)

        utterances = get_utterance_generator(text_source, text_encoding, ssml)
        for synthesis_input in utterances:
            request.input.CopyFrom(synthesis_input)
            response = self._stub.StreamingSynthesize(
                request, metadata=metadata if metadata else self._metadata.metadata
            )
            if with_response_meta:
                yield response, await response.initial_metadata()
            else:
                yield response

    async def synthesize_to_audio_wav(
            self,
            text_source: str,
            config: dict,
            file_name: str,
            ssml: bool = False,
            output_dir: str = os.curdir,
            text_encoding: str = "utf-8",
            with_response_meta=False,
            metadata=None
    ):
        """
        Description:
        Generate audio for each text line from your text source and save it in wav format.
            :param text_source: path to file with text or string with text
            :param config: dict conforming to streaming_synthesize_config_schema
            :param file_name: name of synthesis audio file
            :param ssml: enable ssml
            :param output_dir: path to output directory where to store synthesized audio
            :param text_encoding: text encoding
            :param with_response_meta: return metadata of last row
            :param metadata: configure own metadata
        """
        rows_responses = self.streaming_synthesize(text_source, config, ssml, text_encoding, metadata)
        get_chunk = get_encoder(config["audio_encoding"], config["sample_rate_hertz"])
        os.makedirs(output_dir, exist_ok=True)

        response_meta = None
        index = 0
        async for row_response in rows_responses:
            response_meta = await row_response.initial_metadata()

            audio_chunks = []
            async for response in row_response:
                audio_chunks += get_chunk(response.audio_chunk)

            save_synthesize_wav(bytes(audio_chunks),
                                os.path.join(output_dir, f"{file_name}_{index}.wav"),
                                config["sample_rate_hertz"])
            index += 1

        return response_meta if with_response_meta else None
