
from socket import inet_ntoa

def ip_int_to_ascii(int_ip):
    """Pad the integer IP before converting to ASCII."""

    return inet_ntoa(hex(int(int_ip))[2:-1].zfill(8).decode('hex'))

