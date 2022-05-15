import socket
import PySimpleGUI as gui
from time import time

PACKET_SIZE = 1024


def sgui():
    return gui.Window('Получатель TCP', [
        [gui.Text('Введите IP  адрес', size=(22, 1)),
         gui.InputText('127.0.0.1', key='host')],
        [gui.Text('Введите порт для получения', size=(22, 1)),
         gui.InputText('1228', key='port')],
        [gui.Text('Скорость соединения', size=(22, 1)), gui.Text(key='speed')],
        [gui.Text('Число полученных пакетов', size=(22, 1)),
         gui.Text(key='packets')],
        [gui.Button('Получить')],
    ])


def receive_packets(window):
    total_packets = 0
    speed = 0
    last_time = 1

    while True:
        event, values = window.read()

        if event in (None, 'Exit'):
            break

        if event == 'Получить':
            host, port = values['host'], int(values['port'])
            ssocl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssocl.bind((host, port))
            ssocl.listen(1)

            packets_count = 0
            first_time = 0

            try:
                rsock, _ = ssocl.accept()
                total_packets = int(
                    rsock.recv(PACKET_SIZE).decode('utf-8'))
                for i in range(total_packets):
                    try:
                        time_now = time()
                        rmsg = rsock.recv(PACKET_SIZE).decode('utf-8')
                        if rmsg != '':
                            packets_count += 1
                            if first_time == 0:
                                first_time = time_now
                    except socket.timeout:
                        print('Request timeout')
                last_time = time()
                rsock.close()
            except Exception as e:
                print(e)

            total_time = (last_time - first_time) * 1000
            if total_time > 0:
                speed = round(PACKET_SIZE * packets_count / total_time)
            window['packets'].Update(f'{packets_count}/{total_packets}')
            window['speed'].Update(f'{speed} KB/s')

            ssocl.close()


if __name__ == '__main__':
    window = sgui()
    receive_packets(window)
