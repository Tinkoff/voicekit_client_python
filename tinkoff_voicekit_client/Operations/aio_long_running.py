from jsonschema import validate

from tinkoff_voicekit_client.Operations import config_schema
from tinkoff_voicekit_client.Operations.helper_operations import (
    get_proto_operation_request,
    get_proto_delete_operation_request,
    get_proto_list_operations_request,
    get_proto_watch_operations_request,
    get_proto_wait_operation_request
)
from tinkoff_voicekit_client.speech_utils.BaseClient import aio_client
from tinkoff_voicekit_client.speech_utils.apis.tinkoff.cloud.longrunning.v1.longrunning_pb2_grpc import OperationsStub
from tinkoff_voicekit_client.speech_utils.config_data import client_config, aud
from tinkoff_voicekit_client.speech_utils.infrastructure import response_format, aio_dict_generator
from tinkoff_voicekit_client.speech_utils.metadata import Metadata


class ClientOperations(aio_client.BaseClient):

    def __init__(
            self,
            api_key: str,
            secret_key: str,
            host: str = client_config["host_operations"],
            port: int = client_config["port"],
            ssl_channel: bool = True,
            ca_file: str = None
    ):
        """
        Create async client for long running operations.
            :param api_key: client public api key
            :param secret_key: client secret api key
            :param host: Tinkoff Voicekit speech operations host url
            :param port: Tinkoff Voicekit speech operations port, default value: 443
            :param ca_file: optional certificate file
        """
        super().__init__(host, port, ssl_channel, ca_file)
        self._metadata = Metadata(api_key, secret_key, aud["operations"])
        self._api_key = api_key
        self._secret_key = secret_key
        self._stub = OperationsStub(self._channel)

    async def get_operation(self, request: dict, metadata=None, dict_format=True):
        """
        Return operation by operation ID
            :param request: operation request
            :param metadata: configure own metadata
            :param dict_format: dict response instead of proto object
        """
        validate(request, config_schema.get_operation_config_schema)
        response = await self._stub.GetOperation(
            get_proto_operation_request(request),
            metadata=metadata if metadata else self._metadata.metadata,
        )
        return response_format(response, dict_format)

    async def delete_operation(self, operation_filter: dict, metadata=None, dict_format=True):
        """
        Delete all operations matching operation filter
            :param operation_filter: configure operation filter
            :param metadata: configure own metadata
            :param dict_format: dict response instead of proto object
        """
        validate(operation_filter, config_schema.operation_filter_config_schema)
        response = await self._stub.DeleteOperation(
            get_proto_delete_operation_request(operation_filter),
            metadata=metadata if metadata else self._metadata.metadata,
        )
        return response_format(response, dict_format)

    async def cancel_operation(self, operation_filter: dict, metadata=None, dict_format=True):
        """
        Cancel all operations matching operation filter
            :param operation_filter: configure operation filter
            :param metadata: configure own metadata
            :param dict_format: dict response instead of proto object
        """
        validate(operation_filter, config_schema.operation_filter_config_schema)
        response = await self._stub.CancelOperation(
            get_proto_delete_operation_request(operation_filter),
            metadata=metadata if metadata else self._metadata.metadata,
        )
        return response_format(response, dict_format)

    async def list_operations(self, request: dict, metadata=None, dict_format=True):
        """
        Return list with operations
            :param request: configure list operation request
            :param metadata: configure own metadata
            :param dict_format: dict response instead of proto object
        """
        validate(request, config_schema.list_operations_config_schema)
        response = await self._stub.ListOperations(
            get_proto_list_operations_request(request),
            metadata=metadata if metadata else self._metadata.metadata,
        )
        return response_format(response, dict_format)

    async def watch_operations(self, request: dict, metadata=None, dict_format=True):
        """
        Watch operations
            :param request: watch operations request
            :param metadata: configure own metadata
            :param dict_format: dict response instead of proto object
        """
        validate(request, config_schema.watch_operations_config_schema)
        response = self._stub.WatchOperations(
            get_proto_watch_operations_request(request),
            metadata=metadata if metadata else self._metadata.metadata,
        )
        return aio_dict_generator(response, dict_format)

    async def wait_operation(self, request: dict, metadata=None, dict_format=True):
        """
        Wait operation
            :param request: wait operation request
            :param metadata:  configure own metadata
            :param dict_format: dict response instead of proto object
        """
        validate(request, config_schema.wait_operation_config_schema)
        response = await self._stub.WaitOperation(
            get_proto_wait_operation_request(request),
            metadata=metadata if metadata else self._metadata.metadata,
        )
        return response_format(response, dict_format)
