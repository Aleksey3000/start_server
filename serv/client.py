import os
import sys
from socket import socket, AF_INET, SOCK_STREAM
from PyQt5 import QtGui
from des import *
from colorama import Fore


class ClientThread(QtCore.QThread):
    signal_frame = QtCore.pyqtSignal(bytes)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.client = socket(AF_INET, SOCK_STREAM)
        self.command = 'None'
        hosts = ('127.0.0.1', '192.168.0.102', 'supersite.ddnsking.com')
        port = 5007
        for host in hosts:
            try:
                print(f'\rConnecting to {host}:{port}', end='')
                self.client.connect((host, port))
                print(Fore.GREEN, '\nПодключено')
                return
            except Exception as ex:
                print(Fore.RED, f'\rFailed to connect to {host} {ex}')
        raise ConnectionError

    def run(self):
        print('run')
        while True:
            frame = self.receive()
            print(f' | event - {self.command}', end='')
            self.signal_frame.emit(frame)
            self.client.send(self.command.encode('cp1125'))
            self.command = 'None'


    def receive(self):
        data = self.client.recv(1024).decode('cp1125')
        if data:
            full_size = int(data)
            print(Fore.RESET, f'\rsize: {full_size}', end='')
            size = 0
            frame = b''
            while size < full_size:
                data = self.client.recv(1024)
                size += len(data)
                frame += data

            return frame
        return self.receive()


class Client(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        print('Client  __init__')
        self.thread = ClientThread()
        QtWidgets.QWidget.__init__(self, parent)
        print(1)
        self.ui = Ui_MainWindow()
        print(2)
        self.ui.setupUi(self)
        print(3)
        self.pixmap = QtGui.QPixmap()

        self.thread.start()
        self.thread.signal_frame.connect(self.show_frame)

    def show_frame(self, frame):
        self.pixmap.loadFromData(frame)
        self.ui.label.setPixmap(self.pixmap)

    def event(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            current_button = event.button()

            if current_button == 1:
                self.thread.command = f'lk {event.x()} {event.y()}'
            else:
                self.thread.command = f'rk {event.x()} {event.y()}'

        elif event.type() == QtCore.QEvent.MouseMove:
            self.thread.command = f'm {event.x()} {event.y()}'

        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            self.thread.command = f'dlk {event.x()} {event.y()}'


        return QtWidgets.QWidget.event(self, event)

    def closeEvent(self, event):
        print('close')
        self.thread.client.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    print(1, 's')
    application = Client()
    print(2, 's')
    application.show()
    print(3, 's')
    sys.exit(app.exec_())
