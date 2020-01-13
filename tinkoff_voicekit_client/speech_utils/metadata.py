import copy
from time import time
import hmac
import json
import base64


class Metadata:
    _TEN_MINUTES = 600

    _AUD = {
        "STT": "tinkoff.cloud.stt",
        "TTS": "tinkoff.cloud.tts"
    }

    _AUTH_PAYLOAD = {
        "iss": "best_issuer",
        "sub": "best_user",
        "aud": None
    }

    _HEADER = {
        "alg": "HS256",
        "typ": "JWT",
        "kid": None
    }

    def __init__(self, api_key: str, secret_key: str, aud: str = None):
        if aud is None: raise ValueError("Undefined type of metadata for STT or TTS")
        self._aud = aud
        self._api_key = api_key
        self._secret_key = secret_key
        jwt = self._create_jwt(api_key, secret_key)
        metadata = [
            ["authorization", "Bearer {0}".format(jwt)],
            ["x-api-key", api_key],
        ]

        self.metadata = metadata

    def _create_jwt(self, api_key: str, secret_key: str):
        header = copy.deepcopy(Metadata._HEADER)
        header["kid"] = api_key

        auth_payload = copy.deepcopy(Metadata._AUTH_PAYLOAD)
        auth_payload["aud"] = Metadata._AUD[self._aud]
        self._expiration_time = int(time()) + Metadata._TEN_MINUTES
        auth_payload["exp"] = self._expiration_time

        payload_bytes = json.dumps(auth_payload, separators=(',', ':')).encode("utf-8")
        header_bytes = json.dumps(header, separators=(',', ':')).encode("utf-8")
        payload_base64 = base64.urlsafe_b64encode(payload_bytes)
        header_base64 = base64.urlsafe_b64encode(header_bytes)

        data = header_base64 + b"." + payload_base64
        signature_bytes = hmac.new(base64.urlsafe_b64decode(self._pad_base64(secret_key)),
                                   msg=data,
                                   digestmod="sha256")
        signature = base64.urlsafe_b64encode(signature_bytes.digest())

        jwt = data + b"." + signature
        return jwt.decode("utf-8")

    def _pad_base64(self, base64_str):
        num_equals_signs = 4 - len(base64_str) % 4
        return base64_str + '=' * num_equals_signs

    def is_fresh_jwt(self):
        return self._expiration_time > int(time())

    def refresh_jwt(self):
        api_key = self.metadata[1][1]
        self.metadata[0][1] = "Bearer {0}".format(self._create_jwt(api_key, self._secret_key))
