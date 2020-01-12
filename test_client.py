import socket
import dnslib
import binascii

# query in hexidecimal
packet = b'd5ad818000010005000000000377777706676f6f676c6503636f6d0000010001c00c0005000100000005000803777777016cc010c02c0001000100000005000442f95b68c02c0001000100000005000442f95b63c02c0001000100000005000442f95b67c02c0001000100000005000442f95b93'

# represented in binary
packet = binascii.unhexlify(packet)
print(f'\nInitial binary query packet: \n{packet}\n')

# create a client UDP socket, (since DNS lookups are done through UDP).
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(10)

# instead of '127.0.0.1' put your own ip of your DNS server.
# port should be 53 by default for DNS lookups (may require Administrator Rights).
server_address = ('127.0.0.1', 53)

try:
    client_socket.sendto(packet, server_address)
    response_packet = client_socket.recv(len(packet) + 30)

    print(f'Resolved packet (in binary): \n{response_packet}\n')
    print(f'Resolved packet (in hexideciaml): \n{binascii.hexlify(response_packet)}\n')
    print(f'Parsed packet (as per DiG): \n{dnslib.DNSRecord.parse(response_packet)}\n')

except socket.error as err:
    print(err)
finally:
    client_socket.close()