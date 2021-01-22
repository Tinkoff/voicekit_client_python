import os
import aioboto3

from datetime import datetime
from tinkoff_voicekit_client.Uploader.uploader import UploaderBase


class Uploader(UploaderBase):
    def __init__(self, api_key: str, secret_key: str, ca_file: str = None, host: str = None):
        """
        aio_voicekit Uploader upload data for Long running execution
            :param api_key: client public api key
            :param secret_key: client secret api key
            :param ca_file: optional certificate file
            :param host: Tinkoff Voicekit uploader host url
        """
        super().__init__(api_key, secret_key, ca_file, host)
        self._s3 = aioboto3.client(
            service_name="s3",
            endpoint_url=self._host,
            aws_access_key_id=self._api_key,
            aws_secret_access_key=self._secret_key,
            verify=self._ca_file
        )

    async def upload(self, source: str, object_name: str = None):
        """
        async Upload data from source for long running execution
        uri has next schema: storage://UPLOADER_HOST/_BUCKET/<object_name>
            :param source: path to file or file like obj
            :param object_name: object name in storage (default: 'default_name_<utcnow>')
            :return: uri
        """
        async with self._s3 as client:
            if object_name is None:
                object_name = f"default_name_{datetime.utcnow()}"
            if os.path.isfile(source):
                await client.upload_file(source, Uploader._BUCKET, object_name)
            else:
                await client.upload_fileobj(source, Uploader._BUCKET, object_name)
            return Uploader.create_uri(object_name)
