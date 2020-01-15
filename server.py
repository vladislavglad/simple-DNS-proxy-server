import socket
import dnslib 

# create a socket to resieve queries. 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('', 53)
server_socket.bind(server_address)
# server_socket.listen(1)
print(f'Server is listening on port: {server_address[1]}\n')

# create a socket to send queries to external DNS server.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(10)
# use any public DNS server you like; I use Google's.
DNS_address = ('8.8.8.8', 53)

while True:
    try:

        # recieve query from an external socket.
        query, client_address = server_socket.recvfrom(1024)
        print(f'Recieved Packet: \n{query}\n')
        parsed_query = dnslib.DNSRecord.parse(query)
        print(f'Parsed Packet: \n{parsed_query}\n')

        domain_name = str(parsed_query.get_q())
        # print(f'Domain_name: \n{domain_name}\n')

        if 'playstation.com' in domain_name:
            # print('The website is in the question section of the query.\n')

            skeleton_reply = parsed_query.reply()
            skeleton_reply.add_answer(*dnslib.RR.fromZone('playstation.com A 127.0.0.1'))
            print(f'Initiated Response: \n{skeleton_reply}\n')

            response = skeleton_reply.pack()
            # response = bytes(response)
            server_socket.sendto(response, client_address)
            print(f'Sent Response: \n{response}\n')

        # add more elif statements if you need more custom resolutions.
        # TODO: put custom resolutions into one defined function.
        elif 'thearchstones.com' in domain_name:
            
            skeleton_reply = parsed_query.reply()
            skeleton_reply.add_answer(*dnslib.RR.fromZone('thearchstones.com A 127.0.0.1'))
            print(f'Initiated Response: \n{skeleton_reply}\n')
            
            response = skeleton_reply.pack()
            server_socket.sendto(response, client_address)
            print(f'Sent Response: \n{response}\n')
        
        else: 

            # if it is not in my list of specified domain names above, then query Google's public DNS.
            # and return the response directly to the client; so this server acts as proxy.
            client_socket.sendto(query, DNS_address)
            response = client_socket.recv(1024)
            server_socket.sendto(response, client_address)
            print(f'Sent Response from Google DNS: \n{response}\n')

            # pass

    except KeyboardInterrupt:
        # raise
        print('Key pressed')
        server_socket.close()
        client_socket.close()
    except socket.error as err:
        print(err)
        server_socket.close()
        client_socket.close()
        