from socket import socket, AF_INET, SOCK_STREAM
import pyautogui
from PIL import ImageGrab
from io import BytesIO
from colorama import Fore
import traceback


class Server:
    def __init__(self):
        self.is_press = 0
        pyautogui.FAILSAFE = False
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
                        command = conn.recv(1024).decode('utf-8').split()
                        try:
                            if command[0] != 'None':
                                if command[0] == 'p':
                                    if not self.is_press:
                                        pyautogui.mouseDown()
                                        self.is_press = 1
                                    if len(command) == 4:
                                        self.mouse_active(command[1], int(command[2]), int(command[3]))

                                elif 'sc' in command:
                                    pyautogui.scroll(int(command[-1]))
                                elif len(command) == 3:
                                    self.mouse_active(command[0], int(command[1]), int(command[2]))
                                    if self.is_press:
                                        pyautogui.mouseUp()
                                        self.is_press = 0
                        except Exception as ex:
                            print(ex, end='')
                        print(f'\rsize: {size}, Output: {command}', end='')
                except Exception as ex:
                    print(Fore.RED, ex, traceback.format_exc(), Fore.RESET)

    @staticmethod
    def screenshot():
        frame = ImageGrab.grab()
        b = BytesIO()
        frame.save(b, "JPEG")
        frame_bytes = b.getvalue()
        size = str(len(frame_bytes)).encode('utf-8')
        return frame_bytes, size

    @staticmethod
    def mouse_active(flag, x, y):
        try:
            if flag == 'lk':
                pyautogui.leftClick(x, y)
            elif flag == 'rk':
                pyautogui.rightClick(x, y)
            elif flag == 'dlk':
                pyautogui.doubleClick(x, y)
            elif flag == 'm':
                pyautogui.moveTo(x, y)
        except pyautogui.FailSafeException:
            pass


if __name__ == '__main__':
    server = Server()
    server.run()
