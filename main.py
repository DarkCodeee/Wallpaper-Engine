from display import *
from gui import *
import multiprocessing as mp
from multiprocessing.sharedctypes import Array
import time


if __name__ == "__main__":
    wallpaper = Array("c", bytes("x"*100000, "UTF-8"))
    speed = mp.Value('i', 60)
    pause = mp.Value('i', 0)

    mp.Process(target=create_class_Display, args=(wallpaper, speed, pause), daemon=True, name="display").start()

    create_class_gui("main.ui", wallpaper, speed, pause)
    #mp.Process(target=create_class_gui, args=("main.ui", wallpaper, speed, pause)).start()

    #num.value = bytes("3.mp4", "UTF-8")