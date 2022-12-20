import pyautogui
import socket
import base64
import json
import time
import os


class VNCClient:
    def __init__(self, ip, port):
        print('__init__')
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                self.client.connect((ip, port))
                break
            except ConnectionError:
                time.sleep(5)

    # Переместить мышь по заданным координатам
    @staticmethod
    def mouse_active(mouse_flag, x, y):
        print('mouse_active')
        if mouse_flag == 'mouse_left_click':
            pyautogui.leftClick(int(x), int(y))
            return "mouse_left_click"

        elif mouse_flag == 'mouse_right_click':
            pyautogui.rightClick(int(x), int(y))
            return "mouse_right_click"

        elif mouse_flag == 'mouse_double_left_click':
            pyautogui.doubleClick(int(x), int(y))
            return "mouse_double_left_click"

    # Обработать изображение с экрана
    @staticmethod
    def screen_handler():
        print('screen_handler')
        pyautogui.screenshot('1.png')
        with open('1.png', 'rb') as file:
            reader = base64.b64encode(file.read())
        os.remove('1.png')
        return reader

    # Обработка входящих команд
    def execute_handler(self):
        print('execute_handler')
        while True:
            responce = self.receive_json().split()
            print(responce)
            if responce[0] == 'screen':
                result = self.screen_handler()
            elif 'mouse' in responce[0]:
                result = self.mouse_active(responce[0], responce[1], responce[2])
            else:
                result = ''
            self.send_json(result)

    # Отправляем json данные серверу
    def send_json(self, data):
        print('send_json')
        # Если данные окажутся строкой
        try:
            json_data = json.dumps(data.decode('utf-8'))
        except AttributeError:
            json_data = json.dumps(data)
        self.client.send(json_data.encode('utf-8'))

    # Получаем json данные от сервера
    def receive_json(self):
        print('receive_json')
        json_data = ''
        while True:
            try:
                json_data += self.client.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except:
                pass


if __name__ == '__main__':
    client = VNCClient('127.0.0.1', 5009)
    client.execute_handler()
