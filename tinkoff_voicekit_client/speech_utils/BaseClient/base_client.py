import grpc

from tinkoff_voicekit_client.speech_utils.config_data import MAX_LENGTH


class BaseClient:
    """
    This class provide base methods for STT and TTS
    """

    def __init__(self):
        pass

    def _make_channel(self, host, port, ca_file=None):
        target = "{}:{}".format(host, port)
        if port == 443:
            if ca_file:
                with open(ca_file, "rb") as pem:
                    creds = grpc.ssl_channel_credentials(pem.read())
            else:
                creds = grpc.ssl_channel_credentials()

            return grpc.secure_channel(target, creds, options=[
                ('grpc.max_send_message_length', MAX_LENGTH),
                ('grpc.max_receive_message_length', MAX_LENGTH)]
                                       )
        else:
            return grpc.insecure_channel(target)
