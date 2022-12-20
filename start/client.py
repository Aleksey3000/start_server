import socket
import os
from sys import exit as sys_exit
from colorama import Fore
from send.client import SendProject


class Start:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hosts = ('192.168.0.102', 'supersite.ddnsking.com')
        port = 5008
        for host in hosts:
            try:
                print(f'\rConnecting to {host}:{port}', end='')
                self.client.connect((host, port))
                print(Fore.GREEN, '\nПодключено')
                self.send_project = SendProject(client=self.client)
                return
            except Exception as ex:
                print(Fore.RED, f'\rFailed to connect to {host} {ex}')

        raise ConnectionError

    def run(self):

        try:
            while True:
                command = input('>>>')

                if command == 'cmd':
                    self.cmd(command)
                    continue

                data = command.encode('cp1125')
                self.client.send(data)
                if command == 'stop':
                    data = self.client.recv(1024)
                    print(data.decode('cp1125'))
                    continue
                elif command == 'start':
                    data = self.client.recv(1024)
                    print(data.decode('cp1125'))
                    continue
                elif command == 'exit':
                    self.client.close()
                    sys_exit(1)
                elif command == 'send':
                    print('--- send project ---')
                    self.send_project.run()
                    print('--- stop send project ---')

                elif len(command.split()) > 1:
                    print(command)
                    f = command.split()[0]
                    command = command[len(f) + 1:]

                    if f == 'file':
                        print('Start send file')
                        # VID_20221105_153542.mp4
                        with open(r'to_load\\' + command, 'rb') as file:
                            file_size = os.path.getsize(r'to_load\\' + command)
                            print(file_size)
                            self.client.send(str(file_size).encode('cp1125'))
                            self.client.recv(1)
                            send_size = 0
                            data = ''
                            while data != b'':
                                data = file.read(1024)
                                self.client.send(data)
                                send_size += len(data)
                                print(f'\rSend: {round(100 / (file_size / send_size), 2)} %', end='')
                            print(self.client.recv(1024).decode('cp1125'))
                    elif f == 'del':
                        data = self.client.recv(1024)
                        print(data.decode('cp1125'))

        except Exception as ex:
            self.client.close()
            print('Ошибка в обработке данных:\n', ex)
        finally:
            self.client.close()
            print('Подключение завершено\n')

    def cmd(self, command):
        print('^^^CMD^^^')
        commands = command + ' '
        command = input('cmd>')
        while command != 'close':
            commands += command + '\n'
            command = input('cmd>')
        print(commands)
        self.client.send(commands.encode('cp1125'))

        full_size = int(self.client.recv(1024).decode('cp1125'))
        receive_size = 0
        output = ''
        while receive_size < full_size:
            data = self.client.recv(1024)
            output += data.decode('cp1125')
            receive_size += len(data)
            print(len(data))
        print(output)

        if 'tree' in command:
            # cmd tree /f
            with open('cmd_tree.txt', 'w', encoding='utf-8') as file:
                file.write(output)


if __name__ == '__main__':
    client = Start()
    client.run()

    '''#commands = ['tree', '/f', 'C:/Users/79212/PycharmProjects/myserver/']
    commands = ''
    command = input('>>>')
    while command != 'break':
        commands += command + '\n'
        command = input('>>>')

    from subprocess import Popen, PIPE
    commands = 
    ipconfig /all
    tree /f
    

    process = Popen("cmd.exe", shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=False)
    out, err = process.communicate(commands.encode('cp1125'))
    print(out.decode('cp1125'))'''
