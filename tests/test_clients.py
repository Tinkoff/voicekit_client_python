import time

from tinkoff_voicekit_client import user_utils


def test_recognize(client_stt, audio_data):
    response, meta = client_stt.recognize(
        audio_data["source"], audio_data["config"], with_response_meta=True
    )
    print(response)
    print(user_utils.get_x_request_id(meta))


def test_streaming_recognize(client_stt, audio_data):
    streaming_config = {"config": audio_data["config"]}
    responses = client_stt.streaming_recognize(
        audio_data["source"], streaming_config
    )
    for response in responses:
        print(response)


def test_profanity_filter(client_stt, audio_with_profanity_lexic):
    response, meta = client_stt.recognize(
        audio_with_profanity_lexic["source"],
        audio_with_profanity_lexic["config"],
        with_response_meta=True,
    )
    print(response)


def test_long_running_recognize(client_stt, audio_data, client_operations):
    long_running_config = {
        "config": audio_data["config"],
        "group": "group_name"
    }
    response, uri, meta = client_stt.longrunning_recognize_with_uploader(
        audio_data["source"], long_running_config, with_response_meta=True
    )
    print(response)
    print(uri)
    print(user_utils.get_x_request_id(meta))
    time.sleep(1)
    results = client_operations.get_operation({"id": response["id"]})
    print(results)


def test_synthesis(client_tts, synthesis_config):
    client_tts.synthesize_to_audio_wav("Привет, как дела!", synthesis_config, "synthesis_speech")

