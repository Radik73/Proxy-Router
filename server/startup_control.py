class StartupControl():
    def check_numdber_of_port(self, port):
        if port.isdigit():
            return True
        else:
            return False

    def check_version(self, version):
        if version.isalnum():
            print('Version of server: {version}'.format(version=version))
            return True
        else:
            return False