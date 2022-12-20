import psutil
from time import sleep

import pyautogui
import keyboard

stopKey = "s"  # The stopKey is the button to press to stop. you can also do a shortcut like ctrl+s
maxX, maxY = pyautogui.size()  # get max size of screen
while True:
    if keyboard.is_pressed(stopKey):
        pyautogui.press('escape')
    else:
        'pyautogui.moveTo(maxX/2, maxY/2) #move the mouse to the center of the screen'
sleep(10000)
exit()


tsk = {'taskmgr.exe', 'cmd.exe', 'powershell.exe'}
while True:
    for proc in psutil.process_iter():
        if proc.name().lower() in tsk:
            proc.terminate()

