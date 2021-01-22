import time

import pytest

from tinkoff_voicekit_client import user_utils


@pytest.mark.asyncio
async def test_aio_recognize(aio_client_stt, audio_data):
    response, meta = await aio_client_stt.recognize(
        audio_data["source"], audio_data["config"], with_response_meta=True
    )
    print(response)
    print(meta)


@pytest.mark.asyncio
async def test_aio_streaming_recognize(aio_client_stt, audio_data):
    streaming_config = {"config": audio_data["config"]}
    responses = await aio_client_stt.streaming_recognize(
        audio_data["source"], streaming_config
    )
    async for response in responses:
        print(response)


@pytest.mark.asyncio
async def test_aio_long_running_recognize(aio_client_stt, audio_data, aio_client_operations):
    long_running_config = {
        "config": audio_data["config"],
        "group": "group_name"
    }
    response, uri, meta = await aio_client_stt.longrunning_recognize_with_uploader(
        audio_data["source"], long_running_config, with_response_meta=True
    )
    print(response)
    print(uri)
    print(user_utils.get_x_request_id(meta))
    time.sleep(1)
    results = await aio_client_operations.get_operation({"id": response["id"]})
    print(results)


@pytest.mark.asyncio
async def test_aio_synthesis(aio_client_tts, synthesis_config):
    await aio_client_tts.synthesize_to_audio_wav("Привет, как дела!", synthesis_config, "aio_synthesis_speech")
