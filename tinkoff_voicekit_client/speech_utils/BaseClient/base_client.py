import grpc

from tinkoff_voicekit_client.speech_utils.config_data import MAX_LENGTH


class BaseClient:
    """
    This class provide base methods for STT, TTS, Operations
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

    def __del__(self):
        if hasattr(self, "_channel"):
            self._channel.close()

    def _configure_channel(self, options):
        if options:
            self._options = options
        else:
            self._options = [
                ('grpc.max_send_message_length', MAX_LENGTH),
                ('grpc.max_receive_message_length', MAX_LENGTH)
            ]

    def _make_channel(self):
        target = "{}:{}".format(self._host, self._port)
        if self._ssl_channel:
            if self._ca_file:
                with open(self._ca_file, "rb") as pem:
                    creds = grpc.ssl_channel_credentials(pem.read())
            else:
                creds = grpc.ssl_channel_credentials()

            return grpc.secure_channel(target, creds, options=self._options)
        else:
            return grpc.insecure_channel(target, options=self._options)
