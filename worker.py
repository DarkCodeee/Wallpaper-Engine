import os
import threading
import time

import win32api, win32gui, win32con


class WorkerW:
    def __init__(self):
        #Дескриптор окна
        self.workerw = None

    #Получение дескриптора окна
    def Callback(self, hwnd, hwnds):
        btnhdl = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", '')

        if btnhdl != 0:
            self.workerw = win32gui.FindWindowEx(0, hwnd, "WorkerW", '')

            return self.workerw

    #Создание окна
    def Create_window(self):
        program = win32gui.FindWindow("Progman", None)
        #Создания окна workerw (если оно есть, то ничего не происходит)
        win32gui.SendMessageTimeout(program, 0x052C, 0, 0, win32con.SMTO_NORMAL, 1000)
        win32gui.EnumWindows(self.Callback, None)

    #Установить родителя workerw
    def Set_parent(self, hwnd):
        win32gui.SetParent(hwnd, self.workerw)