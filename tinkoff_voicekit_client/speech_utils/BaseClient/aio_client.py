import grpc

from tinkoff_voicekit_client.speech_utils.BaseClient.base_client import AbstractBaseClient


class BaseClient(AbstractBaseClient):
    """
    This class provide base methods for STT, TTS, Operations
    """
    def __init__(self, host, port, ssl_channel=False, ca_file=None, options: list = None):
        super().__init__(host, port, ssl_channel, ca_file, options)

    def _make_channel(self):
        target = "{}:{}".format(self._host, self._port)
        if self._ssl_channel:
            creds = self._get_credential()
            return grpc.aio.secure_channel(target, creds, options=self._options)
        else:
            return grpc.aio.insecure_channel(target, options=self._options)

    async def close(self):
        await self._channel.close()
