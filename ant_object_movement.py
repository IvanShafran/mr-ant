from PySide.QtCore import Qt
from ant_object import AntObject


class AntObjectMovement(AntObject):
    def __init__(self):
        super(AntObjectMovement, self).__init__()
        self.__last_step_direction = None
        self.__last_step_value = None
        self.step_value = 2

    def __move__(self, doStep, coordinate, direction, step_value):
        if direction == 'up' or direction == 'left':
            doStep(coordinate - step_value)
        else:
            doStep(coordinate + step_value)

        self.__last_step_direction = direction
        self.__last_step_value = step_value

    def up(self, step_value):
        self.__move__(self.point.setY, self.point.y(), 'up', step_value)

    def down(self, step_value):
        self.__move__(self.point.setY, self.point.y(), 'down', step_value)

    def left(self, step_value):
        self.__move__(self.point.setX, self.point.x(), 'left', step_value)

    def right(self, step_value):
        self.__move__(self.point.setX, self.point.x(), 'right', step_value)

    def cancelLastStep(self):
        if 'up' == self.__last_step_direction:
            self.down(self.__last_step_value)
        elif 'down' == self.__last_step_direction:
            self.up(self.__last_step_value)
        elif 'left' == self.__last_step_direction:
            self.right(self.__last_step_value)
        elif 'right' == self.__last_step_direction:
            self.left(self.__last_step_value)

        self.__last_step_direction = None


class AntObjectUserMovement(AntObjectMovement):
    def __init__(self):
        super(AntObjectUserMovement, self).__init__()

        self.key_up = Qt.Key_W
        self.key_down = Qt.Key_S
        self.key_left = Qt.Key_A
        self.key_right = Qt.Key_D
