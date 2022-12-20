from psutil import process_iter
from subprocess import call

print('b')

while True:
    process = map(lambda x: x.name(), process_iter())
    if 'a.exe' not in process:
        call(r'a.exe')
    if 'main.exe' not in process:
        call(r'main.exe')
