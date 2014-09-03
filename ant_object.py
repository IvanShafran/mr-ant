from PySide.QtGui import QPixmap
from PySide.QtCore import QPoint


class AntObject():
    def __init__(self, point=QPoint(0, 0)):
        self.picture = QPixmap()
        self.point = point
        self.enabled = True

    def width(self):
        return self.picture.width()

    def height(self):
        return self.picture.height()

    def __eq__(self, other):
        return self.point == other.point and self.width() == other.width() and self.height() == other.height()
