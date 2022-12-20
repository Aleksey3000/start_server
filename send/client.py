from socket import socket, AF_INET, SOCK_STREAM
from colorama import Fore
from os import walk, listdir
import sys
import os


class SendProject:
    def __init__(self, client=None):
        self.project = None
        self.PATH = r'C:\\Users\\79212\\PycharmProjects\\'
        if client is not None:
            self.client = client
        else:
            self.client = socket(AF_INET, SOCK_STREAM)
            hosts = ('192.168.0.102', 'supersite.ddnsking.com')
            port = 5008
            self.ignore = []
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
        projects = self.client.recv(1024).decode('utf-8').split('|')
        print(projects)
        branch = input('>>>')
        if branch.split()[0] == 'save':
            self.client.send(branch.encode('utf-8'))
            self.receive_zip(fr'C:\Users\79212\AppData\Roaming\SRV', branch.split()[1])
            print(f'File {branch.split()[1]}.zip saved')
            sys.exit()

        self.client.send(branch.encode('utf-8'))
        print(listdir(self.PATH))
        self.project = input('>>>')
        self.PATH += self.project
        with open(self.PATH + '\\ignore', 'r', encoding='utf-8') as ignore:
            self.ignore = ignore.read().split()
        print(self.PATH)
        print(self.ignore)
        f_req = '0'
        file_names = self.get_file_names(self.project)
        data = '|'.join(file_names).encode('utf-8')
        self.client.send(str(len(data)).encode('utf-8'))
        self.client.recv(1)
        self.client.send(data)
        self.client.recv(1)
        for file_name in file_names:
            print('to send', file_name)
            self.send_file(file_name)
            if 'requirements.txt' in file_name:
                f_req = '1'
            print('Send file', file_name)

        if int(f_req):
            f_req = input('install packages? 1 or 0>')
        self.client.send(f_req.encode('utf-8'))

        data = self.client.recv(1024)
        while data:
            print(data.decode('cp1125'))
            data = self.client.recv(1024)
        print(Fore.GREEN, 'OK')

    def get_file_names(self, project):
        files = []
        for (path, dir, file_names) in walk(r'C:\\Users\\79212\\PycharmProjects\\' + project):
            f = True
            for i in self.ignore:
                if i in path:
                    f = False
                    break
            if f:
                for filename in file_names:
                    filename = filename.replace('\\', '\\\\')
                    files.append(path[path.find(self.project) + len(self.project):] + '\\\\' + filename)

        return files

    def send_file(self, file_name):
        with open(self.PATH + file_name, 'rb') as file:
            data = file.read()
        size = str(len(data))
        self.client.send(size.encode('utf-8'))
        d = self.client.recv(1)
        print(d)
        self.client.send(data)
        self.client.recv(1)

    def receive_zip(self, dir, name):
        if not os.path.exists(dir):
            os.makedirs(dir)

        full_size = int(self.client.recv(1024).decode('utf-8'))
        self.client.send(b' ')
        size = 0
        with open(fr'{dir}\{name}.zip', 'wb') as file:
            while size < full_size:
                data = self.client.recv(1024)
                size += len(data)
                file.write(data)


if __name__ == '__main__':
    send_prj = SendProject()
    send_prj.run()
