from PySide.QtGui import QPushButton, QMainWindow
from game_run_to_anthill import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        btn = QPushButton(self)
        QObject.connect(btn, SIGNAL('clicked()'), self.startRunToAnthill)
        btn.setText('Start')

        self.setGeometry(200, 200, 500, 300)
        self.setWindowTitle('Mr Ant')
        self.show()

    def startRunToAnthill(self):
        self.game = GameRunToAnthill()
        self.game.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
