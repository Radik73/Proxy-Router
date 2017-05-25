import ipaddress

def inspect_for_digits(checked):
    if checked.isdigit():
        return True

def inspect_for_numdber_of_port(checked):
    if checked.isdigit() and len(str(checked)) <= 4:
        return  True

def inspect_for_ip(checked):
    try:
        ipaddress.ip_address(checked)
    except ValueError:
        return False
    else:
        return True