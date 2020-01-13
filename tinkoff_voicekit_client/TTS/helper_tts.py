import json
import os
import wave
from google.protobuf import json_format
from tinkoff_voicekit_client.speech_utils.apis import tts_pb2


def get_encoder(encoding: str, rate: int):
    if encoding == "LINEAR16":
        return lambda audio_chunk: list(map(lambda x: int(x), audio_chunk))
    elif encoding == "RAW_OPUS":
        from opuslib import Decoder
        decode = Decoder(rate, channels=1).decode
        return lambda audio_chunk: list(map(lambda x: int(x), decode(audio_chunk, frame_size=int(0.12 * rate))))
    else:
        raise NotImplemented("Another encoding is not supported")


def save_synthesize_wav(
        audio_content: bytes,
        file_name: str,
        rate: int,
        channels: int = 1
):
    with wave.open(file_name, "wb") as wav_out:
        wav_out.setnframes(len(audio_content))
        wav_out.setframerate(rate)
        wav_out.setnchannels(channels)
        wav_out.setsampwidth(2)
        wav_out.writeframes(audio_content)


def get_config(config: dict):
    return json_format.Parse(json.dumps(config), tts_pb2.AudioConfig())


def get_utterance_generator(text_source):
    return generate_file_utterances if os.path.isfile(text_source) else generate_text_utterances


def generate_utterance(line: str):
    text = line.strip()
    return None if not text or text.startswith("#") else text


def generate_file_utterances(text_file: str, text_encoding: str):
    with open(text_file, "r", encoding=text_encoding) as f:
        for line in f:
            result = generate_utterance(line)
            if result is None:
                continue
            else:
                yield result


def generate_text_utterances(text: str, text_encoding: str):
    yield text.encode(text_encoding).strip()
