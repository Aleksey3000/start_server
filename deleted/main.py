from psutil import process_iter
import os
import signal
from subprocess import call

process = map(lambda x: x.name(), process_iter())

if 'b.exe' not in process:
    call(r'b.exe')
if 'a.exe' not in process:
    call(r'a.exe')


def delete(process):
    for i in process:
        try:
            os.kill(i, signal.SIGINT)
        except Exception as exp:
            print(exp, 'ex', i)


