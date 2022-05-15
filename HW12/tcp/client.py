import datetime
import socket
import PySimpleGUI as gui
from random import choice
from string import ascii_letters

PACKET_SIZE = 1024


def random_string(length):
    return ''.join(choice(ascii_letters) for _ in range(length))


def cgui():
    return gui.Window('Отправитель TCP', [
        [gui.Text('Введите IP адрес получателя', size=(32, 1)),
         gui.InputText('127.0.0.1', key='host')],
        [gui.Text('Введите порт получателя', size=(32, 1)),
         gui.InputText('1228', key='port')],
        [gui.Text('Введите количество пакетов для отправки', size=(32, 1)),
         gui.InputText('10', key='packets')],
        [gui.Button('Отправить пакеты')],
    ])


def send_packets(window):
    while True:
        event, values = window.read()

        if event in (None, 'Exit'):
            break

        if event == 'Отправить пакеты':
            try:
                host, port = values['host'], int(values['port'])
                packets_number = int(values['packets'])
            except Exception as e:
                print(e)

            try:
                csock = socket.socket(socket.AF_INET,
                                      socket.SOCK_STREAM)
                csock.connect((host, port))
                csock.sendall(
                    bytes(str(packets_number), encoding='utf-8'))
                for i in range(packets_number):
                    time_now = datetime.datetime.now()
                    msg = str(time_now) + ' ' + random_string(
                        PACKET_SIZE - len(str(time_now)) - 1)
                    csock.sendall(msg.encode('utf-8'))
                csock.close()
            except Exception as e:
                print(e)


if __name__ == '__main__':
    window = cgui()
    send_packets(window)
