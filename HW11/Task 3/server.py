import socket

HOST = 'localhost'
PORT = 1228


def server():
    try:
        server_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        server_socket.bind((HOST, PORT))
    except Exception as e:
        print(e)
        return

    print('Server is working!')
    while True:
        msg, address = server_socket.recvfrom(1024)
        msg = msg.decode('utf-8')
        print(f'Client message: {msg}')

        msg = msg.upper()
        print(f'Server message: {msg}')
        server_socket.sendto(msg.encode('utf-8'), address)


if __name__ == '__main__':
    server()
