import socket
import cv2
import numpy as np

HOST = "localhost"
PORT = 1228


def conn_ss():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    conn, _ = server_socket.accept()
    return conn


def server_window(conn):
    img = np.zeros(shape=[400, 400, 3], dtype=np.uint8)
    color = (255, 255, 255)
    thickness = 2
    cv2.namedWindow(winname="Server")
    cv2.imshow("Server", img)

    while True:
        cv2.imshow("Server", img)
        if cv2.waitKey(10) == 27:
            break
        data = conn.recv(1024).decode('utf-8')
        if data != '':
            for ends in data.split(':'):
                if ends == '':
                    break
                x_pointer, y_pointer, x_new, y_new = ends.split()
                cv2.line(img, (int(x_pointer), int(y_pointer)),
                         (int(x_new), int(y_new)), color,
                         thickness=thickness)

    conn.close()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    conn = conn_ss()
    server_window(conn)
