#!/usr/bin/env python3
"""
NetcatP Tool in Python
This Python script provides a simple and lightweight netcat dupe that allows users to
send and receive data over using IPv4 and IPv6 addresses. It is designed to be easy to use
and versatile, making it suitable for various networking tasks, including testing, debugging,
and learning purposes.
By keeping a simplistic command-line style, this script offers users an intuative interface for
communicating over. When launched with only a port number, the script will listen for incoming
traffic. When supplied with a target IP address and port, the script will both send and
receive data.
Keywords: Python, Netcat, UDP, TCP, Networking, IPv4, IPv6, Socket Programming, Command Line Tool,
          Lightweight, Versatile, Testing, Debugging, Learning
To use this script, run the following commands:
1. For receiving data only:
   python netcatp.py <port> <protocol>
2. For sending and receiving data:
   python netcatp.py <port> <target_host> <target_port> <protocol>
Replace <port> with the desired local port number, <target_host> with the target IPv4 or IPv6
address, and <target_port> with the target port number. Replace <protocol> with 0 for UDP or 1
for TCP, this argument is not required with UDP being default.
"""
import socket
import sys
import threading

def tcp_receiver(recv_sock, port):
    recv_sock.bind(('', port))
    print(f"Listening on port {port}...")
    recv_sock.listen(5)

    while True:
        con, addr = recv_sock.accept()
        data, addr = con.recvfrom(4096)
        print(f"Received from {addr}: {data.decode('utf-8')}")

def udp_receiver(recv_sock, port):
    recv_sock.bind(('', port))
    print(f"Listening on port {port}...")

    while True:
        data, addr = recv_sock.recvfrom(4096)
        print(f"Received from {addr}: {data.decode('utf-8')}")

def sender(send_sock, target_addr):
    print(f"Sending data to {target_addr[0]} on port {target_addr[1]}...")

    while True:
        line = input()
        send_sock.sendto(line.encode('utf-8'), target_addr)

def protocol(proto, argc):
    """
    Handles different protocol from arguement format to socket integer.
    Default value is 0=UDP.
    Other values include:
    1=TCP
    """
    proto_map = (socket.IPPROTO_UDP, socket.IPPROTO_TCP)

    if argc == 2 or argc ==4:
        sproto = socket.IPPROTO_UDP
    else:
        sproto = proto_map[proto]

    return sproto

def socket_type(proto, argc):
    """
    Define socket type based on given prtocol.
    This is for compatability.
    """
    type_map = (socket.SOCK_DGRAM, socket.SOCK_STREAM)

    if argc == 2 or argc == 4:
        stype = socket.SOCK_DGRAM
    else:
        stype = type_map[proto]

    return stype

def main():
    argc = len(sys.argv)
    if argc == 1 or argc > 5:
        print("Usage: python netcat_udp.py <port> [target_host target_port]")
        sys.exit(1)

    port = int(sys.argv[1])
    sproto = protocol(int(sys.argv[-1]), argc)
    stype = socket_type(int(sys.argv[-1]), argc)

    recv_sock = socket.socket(socket.AF_INET6, stype, proto=sproto)
    recv_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, False)

    if sproto == 17:
        recv_thread = threading.Thread(target=udp_receiver, args=(recv_sock, port))
    else:
        recv_thread = threading.Thread(target=tcp_receiver, args=(recv_sock, port))
    recv_thread.daemon = True # exit when main thread exits
    recv_thread.start()

    if argc == 4:
        target_host = sys.argv[2]
        target_port = int(sys.argv[3])

        addr_info = socket.getaddrinfo(target_host, target_port, socket.AF_UNSPEC, stype, proto=sproto)
        target_family, _, _, _, target_addr = addr_info[0]

        send_sock = socket.socket(target_family, stype, proto=sproto)

        send_thread = threading.Thread(target=sender, args=(send_sock, target_addr))
        send_thread.daemon = True # exit when main thread exits
        send_thread.start()
        send_thread.join()
        

    recv_thread.join()
    

if __name__ == "__main__":
    main()

