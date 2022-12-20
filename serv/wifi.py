import subprocess


def main():
    data = subprocess.check_output('netsh lan show profiles').decode('utf-8').split('\n')
    print(data)


if __name__ == '__main__':
    main()
