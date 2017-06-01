def shaper(dict_of_data):
    payload = {'device_id': dict_of_data['device_id'], 'request_id': dict_of_data['request_id'], 'status': dict_of_data['status']}
    return(payload)