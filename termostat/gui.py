import sys

from qtmodern import styles

from PyQt6.QtWidgets import QPushButton, QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Termostat")
        self.setAutoFillBackground(True)

        button = QPushButton("Click me!")
        self.setCentralWidget(button)

        self.setMinimumSize(800, 600)


def main():
    app = QApplication(sys.argv)

    styles.dark(app)

    window = MainWindow()
    window.show()

    app.exec()
