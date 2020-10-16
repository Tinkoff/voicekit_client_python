import json

from google.protobuf import json_format

import tinkoff_voicekit_client.speech_utils.apis.tinkoff.cloud.longrunning.v1.longrunning_pb2 as pb_operations


def get_proto_operation_request(request: dict):
    grpc_request = json_format.Parse(json.dumps(request), pb_operations.GetOperationRequest())
    return grpc_request


def get_proto_delete_operation_request(operation_filter: dict):
    grpc_filter = json_format.Parse(json.dumps(operation_filter), pb_operations.OperationFilter())
    grpc_delete_request = pb_operations.DeleteOperationRequest()
    grpc_delete_request.filter.CopyFrom(grpc_filter)
    return grpc_delete_request


def get_proto_list_operations_request(request: dict):
    grpc_list_operation_request = json_format.Parse(json.dumps(request), pb_operations.ListOperationsRequest())
    return grpc_list_operation_request


def get_proto_cancel_operation_request(operation_filter: dict):
    grpc_filter = json_format.Parse(json.dumps(operation_filter), pb_operations.OperationFilter())
    grpc_cancel_request = pb_operations.CancelOperationRequest()
    grpc_cancel_request.filter.CopyFrom(grpc_filter)
    return grpc_cancel_request


def get_proto_watch_operations_request(request: dict):
    grpc_watch = json_format.Parse(json.dumps(request), pb_operations.WatchOperationsRequest())
    return grpc_watch


def get_proto_wait_operation_request(request: dict):
    grpc_wait = json_format.Parse(json.dumps(request), pb_operations.WaitOperationRequest())
    return grpc_wait
