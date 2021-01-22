import grpc

from abc import ABC, abstractmethod

from tinkoff_voicekit_client.speech_utils.config_data import MAX_LENGTH


class AbstractBaseClient(ABC):
    """
    This class provide abstract channel creation.
    _make_channel must be overridden.
    """

    def __init__(
            self,
            host,
            port,
            ssl_channel=False,
            ca_file=None,
            options: list = None,
    ):
        self._host = host
        self._port = port
        self._ssl_channel = ssl_channel
        self._ca_file = ca_file
        self._configure_channel(options)
        self._channel = self._make_channel()

    def _configure_channel(self, options):
        if options:
            self._options = options
        else:
            self._options = [
                ('grpc.max_send_message_length', MAX_LENGTH),
                ('grpc.max_receive_message_length', MAX_LENGTH)
            ]

    def _get_credential(self):
        if not self._ca_file:
            return grpc.ssl_channel_credentials()
        with open(self._ca_file, "rb") as pem:
            return grpc.ssl_channel_credentials(pem.read())

    @abstractmethod
    def _make_channel(self):
        pass


class BaseClient(AbstractBaseClient):
    """
    This class provide base methods for STT, TTS, Operations
    """
    def __init__(self, host, port, ssl_channel=False, ca_file=None, options: list = None):
        super().__init__(host, port, ssl_channel, ca_file, options)

    def __del__(self):
        if hasattr(self, "_channel"):
            self._channel.close()

    def _make_channel(self):
        target = "{}:{}".format(self._host, self._port)
        if self._ssl_channel:
            creds = self._get_credential()
            return grpc.secure_channel(target, creds, options=self._options)
        else:
            return grpc.insecure_channel(target, options=self._options)
