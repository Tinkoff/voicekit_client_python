from jsonschema import validate

from tinkoff_voicekit_client.Operations.helper_operations import (
    get_proto_operation_request,
    get_proto_delete_operation_request,
    get_proto_list_operations_request,
    get_proto_watch_operations_request,
    get_proto_wait_operation_request
)
from tinkoff_voicekit_client.speech_utils.BaseClient.base_client import BaseClient
from tinkoff_voicekit_client.speech_utils.apis.tinkoff.cloud.longrunning.v1.longrunning_pb2_grpc import OperationsStub
from tinkoff_voicekit_client.speech_utils.config_data import client_config
from tinkoff_voicekit_client.speech_utils.core import response_format, dict_generator
from tinkoff_voicekit_client.speech_utils.metadata import Metadata


class ClientOperations(BaseClient):
    definitions = {
        "OperationStateFilter": {
            "type": "string",
            "enum": ["ENQUEUED", "PROCESSING", "DONE", "FAILED"]
        },
        "ServiceIDFilter": {
            "oneOf": [
                {"exact_service_id": {"type": "string"}},
                {"any_service_id": {"type": "object"}}
            ]
        },
        "IDFilter": {
            "oneOf": [
                {"exact_id": {"type": "string"}},
                {"any_id": {"type": "object"}}
            ]
        },
        "GroupFilter": {
            "oneOf": [
                {"exact_group": {"type": "string"}},
                {"any_group": {"type": "object"}}
            ]
        }
    }

    operation_filter_config_schema = {
        "type": "object",
        "definitions": definitions,
        "properties": {
            "service_id": {"$ref": "#/definitions/ServiceIDFilter"},
            "id": {"$ref": "#/definitions/IDFilter"},
            "group": {"$ref": "#/definitions/GroupFilter"},
            "state": {
                "type": "array",
                "items": {"$ref": "#/definitions/OperationStateFilter"}
            },
        }
    }

    list_operations_config_schema = {
        "type": "object",
        "operation_filter": operation_filter_config_schema,
        "properties": {
            "filter": {"$ref": "#/operation_filter"},
            "page_size": {"type": "number"},
            "page_token": {"type": "string"}
        }
    }

    get_operation_config_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string"}
        }
    }

    wait_operation_config_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "timeout": {"type": "string"}
        }
    }

    watch_operations_config_schema = {
        "type": "object",
        "operation_filter": operation_filter_config_schema,
        "properties": {
            "filter": {"$ref": "#/operation_filter"},
            "listen_for_updates": {"type": "boolean"}
        }
    }

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
        Create client for long running operations.
            :param api_key: client public api key
            :param secret_key: client secret api key
            :param host: Tinkoff Voicekit speech operations host url
            :param port: Tinkoff Voicekit speech operations port, default value: 443
            :param ca_file: optional certificate file
        """
        super().__init__(host, port, ssl_channel, ca_file)
        self._metadata = Metadata(api_key, secret_key, "tinkoff.cloud.longrunning")
        self._api_key = api_key
        self._secret_key = secret_key
        self._stub = OperationsStub(self._channel)

    def get_operation(self, request: dict, metadata=None, dict_format=True):
        """
        Return operation by operation ID
            :param request: operation request
            :param metadata: configure own metadata
            :param dict_format: dict response instead of proto object
        """
        validate(request, ClientOperations.get_operation_config_schema)
        response = self._stub.GetOperation(
            get_proto_operation_request(request),
            metadata=metadata if metadata else self._metadata.metadata,
        )
        return response_format(response, dict_format)

    def delete_operation(self, operation_filter: dict, metadata=None, dict_format=True):
        """
        Delete all operations matching operation filter
            :param operation_filter: configure operation filter
            :param metadata: configure own metadata
            :param dict_format: dict response instead of proto object
        """
        validate(operation_filter, ClientOperations.operation_filter_config_schema)
        response = self._stub.DeleteOperation(
            get_proto_delete_operation_request(operation_filter),
            metadata=metadata if metadata else self._metadata.metadata,
        )
        return response_format(response, dict_format)

    def cancel_operation(self, operation_filter: dict, metadata=None, dict_format=True):
        """
        Cancel all operations matching operation filter
            :param operation_filter: configure operation filter
            :param metadata: configure own metadata
            :param dict_format: dict response instead of proto object
        """
        validate(operation_filter, ClientOperations.operation_filter_config_schema)
        response = self._stub.CancelOperation(
            get_proto_delete_operation_request(operation_filter),
            metadata=metadata if metadata else self._metadata.metadata,
        )
        return response_format(response, dict_format)

    def list_operations(self, request: dict, metadata=None, dict_format=True):
        """
        Return list with operations
            :param request: configure list operation request
            :param metadata: configure own metadata
            :param dict_format: dict response instead of proto object
        """
        validate(request, ClientOperations.list_operations_config_schema)
        response = self._stub.ListOperations(
            get_proto_list_operations_request(request),
            metadata=metadata if metadata else self._metadata.metadata,
        )
        return response_format(response, dict_format)

    def watch_operations(self, request: dict, metadata=None, dict_format=True):
        """
        Watch operations
            :param request: watch operations request
            :param metadata: configure own metadata
            :param dict_format: dict response instead of proto object
        """
        validate(request, ClientOperations.watch_operations_config_schema)
        response = self._stub.WatchOperations(
            get_proto_watch_operations_request(request),
            metadata=metadata if metadata else self._metadata.metadata,
        )
        return dict_generator(response, dict_format)

    def wait_operation(self, request: dict, metadata=None, dict_format=True):
        """
        Wait operation
            :param request: wait operation request
            :param metadata:  configure own metadata
            :param dict_format: dict response instead of proto object
        """
        validate(request, ClientOperations.wait_operation_config_schema)
        response = self._stub.WaitOperation(
            get_proto_wait_operation_request(request),
            metadata=metadata if metadata else self._metadata.metadata,
        )
        return response_format(response, dict_format)
