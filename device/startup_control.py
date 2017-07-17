import ipaddress


class StartupControl():
    def check_digit(self, port):
        if port.isdigit():
            return True
        else:
            return False

    def check_ip(self, ip):
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            return False
        else:
            return True