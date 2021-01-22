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
