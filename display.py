import pygame as pg
import cv2

from worker import *

pg.init()

class Display:
    def __init__(self, path_file, speed, pause):
        self.path_file = path_file

        self.speed = speed
        self.pause = pause

        self.draw = {
            "path": b'',
            "type": '',
            "speed": 0}

        self.image = None
        self.video = None
        self.create_display()
        self.cycle_display()

    def create_worker(self):
        self.worker = WorkerW()
        self.worker.Create_window()
        self.worker.Set_parent(self.hwnd)

    def create_display(self):
        flags = pg.FULLSCREEN | pg.DOUBLEBUF
        width, height = pg.display.Info().current_w, pg.display.Info().current_h
        self.display = pg.display.set_mode([width, height], flags, 16)

        pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])

        self.surface = pg.Surface([width, height])

        self.hwnd = pg.display.get_wm_info()["window"]

        self.create_worker()


    def check_file(self):
        self.draw["path"] = self.path_file.value
        imageToCheck = ('.png', '.jpg', '.jpeg')
        video = (".mp4")

        if self.draw["path"].decode("UTF-8").lower().endswith(imageToCheck):
            self.image = pg.image.load("data/wallpapers/"+self.draw["path"].decode("UTF-8"))
            self.surface = pg.Surface([self.image.get_width(), self.image.get_height()])
            self.draw["type"] = "image"
            self.video = None
        elif self.draw["path"].decode("UTF-8").lower().endswith(video):
            self.image = None
            self.draw["type"] = "video"
            self.video = cv2.VideoCapture("data/wallpapers/"+self.draw["path"].decode("UTF-8"))
            self.surface = pg.Surface([self.video.get(cv2.CAP_PROP_FRAME_WIDTH), self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)])



    def cycle_display(self):

        self.run = True
        self.timer = pg.time.Clock()

        while self.run:
            try:
                self.timer.tick(self.speed.value)
                print(self.timer.get_fps(), self.speed.value)
                pg.display.set_caption(str(self.timer.get_fps()))
                #self.surface.fill((0,0,0))

                if self.path_file.value != self.draw["path"]:
                    self.check_file()

                for i in pg.event.get():
                    if i.type == pg.QUIT:
                        self.run = False
                if not self.pause.value:
                    #print("Run")
                    try:
                        if self.image:
                            self.surface.blit(self.image, self.image.get_rect())
                        elif self.video:
                            if self.video.get(cv2.CAP_PROP_POS_FRAMES) >= self.video.get(cv2.CAP_PROP_FRAME_COUNT) - 2:
                                self.video = cv2.VideoCapture("data/wallpapers/"+self.draw["path"].decode("UTF-8"))
                            frame, img = self.video.read()
                            if frame:
                                self.surface.blit(pg.image.frombuffer(img.tobytes(), img.shape[1::-1], "BGR"), (0, 0))
                            #print(self.video.get(cv2.CAP_PROP_POS_FRAMES))
                    except Exception as e:
                        print(e)
                        self.check_file()

                surface = pg.transform.scale(self.surface, [self.display.get_width(), self.display.get_height()])
                self.display.blit(surface, surface.get_rect())

                pg.display.flip()
            except Exception as e:
                print(e)

        pg.quit()


def create_class_Display(path_file, speed, pause):
    display = Display(path_file, speed, pause)


