
def get_x_request_id(metadata):
    """
    Returning x-request-id from response metadata
        :param metadata: response metadata from one of VoiceKit methods
    return: None if x-request-id don't contain in metadata
    """
    x_request_id = tuple(filter(lambda x: x[0] == 'x-request-id', metadata))
    if x_request_id:
        x_request_id = x_request_id[0][1]
        return x_request_id
    return None
