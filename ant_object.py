from PySide.QtGui import QPixmap
from PySide.QtCore import QPoint


class AntObject():
    def __init__(self, point=QPoint(0, 0)):
        self.picture = QPixmap()
        self.point = point
        self.__animated = False
        self.__enabled = True

    def isAnimated(self):
        return self.__animated

    def isEnabled(self):
        return self.__enabled

    def setEnabled(self, enabled=True):
        self.__enabled = enabled

    def width(self):
        return self.picture.width()

    def height(self):
        return self.picture.height()

    def __eq__(self, other):
        return self.point == other.point and self.width() == other.width() and self.height() == other.height()
