from psutil import process_iter
from subprocess import call

print('a')

while True:
    process = map(lambda x: x.name(), process_iter())
    if 'b.exe' not in process:
        call(r'b.exe')
    if 'main.exe' not in process:
        call(r'main.exe')

