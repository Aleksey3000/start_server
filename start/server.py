import sys
import multiprocessing
import os
import subprocess
import socket
from send.server import SendProject


class Start:
    def __init__(self):
        self.RUN = r'C:\Users\79212\PycharmProjects\project\start\run'

        print('start server')
        self.conn, addr = self.connection()
        self.send_project = SendProject(self.conn)

        with open(self.RUN, 'w', encoding='utf-8') as file1:
            self.process = {}
            with open('projects', 'r', encoding='utf-8') as file:
                for project in file.read().split('\n'):
                    key, val = project.split(' - ')
                    self.process[key] = [multiprocessing.Process(target=self.server, args=(key, val),
                                                                 name=key, daemon=True), 0]
                    file1.write(f'{key} - 0\n')
        print(self.process)


    @staticmethod
    def connection():
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(1)
            server.bind(('', 5006))
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
    def server(project, app):
        subprocess.call(fr'C:\Users\79212\PycharmProjects\{project}\venv\Scripts\python.exe '
                        fr'C:/Users/79212/PycharmProjects/{project}/{app}')

    def run(self):
        while True:
            try:
                while True:
                    data = self.conn.recv(1024)
                    command = data.decode('cp1125')

                    f = command.split()[0]
                    command = command[len(f) + 1:]

                    if f == 'stop':
                        self.process[command][1] = 0
                        with open(self.RUN, 'w', encoding='utf-8') as file:
                            for key, prc in self.process.items():
                                file.write(f'{key} - {prc[1]}\n')
                        print('exit')
                        self.process[command][0].join()
                        self.process[command][0].terminate()
                        self.conn.send(f'Process {command} was closed'.encode('cp1125'))


                    elif f == 'start':
                        self.process[command][1] = 1
                        with open(self.RUN, 'w', encoding='utf-8') as file:
                            for key, prc in self.process.items():
                                file.write(f'{key} - {prc[1]}\n')
                        self.process[command][0].start()
                        self.conn.send('Process was started'.encode('cp1125'))

                    elif 'cmd' == f:
                        self.cmd(command)

                    elif f == 'file':
                        if '\\' in command:
                            path = command[:command.rfind('\\')]
                            if not os.path.exists(path):
                                os.makedirs(path)
                        with open(command, 'wb') as file:
                            file.write(self.receive())
                    elif f == 'send':
                        self.send_project.run()

                    elif f == 'del':
                        try:
                            os.remove(command)
                            self.conn.send(f'File {command} deleted'.encode('cp1125'))
                        except FileNotFoundError:
                            self.conn.send(f'File {command} not found'.encode('cp1125'))

                    print('>>>' + command)
            except Exception as ex:
                print(ex)
                self.conn.close()
            finally:
                self.conn.close()

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

    def cmd(self, command):
        print("'" + command + "'")
        try:
            data = subprocess.check_output('cd C:/Users/79212/PycharmProjects/myserver', shell=True)
            data += subprocess.check_output(command, shell=True)
            print(1)
        except Exception as ex:
            data = str(ex).encode('cp1125')
            print(2)
        if len(data) == 0:
            data = 'Нет результата'.encode('cp1125')
            print(3)
        self.conn.send(data)


if __name__ == '__main__':
    start = Start()
    start.run()
    print('Super run...')
