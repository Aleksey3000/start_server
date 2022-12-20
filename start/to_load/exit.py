from threading import Thread
import os
from time import sleep

RUN = r'C:\Users\79212\PycharmProjects\project\start\run'

def exiting(name: str, time: int =3) -> None:
    def thread():
        while True:
            with open(RUN, 'r', encoding='utf-8') as file:
                for project in file.read().split('\n'):
                    try:
                        key, val = project.split(' - ')

                        if key == name and not int(val):
                            print('Process exiting start and run reloader.')
                            os._exit(1)
                    except ValueError:
                        pass
            sleep(time)


    thread = Thread(target=thread)
    thread.start()
