import os
import sys
import json
import glob
import base64
from des import *
import socket
from PyQt5 import QtGui


class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(list)

    def __init__(self, ip, port, parent=None):
        print('__init__')
        QtCore.QThread.__init__(self, parent)

        # Принимаем глобальные переменные
        self.active_socket = None
        self.ip = ip
        self.port = port
        self.command = 'screen'

        # Создаем TCP-Сервер
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.listen()

    # Принимаем и обрабатываем изображение
    def run(self):
        print('run')
        # Принимаем входящее соединение
        data_connection, address = self.server.accept()
        self.active_socket = data_connection

        while True:
            print(self.command)
            if self.command.split(' ')[0] != 'screen':
                self.send_json(self.command)
                responce = self.receive_json()
                self.mysignal.emit([responce])
                self.command = 'screen'
            if self.command.split(' ')[0] == 'screen':
                self.send_json(self.command)
                responce = self.receive_json()
                self.mysignal.emit([responce])

    # Отправка json-данных клиенту
    def send_json(self, data):
        print('send_json')
        # Обрабатываем бинарные данные
        try:
            json_data = json.dumps(data.encode('utf-8'))
        except TypeError:
            json_data = json.dumps(data)

        # В случае если клиент разорвал соединение, но сервер отправляет команду
        try:
            self.active_socket.send(json_data.encode('utf-8'))
        except ConnectionResetError:
            # Отключаемся от текущей сессии
            self.active_socket = None

    # Получаем json данные от клиента
    def receive_json(self):
        print('receive_json')
        json_data = ''
        while True:
            try:
                if self.active_socket is not None:
                    json_data += self.active_socket.recv(1024).decode('utf-8')
                    return json.loads(json_data)
                else:
                    return None
            except ValueError:
                pass


class VNCServer(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        print('VNCServer  __init__')
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Создаем экземпляр обработчика
        self.ip = '127.0.0.1'
        self.port = 5009
        self.thread_handler = MyThread(self.ip, self.port)
        self.thread_handler.start()

        # Обработчик потока для обновление GUI
        self.thread_handler.mysignal.connect(self.screen_handler)

    # Обработка и вывод изображения
    def screen_handler(self, screen_value):
        print('screen_handler')
        data = ['mouse_move_to', 'mouse_left_click',
                'mouse_right_click', 'mouse_double_left_click']

        # В случае если это не скрин, пропускаем шаг
        if screen_value[0] not in data:
            decrypt_image = base64.b64decode(screen_value[0])
            with open('2.png', 'wb') as file:
                file.write(decrypt_image)

            # Выводим изображение в панель
            image = QtGui.QPixmap('2.png')

            self.ui.label.setPixmap(image)

    # После закрытия сервера удаляем изображения
    def closeEvent(self, event):
        print('closeEvent')
        for file in glob.glob('*.png'):
            try:
                os.remove(file)
            except FileNotFoundError:
                pass

    # Обработка EVENT событий
    def event(self, event):
        print('event', end='\r')
        # Обработка ЛКМ, ПКМ
        if event.type() == QtCore.QEvent.MouseButtonPress:
            current_button = event.button()  # Определяем нажатую кнопку

            if current_button == 1:
                mouse_cord = f'mouse_left_click {event.x()} {event.y()}'
            else:
                mouse_cord = f'mouse_right_click {event.x()} {event.y()}'
            self.thread_handler.command = mouse_cord

        # Движение мыши без нажатий
        elif event.type() == QtCore.QEvent.MouseMove:
            mouse_cord = f'mouse_move_to {event.x()} {event.y()}'
            self.thread_handler.command = mouse_cord

        # Обработка double-кликов
        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            mouse_cord = f'mouse_double_left_click {event.x()} {event.y()}'
            self.thread_handler.command = mouse_cord

        return QtWidgets.QWidget.event(self, event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    print(1)
    myapp = VNCServer()
    print(2)
    myapp.show()
    print(3)
    sys.exit(app.exec_())
