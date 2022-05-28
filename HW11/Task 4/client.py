import socket
import numpy as np
import cv2

HOST = 'localhost'
PORT = 1228

# global var
img = np.zeros(shape=[400, 400, 3], dtype=np.uint8)
x_pointer = -1
y_pointer = -1
drawing = False
color = (255, 255, 255)
thickness = 2

# client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def draw_line(x_new, y_new):
    global x_pointer, y_pointer, img
    cv2.line(img, (x_pointer, y_pointer), (x_new, y_new), color,
             thickness=thickness)
    client_socket.send(
        f'{x_pointer} {y_pointer} {x_new} {y_new}:'.encode('utf-8'))


def draw_curve(event, x_new, y_new, flags, param):
    global x_pointer, y_pointer, drawing, img
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_pointer = x_new
        y_pointer = y_new
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        draw_line(x_new, y_new)
        x_pointer = x_new
        y_pointer = y_new
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            draw_line(x_new, y_new)
            x_pointer = x_new
            y_pointer = y_new


def client_window():
    cv2.namedWindow(winname="Client")
    cv2.setMouseCallback("Client",
                         draw_curve)

    while True:
        cv2.imshow("Client", img)

        if cv2.waitKey(10) == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    client_window()
