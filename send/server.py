import os
import traceback
from socket import socket, AF_INET, SOCK_STREAM
from colorama import Fore
from subprocess import Popen, PIPE
import shutil


class SendProject:
    def __init__(self, conn=None):
        self.PATH = 'C:\\Users\\akuzm\\PycharmProjects\\'
        self.projects = os.listdir(self.PATH)
        if conn is not None:
            self.conn = conn
        else:
            self.server = socket(AF_INET, SOCK_STREAM)
            self.server.bind(('', 5008))
            self.server.listen()
            self.conn, addr = self.server.accept()
            print('Connected to', conn, addr)

    def run(self):
        try:
            with self.conn:
                print(Fore.GREEN, 'Connection: ', str(self.conn), end='')
                print(Fore.RESET)
                self.conn.send('|'.join(self.projects).encode('utf-8'))
                otv = self.conn.recv(1024).decode('utf-8')
                if otv.split()[0] == 'new':
                    self.PATH += otv.split()[1]
                    os.makedirs(self.PATH)
                elif otv.split()[0] == 'save':
                    self.send_zip(otv.split()[1])
                    raise Exception
                else:
                    self.PATH += otv
                files = self.conn.recv(1024).decode('utf-8').split('|')

                for file_name in files:
                    file = self.receive_file()
                    self.save_file(file, file_name)
                    print(f'Save file - {file_name}\n---------------------------')
                f_req = self.conn.recv(1024).decode('utf-8')
                if int(f_req):
                    data = self.create_venv()
                else:
                    data = 'Packages not installed'.encode('cp1125')
                self.conn.sendall(data)
                print(Fore.GREEN, 'OK')

        except Exception as ex:
            print(Fore.RED, traceback.format_exc(), ex, Fore.RESET)

    def receive_file(self):
        full_size = self.conn.recv(1024).decode('utf-8')
        self.conn.send(b' ')
        print(Fore.BLUE, full_size, Fore.RESET)
        full_size = int(full_size)
        size = 0
        file = b''
        while size < full_size:
            data = self.conn.recv(1024)
            size += len(data)
            file += data
        self.conn.send(b' ')
        return file

    def send_zip(self, branch):
        print('start create zip and send')
        path = 'D:\\server\\zip\\' + branch
        shutil.make_archive(path, 'zip', self.PATH + branch)
        print('zip created')
        size = os.path.getsize(path + '.zip')
        self.conn.send(str(size).encode('utf-8'))
        self.conn.recv(1)
        with open(path + '.zip', 'rb') as file:
            self.conn.sendall(file.read())
        os.remove(path + '.zip')
        print('OK')

    def save_file(self, data, file_name):
        s = file_name.split('\\\\')
        path = self.PATH + '\\\\'.join(s[:-1])
        print(path, 'path')

        if not os.path.exists(path):
            os.makedirs(path)

        with open(self.PATH + '\\' + file_name, 'wb') as file:
            file.write(data)

    def create_venv(self):
        command = f'cd {self.PATH}\npip install -r requirements.txt\npip list\n'
        process = Popen("powershell.exe", shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=False)
        d1, d2 = process.communicate(command.encode('cp1125'))
        print('ok')
        return d1 + d2


if __name__ == '__main__':
    server = SendProject()
    # server.PATH = server.PATH + 'super'
    # print(server.create_venv().decode('cp1125'))
    server.run()
    server.conn.close()
