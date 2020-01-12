import socket
import dnslib 

server_address = ('', 53)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)
print(f'Server is listening on port: {server_address[1]}\n')
# server_socket.listen(1)

while True:
    try:
        packet, address = server_socket.recvfrom(1024)
        print(f'Recieved Packet: \n{packet}\n')
        parsed_packet = dnslib.DNSRecord.parse(packet)
        print(f'Parsed Packet: \n{parsed_packet}\n')

        question_section = parsed_packet.get_q()
        # print(f'Quesiton Section: \n{question_section}\n')

        if 'www.google.com' or 'google.com' in str(question_section):
            # print('The website is in the question section of the query.\n')

            skeleton_reply = parsed_packet.reply()
            skeleton_reply.add_answer(*dnslib.RR.fromZone('www.google.com A 1.2.3.4'))
            print(f'Initiated Response: \n{skeleton_reply}\n')

            response = skeleton_reply.pack()
            server_socket.sendto(response, address)
            print(f'Sent Response: \n{response}\n')
        
        # TODO: make it a proxy, where only specified Domain Names are resolved the way you want. 
        # Others should be resolved as per usual (through some public DNS).
        
    except KeyboardInterrupt:
        # raise
        print('Key pressed')
        server_socket.close()
    except socket.error as err:
        print(err)
        server_socket.close()
        