import os

import pytest

from tinkoff_voicekit_client import ClientSTT, ClientTTS, ClientOperations, aio_voicekit


class ClientParams:
    API_KEY: str = os.getenv("VOICEKIT_API_KEY")
    SECRET_KEY: str = os.getenv("VOICEKIT_SECRET_KEY")


@pytest.fixture
def params():
    if ClientParams.API_KEY is None:
        raise EnvironmentError("API_KEY isn't initialized")
    if ClientParams.SECRET_KEY is None:
        raise EnvironmentError("API_KEY isn't initialized")
    return ClientParams()


@pytest.fixture
def client_stt(params):
    return ClientSTT(params.API_KEY, params.SECRET_KEY)


@pytest.fixture
def client_tts(params):
    return ClientTTS(params.API_KEY, params.SECRET_KEY)


@pytest.fixture
def client_operations(params):
    return ClientOperations(params.API_KEY, params.SECRET_KEY)


@pytest.fixture
def aio_client_stt(params):
    return aio_voicekit.ClientSTT(params.API_KEY, params.SECRET_KEY)


@pytest.fixture
def aio_client_tts(params):
    return aio_voicekit.ClientTTS(params.API_KEY, params.SECRET_KEY)


@pytest.fixture
def aio_client_operations(params):
    return aio_voicekit.ClientOperations(params.API_KEY, params.SECRET_KEY)


@pytest.fixture
def audio_data():
    audio_data = {}
    audio_data["config"] = {
        "encoding": "LINEAR16",
        "sample_rate_hertz": 48000,
        "num_channels": 1,
    }
    audio_data["source"] = "./tests/audio_source/denorm.wav"
    return audio_data


@pytest.fixture
def synthesis_config():
    return {
        "audio_encoding": "RAW_OPUS",
        "sample_rate_hertz": 48000
    }

@pytest.fixture
def audio_with_profanity_lexic():
    audio_data = {}
    audio_data["config"] = {
        "encoding": "LINEAR16",
        "sample_rate_hertz": 48000,
        "num_channels": 1,
        "profanity_filter": True,
    }
    audio_data["source"] = "./tests/audio_source/profanity_lexic.wav"
    return audio_data
