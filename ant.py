from PySide.QtGui import QPixmap
from ant_motion import AntMotion


class Ant():
    def __init__(self, name):
        self.picture = QPixmap()
        self.motion = AntMotion()
        self.name = name
        self.zombie = False

    def width(self):
        return self.picture.width()

    def height(self):
        return self.picture.height()
