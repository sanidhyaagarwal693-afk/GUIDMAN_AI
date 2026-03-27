import sys
from PyQt5.QtWidgets import QApplication
from overlay import OverlayWindow

def main():
    app = QApplication(sys.argv)

    window = OverlayWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()