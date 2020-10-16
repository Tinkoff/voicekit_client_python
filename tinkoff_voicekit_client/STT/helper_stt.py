import json
import struct

from google.protobuf import json_format

from tinkoff_voicekit_client.speech_utils.apis.tinkoff.cloud.stt.v1 import stt_pb2
from tinkoff_voicekit_client.speech_utils.config_data import MAX_LENGTH, CHUNK_SIZE


def get_proto_request(buffer, config: dict):
    buffer = buffer.read()
    if len(buffer) > MAX_LENGTH:
        raise ValueError(f"Max length of file greater than max: {MAX_LENGTH}")

    grpc_config = json_format.Parse(json.dumps(config), stt_pb2.RecognitionConfig())
    grpc_request = stt_pb2.RecognizeRequest()
    grpc_request.config.CopyFrom(grpc_config)
    grpc_request.audio.content = buffer
    return grpc_request


def get_proto_longrunning_request(source, longrunning_config: dict):
    buffer = None
    if not isinstance(source, str):
        buffer = source.read()
        if len(buffer) > MAX_LENGTH:
            raise ValueError(f"Max length of file greater than max: {MAX_LENGTH}")

    grpc_config = json_format.Parse(json.dumps(longrunning_config["config"]), stt_pb2.RecognitionConfig())
    grpc_request = stt_pb2.LongRunningRecognizeRequest()
    grpc_request.config.CopyFrom(grpc_config)
    grpc_request.group = longrunning_config.get("group", "")
    if buffer:
        grpc_request.audio.content = buffer
    else:
        grpc_request.audio.uri = source
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
