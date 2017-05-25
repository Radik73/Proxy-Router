def inspect(checked):
    list_for_checked = ['device_id', 'request_id', 'status', 'data']
    for key in list_for_checked:
        key_exists = key in checked
        if key_exists == False:
            return False
    return True

def inspect_for_numdber_of_port(checked):
    if checked.isdigit() and int(checked) <= 65535:
        return  True