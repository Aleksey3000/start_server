import socket
from requests import get
from smtplib import SMTP
from email.mime.text import MIMEText
import psutil
import platform
from datetime import datetime
import sys


def send_massage(theme, mes, client):
    sender = 'youth_house@mail.ru'
    password = '4VrnG2yX610Z3erT7Dzz'
    mes = MIMEText(mes)
    mes['Subject'] = theme  # ТЕМА
    server = SMTP('smtp.mail.ru', 587)
    server.starttls()
    try:
        server.login(sender, password)
        server.sendmail(sender, client, mes.as_string())
        print('ALL RIGHT')
    except Exception as ex:
        print(f"ERROR: {ex}")


def get_ip():
    host = socket.gethostname()
    local_ip = socket.gethostbyname(host)
    public_ip = get('http://api.ipify.org').text

    return {'public': public_ip, 'local': local_ip}


def get_info_ip(ip):
    try:
        response = get(url=f'http://ip-api.com/json/{ip}').json()
        return response
    except Exception as ex:
        print('Check connection or ip', ex)


def get_size(b, suffix='B'):
    factor = 1024
    for unit in ('', 'K', 'M', 'G', 'T', 'P'):
        if b < factor:
            return f'{b:.2f}{unit}{suffix}'
        b /= factor


def get_info_pc():
    info = ""
    uname = platform.uname()
    info += f"общая онформация о пк \n{'-' * 7}\n" \
            f" \nСистема- {uname.system}\nИмя узла- {uname.node}\nВыпуск- {uname.release}\n" \
            f"Версия- {uname.version}\nМашина- {uname.machine}\nПроцессор- {uname.processor}\n{'-' * 7}\n"

    cpufreq = psutil.cpu_freq()
    info += f"Информация о процессоре\n{'-' * 7}\n" \
            f"физ. ядра- {psutil.cpu_count(logical=False)}\nВсего ядер- {psutil.cpu_count(logical=True)}\n" \
            f"max частота- {cpufreq.max:.2f}МГц\n" \
            f"min частота- {cpufreq.min:.2f}МГц\n" \
            f"Текущая частота- {cpufreq.current:.2f}МГц\n{'-' * 7}\n"

    svmem = psutil.virtual_memory()
    info += f"Информация о памяти\n{'-' * 7}\n" \
            f"Объём- {get_size(svmem.total)}\n" \
            f"Свободно- {get_size(svmem.available)}\n" \
            f"Используется- {get_size(svmem.used)}\n{'-' * 7}\n"

    info += f"Информация о диске\n{'-' * 7}\n"
    partitions = psutil.disk_partitions()
    for partition in partitions:
        info += f"=== Диск: {partition.device} ====\n" \
                f"  Тип файловой системы: {partition.fstype}"
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        info += f"  Объём: {get_size(partition_usage.total)}\n" \
                f"  Используется: {get_size(partition_usage.used)}\n" \
                f"  Свободно: {get_size(partition_usage.free)}\n"


    return info


def connection():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = str(get_ip()['local'])
    print(ip)
    server.bind((ip, 12345))
    server.listen()

    while True:
        user, adres = server.accept()

        data = user.recv(1024)
        print(data.decode('utf-8'))

def main():
    print(datetime.now())
    '''ip = get_ip()
    print(f'ip: {ip}')
    info = get_info_ip(ip['public'])
    print(info)
    print(get_info_pc())
    # send_massage("ip_info", f"loc: {ip['local']}\npub: {ip['public']}\nInfo: {info}", "akuzmin340@gmail.com")
    '''
    connection()


if __name__ == '__main__':
    main()
