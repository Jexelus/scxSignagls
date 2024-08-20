from threading import Thread
from classes.kbman import KBMan
import time
from pynput import keyboard
from classes.screenReader import ScreenReader
import os
import pyautogui
class Listener(Thread):
    def __init__(self, main_thread):
        super().__init__()
        self.main = main_thread

    def on_press(self, key):
        try:
            print(f'Нажата алфавитно-цифровая клавиша: {key.char}')
        except AttributeError:
            print(f'Нажата специальная клавиша: {key}')
        if key == keyboard.Key.f7:
            print('Нажата клавиша F7 -> переключение состояния')
            exit()

    def on_release(self, key):
        print(f'Клавиша отпущена: {key}')
        
    def run(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


class Main(Thread):
    def __init__(self):
        super().__init__()
        self.is_active = True
        self.kb = KBMan()
        self.sr = ScreenReader(height=1080, width=1920)

    def Check_CAK(self):
        self.kb.press_x()
        time.sleep(0.3)
        t1 = time.time()
        if self.sr.recognize():
            print('SIGNAL!!!')
            # os.remove('./trash/CAK_SIGNALFOUND_POLYGON.png')
            time.sleep(0.20)
            dur = 0.08
            time.sleep(dur)
            pyautogui.mouseDown(1070, 810)
            time.sleep(dur)
            pyautogui.mouseUp(1070, 810)
            time.sleep(dur)
            pyautogui.mouseDown(1350, 800)
            time.sleep(dur)
            pyautogui.mouseUp(1350, 800)
            time.sleep(10.6)
            pyautogui.mouseDown(1350, 800)
            time.sleep(dur)
            pyautogui.mouseUp(1350, 800)
            time.sleep(dur)
            pyautogui.mouseDown(630, 600)
            time.sleep(dur)
            pyautogui.mouseUp(630, 600)

            os.kill(os.getpid(), 9)
        else:
            print('No SIGNAL')
        t2 = time.time()
        print(f"t2 - t1 = {t2 - t1}")
        self.kb.press_x()

    def run(self):
        while True:
            if self.is_active:
                self.Check_CAK()
            time.sleep(0.3)
            print('is_active = ', self.is_active)



if '__main__' == __name__:
    time.sleep(5)
    main = Main()
    # listener = Listener(main)
    # listener.start()
    main.start()