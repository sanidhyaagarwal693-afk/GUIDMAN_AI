from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QTimer
from animator import Animator
from sidebar import Sidebar


class OverlayWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedSize(180, 220)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 180, 220)

        self.animator = Animator(self.label)
        self.animator.play("idle")

        self.sidebar = Sidebar(self)

        self.move(400, 500)

        self.old_pos = None

    # WALKING MOVEMENT
    def walk_to(self, x, y):

        self.animator.play("walking")

        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(900)
        self.anim.setEndValue(QPoint(x - 90, y - 140))
        self.anim.start()

    # GUIDE RUNNER
    def run_guide(self, steps):

        delay = 0

        for step in steps:

            x = step["x"]
            y = step["y"]

            QTimer.singleShot(delay, lambda x=x, y=y: self.walk_to(x, y))
            delay += 1200

            QTimer.singleShot(delay, lambda: self.animator.play("pointing"))
            delay += 1600

        QTimer.singleShot(delay, lambda: self.animator.play("idle"))

    # LEFT CLICK = OPEN SIDEBAR
    # RIGHT CLICK = DRAG STICKMAN
    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            if self.sidebar.isVisible():
                self.sidebar.hide()
                self.animator.play("idle")
            else:
                self.sidebar.show()

        if event.button() == Qt.RightButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):

        if self.old_pos and event.buttons() == Qt.RightButton:

            delta = event.globalPos() - self.old_pos

            self.move(self.x() + delta.x(), self.y() + delta.y())

            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None