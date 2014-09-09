from ant_object import AntObject
from PySide.QtGui import QPixmap


class AntObjectAnimation(AntObject):
    def __init__(self):
        super(AntObjectAnimation, self).__init__()
        self.__animated = True
        self.__frames = list()
        self.__displayed_frame_index = None

    def isAnimated(self):
        return self.__animated

    def getNumberOfFrames(self):
        return len(self.__frames)

    def addFrame(self, path_to_picture, number_of_frame_clones=1):
        for x in range(number_of_frame_clones):
            self.__frames.append(QPixmap())
            if not self.__frames[-1].load(path_to_picture):
                raise Exception("AntObjectAnimation.addFrame: wrong path_to_picture")

        if self.__displayed_frame_index is None:
            self.__displayed_frame_index = 0
            self.__setFrame__()

    def __setFrame__(self):
        self.picture = self.__frames[self.__displayed_frame_index]

    def setNextFrame(self):
        if self.getNumberOfFrames() == 0:
            raise Exception("There aren't any frame")

        self.__displayed_frame_index += 1
        self.__displayed_frame_index %= self.getNumberOfFrames()

        self.__setFrame__()

    def setPreviousFrame(self):
        if self.getNumberOfFrames() == 0:
            raise Exception("There aren't any frame")

        self.__displayed_frame_index -= 1
        if self.__displayed_frame_index == -1:
            self.__displayed_frame_index = self.getNumberOfFrames() - 1

        self.__setFrame__()
