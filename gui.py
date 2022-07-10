import sys
import os
import PyQt5
import cv2
import math
from PyQt5 import QtWidgets, QtGui, uic, QtCore


class Window(QtWidgets.QMainWindow):
    def __init__(self, settings, wallpaper, speed, pause):
        super(Window, self).__init__()

        uic.loadUi(settings, self)

        self.wallpaper = wallpaper
        self.speed = speed
        self.pause = pause

        self.icons = []

        self.initial_settings()

        self.create_table()

        self.speed_input.setValidator(QtGui.QIntValidator(0, 1000, self))
        self.update_button.clicked.connect(self.create_table)
        self.set_wallpaper_button.clicked.connect(self.set_wallpaper)

        self.button_pause.clicked.connect(self.set_pause)
        self.button_start.clicked.connect(self.set_start)

        self.show()


    def initial_settings(self):
        self.setWindowTitle('Wallpaper engine')
        self.setWindowIcon(QtGui.QIcon('WL.ico'))

        self.table.clear()
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()

        self.size = [218, 180]

    def cellClick(self, row, col):
        #self.row = row
        #self.col = col
        self.selest_item = row * self.row + col

        self.update_info()

    def set_wallpaper(self):
        #print(bytes(os.listdir(os.getcwd() + "\\data\\wallpapers\\")[self.selest_item], "UTF-8"))
        #print(os.listdir(os.getcwd() + "\\data\\wallpapers\\")[self.selest_item])
        self.wallpaper.value = bytes(os.listdir(os.getcwd() + "\\data\\wallpapers\\")[self.selest_item], "UTF-8")
        self.speed.value = int(self.speed_input.text())

    def set_start(self):
        self.pause.value = 0

    def set_pause(self):
        self.pause.value = 1

    def update_info(self):
        try:
            cur_dir = os.getcwd() + "\\data\\wallpapers\\"
            files = os.listdir(cur_dir)

            if files[self.selest_item].split('.')[-1] in ["jpg", "png", "jpeg"]:
                self.name_input.setText(files[self.selest_item].split(".")[0])
                self.type_input.setText("picture")
                self.speed_input.setText(str(60))

                _size = QtCore.QSize(332, 252)
                pixmap = self.icons[self.selest_item]
                self.image.setPixmap(pixmap.scaled(_size))

            elif files[self.selest_item].split('.')[-1] in ["mp4", "webm"]:
                self.name_input.setText(files[self.selest_item].split(".")[0])
                self.type_input.setText("video")
                self.speed_input.setText(str(60))

                cam = cv2.VideoCapture(f"{cur_dir}{files[self.selest_item]}")
                cam.set(cv2.CAP_PROP_POS_FRAMES, int(cam.get(cv2.CAP_PROP_FRAME_COUNT)) // 2)
                ret, frame = cam.read()
                pixmap = self.icons[self.selest_item]
                _size = QtCore.QSize(332, 252)
                self.image.setPixmap(pixmap.scaled(_size))
        except Exception as e:
            print(e)

    def convert_nparray_to_QPixmap(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img.shape
        qimg = QtGui.QImage(img.data, w, h, 3 * w, QtGui.QImage.Format_RGB888)
        qpixmap = QtGui.QPixmap(qimg)

        return qpixmap

    def create_table(self):
        self.row = 4
        self.column = 4

        self.icons = []

        self.table.clear()

        self.table.horizontalHeader().setDefaultSectionSize(self.size[0])
        self.table.verticalHeader().setDefaultSectionSize(self.size[1])

        row = column = 0

        cur_dir = os.getcwd()
        files = os.listdir(path=f"{cur_dir}\\data\\wallpapers\\")

        self.table.setRowCount(math.ceil(len(files) / self.row))
        for i in range(len(files)):
            try:
                label = QtWidgets.QLabel()
                if files[i].split('.')[-1] in ["jpg", "png", "jpeg"]:
                    pixmap = QtGui.QPixmap(f"{cur_dir}\\data\\wallpapers\\{files[i]}")
                    self.icons.append(pixmap)

                    label = QtWidgets.QLabel()
                    _size = QtCore.QSize(self.size[0], self.size[-1])
                    label.setPixmap(pixmap.scaled(_size))

                    if row >= self.row:
                        column += 1
                        row = 0
                    self.table.setCellWidget(column, row, label)
                    row += 1
                elif files[i].split('.')[-1] in ["mp4", "webm"]:
                    path = os.getcwd()
                    name = files[i].split(".")[0]
                    cam = cv2.VideoCapture(f"{path}\\data\\wallpapers\\{files[i]}")
                    cam.set(cv2.CAP_PROP_POS_FRAMES, int(cam.get(cv2.CAP_PROP_FRAME_COUNT)) // 2)
                    ret, frame = cam.read()
                    pixmap = QtGui.QPixmap(self.convert_nparray_to_QPixmap(frame))
                    self.icons.append(pixmap)
                    #cv2.imwrite(f"{path}\\data\\wallpapers\\{name}_icon.jpg", frame)

                    label = QtWidgets.QLabel()
                    _size = QtCore.QSize(self.size[0], self.size[-1])
                    label.setPixmap(pixmap.scaled(_size))

                    if row >= self.row:
                        column += 1
                        row = 0
                    self.table.setCellWidget(column, row, label)
                    row += 1
            except Exception as e:
                print(e)

        self.table.setMouseTracking(True)
        self.table.cellClicked.connect(self.cellClick)


def create_class_gui(settings_file, wallpaper, speed, pause):
    app = QtWidgets.QApplication(sys.argv)
    gui = Window(settings_file, wallpaper, speed, pause)
    sys.exit(app.exec())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window("main.ui", 0)
    sys.exit(app.exec())