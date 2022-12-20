import os
import sys
from socket import socket, AF_INET, SOCK_STREAM
import pyautogui
from PIL import ImageGrab
from time import sleep
from io import BytesIO
from colorama import Fore


class Server:
    def __init__(self):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(('', 5007))
        self.server.listen()

    def run(self):

        while True:
            conn, addr = self.server.accept()
            with conn:
                print(Fore.GREEN, 'Connection: ', str(conn), end='')
                print(Fore.RESET)
                try:
                    while True:
                        frame, size = self.screenshot()
                        conn.send(size)
                        conn.send(frame)
                        command = conn.recv(1024).decode('cp1125')
                        if command:
                            command = command.split()
                            self.mouse_active(command[0], int(command[1]), int(command[2]))
                        print(f'\rOutput: {command}', end='')
                        print(f'\rsize: {size}', end='')
                except Exception as ex:
                    print(Fore.RED + str(ex))

    @staticmethod
    def screenshot():
        frame = ImageGrab.grab()
        b = BytesIO()
        frame.save(b, "JPEG")
        frame_bytes = b.getvalue()
        size = str(len(frame_bytes)).encode('cp1125')
        return frame_bytes, size

    @staticmethod
    def mouse_active(flag, x, y):
        print('mouse_active')
        if flag == 'lc':
            pyautogui.leftClick(x, y)

        elif flag == 'rk':
            pyautogui.rightClick(x, y)

        elif flag == 'dlk':
            pyautogui.doubleClick(x, y)
        elif flag == 'm':
            pyautogui.moveTo(x, y)


if __name__ == '__main__':
    server = Server()
    server.run()
