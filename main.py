import multiprocessing
import os
import socket
from subprocess import Popen, call, PIPE
from time import sleep


""" To server
def exiting():
    while True:
        with open('1', 'r', encoding='utf-8') as file:
            f = int(file.read())
        if not f:
            print('Process exiting start and run reloader.')
            os._exit(1)
        sleep(3)


thread = Thread(target=exiting)

if __name__ == '__main__':
    thread.start()
    app.run(debug=True, port=80)
"""


class Start:
    def __init__(self):
        with open('1', 'w', encoding='utf-8') as file:
            file.write('1')
        self.server_prc = multiprocessing.Process(target=self.server, name='prc-server', daemon=True)
        self.conn = None

    @staticmethod
    def connection():
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(1)
            server.bind(('', 5008))
            print(2)
            server.listen()
            print(3)
            conn, addr = server.accept()
            print('Connected with', conn, addr)
            return conn, addr

        except Exception as ex:
            print(ex)
            return f'Error: {ex}'

    @staticmethod
    def server():
        call(r'C:\Users\akuzm\PycharmProjects\server_snake2\venv\Scripts\python.exe '
             r'C:\Users\akuzm\PycharmProjects\server_snake2\main.py ')

    def run(self):
        while True:

            print('start server')
            self.conn, addr = self.connection()
            try:
                while True:
                    data = self.conn.recv(1024)
                    command = data.decode('cp1125')
                    if command == 'stop':
                        print('stop')
                        with open('1', 'w', encoding='utf-8') as file:
                            file.write('0')
                        self.server_prc.join()
                        self.server_prc.terminate()
                        self.server_prc.close()
                        self.conn.send('Process was closed'.encode('cp1125'))
                        continue

                    elif command == 'start':
                        self.server_prc = multiprocessing.Process(target=self.server, name='prc-server', daemon=True)
                        with open('1', 'w', encoding='utf-8') as file:
                            file.write('1')
                        self.server_prc.start()
                        self.conn.send('Process was started'.encode('cp1125'))
                        continue

                    f = command.split()[0]
                    command = command[len(f) + 1:]
                    if 'cmd' == f:
                        print("'" + command + "'")
                        try:
                            process = Popen("powershell.exe", shell=False, stdin=PIPE,
                                            stdout=PIPE, stderr=PIPE, text=False)
                            out, err = process.communicate(command.encode('cp1125'))
                            data = out + err
                            print(1)
                        except Exception as ex:
                            data = str(ex).encode('cp1125')
                            print(2)
                        if len(data) == 0:
                            data = 'Нет результата'.encode('cp1125')
                            print(3)
                        print(len(data))

                        conn.send(str(len(data)).encode('cp1125'))
                        sleep(0.1)
                        conn.send(data)

                    elif f == 'file':
                        print('file')
                        if '\\' in command:
                            path = command[:command.rfind('\\')]
                            if not os.path.exists(path):
                                os.makedirs(path)
                        with open(command, 'wb') as file:
                            file.write(self.receive())
                        print('file')

                    elif f == 'del':
                        try:
                            os.remove(command)
                            conn.send(f'File {command} deleted'.encode('cp1125'))
                        except FileNotFoundError:
                            conn.send(f'File {command} not found'.encode('cp1125'))

                    print('>>>' + command)
            except Exception as ex:
                print(ex)
                conn.close()
            finally:
                conn.close()

    def receive(self):
        print('file receive')

        file_size = int(self.conn.recv(1024).decode('cp1125'))
        print(file_size)
        self.conn.send(b' ')
        receive_size = 0
        full_data = b''

        while receive_size < file_size:
            data = self.conn.recv(1024)
            receive_size += len(data)
            full_data += data

        self.conn.send('\nFile send'.encode('cp1125'))
        return full_data


if __name__ == '__main__':
    start = Start()
    start.run()
    print('Super run...')
