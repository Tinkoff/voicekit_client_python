import io
import json
import os
import struct

from google.protobuf import json_format
from google.protobuf.json_format import MessageToDict

from tinkoff_voicekit_client.speech_utils.apis import stt_pb2
from tinkoff_voicekit_client.speech_utils.config_data import MAX_LENGTH, CHUNK_SIZE


def get_proto_request(buffer, config):
    buffer = buffer.read()
    if len(buffer) > MAX_LENGTH:
        raise ValueError(f"Max length of file greater than max: {MAX_LENGTH}")

    grpc_config = json_format.Parse(json.dumps(config), stt_pb2.RecognitionConfig())
    grpc_request = stt_pb2.RecognizeRequest()
    grpc_request.config.CopyFrom(grpc_config)
    grpc_request.audio.content = buffer
    return grpc_request


def get_first_stream_config(config: dict):
    grpc_config = json_format.Parse(json.dumps(config), stt_pb2.StreamingRecognitionConfig())
    return grpc_config


def create_stream_requests(buffer, config: dict):
    request = stt_pb2.StreamingRecognizeRequest()
    request.streaming_config.CopyFrom(get_first_stream_config(config))
    yield request

    chunk_size = CHUNK_SIZE
    encoding = config["config"]["encoding"]

    while True:
        if encoding == "RAW_OPUS":
            length_bytes = buffer.read(4)
            if not length_bytes:
                break
            length = struct.unpack(">I", length_bytes)[0]
            data = buffer.read(length)
        else:
            data = buffer.read(chunk_size)
            if not data:
                break
        request.audio_content = data
        yield request


def dict_generator(responses):
    for response in responses:
        yield MessageToDict(
            response,
            including_default_value_fields=True,
            preserving_proto_field_name=True
        )["results"]


def get_buffer(source):
    if type(source) is str and os.path.isfile(source):
        with open(source, "rb") as f:
            buffer = f.read()
        return io.BytesIO(buffer)
    elif isinstance(source, io.BufferedReader):
        return source
    elif isinstance(source, io.BytesIO):
        return source
    else:
        raise ValueError("Incorrect source parameters: must be path to file or io.BufferedReader")