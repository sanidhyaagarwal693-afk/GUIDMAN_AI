import os
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap

class Animator:

    def __init__(self,label):

        self.label=label
        self.timer=QTimer()
        self.timer.timeout.connect(self.next_frame)

        self.frames=[]
        self.index=0

    def play(self,animation):

        folder=f"assets/{animation}"

        self.frames=[]
        self.index=0
        print("Loading animation:", folder)
        for file in sorted(os.listdir(folder)):

            if file.endswith(".png"):

                path=os.path.join(folder,file)

                pix=QPixmap(path).scaled(150,200)

                self.frames.append(pix)

        self.timer.start(250)

    def next_frame(self):

        if not self.frames:
            return

        self.label.setPixmap(self.frames[self.index])
        self.index=(self.index+1)%len(self.frames)