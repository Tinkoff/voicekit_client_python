import io
import os

from aiofiles import open
from google.protobuf.json_format import MessageToDict


async def get_buffer(source):
    if type(source) is str and os.path.isfile(source):
        async with open(source, "rb") as f:
            buffer = await f.read()
        return io.BytesIO(buffer)
    elif isinstance(source, io.BufferedReader):
        return source
    elif isinstance(source, io.BytesIO):
        return source
    else:
        raise ValueError("Incorrect source parameters: must be path to file or io.BufferedReader")


def response_format(response, dict_format):
    if dict_format:
        return MessageToDict(
            response,
            including_default_value_fields=True,
            preserving_proto_field_name=True
        )
    return response


async def dict_generator(responses, dict_format):
    if dict_format:
        async for response in responses:
            yield MessageToDict(
                response,
                including_default_value_fields=True,
                preserving_proto_field_name=True
            )
    else:
        async for response in responses:
            yield response
