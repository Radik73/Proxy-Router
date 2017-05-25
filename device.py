import device.cmd_parser as psr
import device.checking as check
import device.device_main as dvs

if __name__ == '__main__':
    notification = 'Startup parameters are not correct'
    parser = psr.createParser()
    namespace = parser.parse_args()
    if check.inspect_for_ip(namespace.ip):
            if check.inspect_for_digits(namespace.identifier_of_device) and check.inspect_for_numdber_of_port(namespace.number_of_port):
                dvs.Device(namespace.ip, namespace.number_of_port, namespace.identifier_of_device)
            else:
                print(notification)
    else:
        print(notification)