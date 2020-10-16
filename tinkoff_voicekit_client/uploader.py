import os
from datetime import datetime

import boto3


class Uploader:
    UPLOADER_HOST = "s3.api.tinkoff.ai"
    STORAGE_PREFIX = "storage://"
    _BUCKET = "inbound"

    def __init__(
            self,
            api_key: str,
            secret_key: str,
            ca_file: str = None,
            host: str = None
    ):
        """
        Uploader upload data for Long running execution
            :param api_key: client public api key
            :param secret_key: client secret api key
            :param ca_file: optional certificate file
            :param host: Tinkoff Voicekit uploader host url
        """
        host = "https://{0}".format(Uploader.UPLOADER_HOST) if host is None else host
        self._api_key = api_key
        self._secret_key = secret_key
        self._s3 = boto3.client(
            service_name="s3",
            endpoint_url=host,
            aws_access_key_id=self._api_key,
            aws_secret_access_key=self._secret_key,
            verify=ca_file
        )

    def upload(self, source: str, object_name: str = None):
        """
        Upload data from source for long running execution
        uri has next schema: storage://UPLOADER_HOST/_BUCKET/<object_name>
            :param source: path to file or file like obj
            :param object_name: object name in storage (default: 'default_name_<utcnow>')
            :return: uri
        """
        if object_name is None:
            object_name = f"default_name_{datetime.utcnow()}"
        if os.path.isfile(source):
            self._s3.upload_file(source, Uploader._BUCKET, object_name)
        else:
            self._s3.upload_fileobj(source, Uploader._BUCKET, object_name)
        return "{0}{1}/{2}/{3}".format(
            Uploader.STORAGE_PREFIX,
            Uploader.UPLOADER_HOST,
            Uploader._BUCKET,
            object_name
        )

    @staticmethod
    def is_storage_uri(uri: str):
        """
        check uri on correct header
            :param uri: verifiable identifier
        """
        return isinstance(uri, str) and uri.startswith(f"{Uploader.STORAGE_PREFIX}")
