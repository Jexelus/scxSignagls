from pynput.keyboard import Key, Controller
from threading import Thread
import time
import random
import pyautogui

class KBMan:
    def __init__(self):
        self.kb = Controller()

    def press_x(self):
        pyautogui.press('x')

