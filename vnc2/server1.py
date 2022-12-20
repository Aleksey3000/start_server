import socket
from requests import get


def connection():
    ip = socket.gethostbyname_ex(socket.gethostname())
    print(ip)
    # print(ip[-1][-1])
    ip = '2C-F0-5D-A8-7B-12'
    ip = get('http://api.ipify.org').text
    print(ip)
    ip = '192.168.1.100'
    print(1)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(2)
    server.bind((str(ip), 49880))
    print(3)
    server.listen()
    conn, addr = server.accept()

    print('Connected with', conn)
    while True:
        data = conn.recv(1024).decode('utf-8')
        print('>>>' + data)


if __name__ == '__main__':
    connection()
