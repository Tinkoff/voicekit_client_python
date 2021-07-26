"""
This file consider config parameters for authorization to server VoiceKit
"""

MAX_LENGTH = 32 * 10**6
CHUNK_SIZE = 8192

language_code = "ru-RU"

client_config = {
    "host_stt": "api.tinkoff.ai",
    "host_tts": "api.tinkoff.ai",
    "host_operations": "api.tinkoff.ai",
    "port": 443
}

aud = {
    "stt": "tinkoff.cloud.stt",
    "tts": "tinkoff.cloud.tts",
    "operations": "tinkoff.cloud.longrunning"
}
