from PyQt5.QtWidgets import (
    QWidget,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication
from guide_engine import GuideEngine


class Sidebar(QWidget):

    def __init__(self, overlay):
        super().__init__()

        self.overlay = overlay
        self.engine = GuideEngine()

        self.processing = False

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setFixedSize(360, 800)

        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 360, 0)

        layout = QVBoxLayout()

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask Guidman...")

        self.send_btn = QPushButton("Send")

        bottom = QHBoxLayout()
        bottom.addWidget(self.input)
        bottom.addWidget(self.send_btn)

        layout.addWidget(self.chat, 8)
        layout.addLayout(bottom, 2)

        self.setLayout(layout)

        self.send_btn.clicked.connect(self.handle)
        self.input.returnPressed.connect(self.handle)
        self.input.textChanged.connect(self.thinking)

        self.old_pos = None

    # THINKING ANIMATION
    def thinking(self):

        if not self.processing:
            self.overlay.animator.play("thinking")

    # HANDLE COMMAND
    def handle(self):

        text = self.input.text().lower()

        if not text:
            return

        self.processing = True

        self.chat.append("You: " + text)

        # LAUGH COMMAND
        if "laugh" in text:

            self.chat.append("Guidman: Haha 😄")

            self.overlay.animator.play("laughing")

            QTimer.singleShot(3000, self.finish_command)

            self.input.clear()
            return

        # DANCE COMMAND
        if "dance" in text:

            self.chat.append("Guidman: Let's dance 💃")

            self.overlay.animator.play("dancing")

            QTimer.singleShot(4000, self.finish_command)

            self.input.clear()
            return

        # CELEBRATE COMMAND
        if "celebrate" in text or "success" in text:

            self.chat.append("Guidman: 🎉 Celebration time!")

            self.overlay.animator.play("celebrating")

            QTimer.singleShot(4000, self.finish_command)

            self.input.clear()
            return

        guide = self.engine.find(text)

        if guide:

            self.chat.append("Guidman: Follow these steps")

            steps = self.engine.load(guide)

            self.overlay.run_guide(steps)

            for step in steps:
                self.chat.append("Step: " + step["text"])

            QTimer.singleShot(4000, self.finish_command)

        else:

            self.chat.append("Guidman: I don't know this command yet.")

            self.finish_command()

        self.input.clear()

    # FINISH COMMAND
    def finish_command(self):

        self.processing = False
        self.overlay.animator.play("idle")

    # DRAG SIDEBAR
    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):

        if self.old_pos is None:
            return

        delta = event.globalPos() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())

        self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None