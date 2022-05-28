import socket

HOST = 'localhost'
PORT = 1228


def client():
    try:
        client_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    except Exception as e:
        print(e)
        return

    msg = input()
    client_socket.sendto(msg.encode('utf-8'), (HOST, PORT))
    print(f'Client message: {msg}')

    try:
        response, _ = client_socket.recvfrom(1024)
        response = response.decode('utf-8')
        print(f'Server response: {response}')
    except socket.timeout:
        print('Request timeout')

    client_socket.close()


if __name__ == '__main__':
    client()
