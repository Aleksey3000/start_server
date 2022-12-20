import socket


def connection():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(('www.youtube.com', 443))
    print('ok')
    while True:
        client.send('POST 1024'.encode('utf-8'))
        print('ok')
        data = client.recv(1024).decode('utf-8')
        print(data, len(data))

def main():
    connection()


if __name__ == '__main__':
    main()
