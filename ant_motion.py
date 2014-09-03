from PySide.QtCore import QPoint, Qt


class AntMotion():
    def __init__(self):
        self.point = QPoint(0, 0)
        self.step_value = 2  # pixels
        self.last_step_direction = None
        self.last_step_value = None
        self.key_up = Qt.Key_W
        self.key_down = Qt.Key_S
        self.key_left = Qt.Key_A
        self.key_right = Qt.Key_D

    def _move(self, doStep, coordinate, direction, *args):
        if len(args) == 1:
            step_value = args[0]
        else:
            step_value = self.step_value

        if direction == 'up' or direction == 'left':
            doStep(coordinate - step_value)
        else:
            doStep(coordinate + step_value)

        self.last_step_direction = direction
        self.last_step_value = step_value

    def up(self, *args):
        self._move(self.point.setY, self.point.y(), 'up', *args)

    def down(self, *args):
        self._move(self.point.setY, self.point.y(), 'down', *args)

    def left(self, *args):
        self._move(self.point.setX, self.point.x(), 'left', *args)

    def right(self, *args):
        self._move(self.point.setX, self.point.x(), 'right', *args)

    def reinitLastStepDirection(self):
        self.last_step_direction = None

    def cancelLastStep(self):
        if 'up' == self.last_step_direction:
            self.down(self.last_step_value)
        elif 'down' == self.last_step_direction:
            self.up(self.last_step_value)
        elif 'left' == self.last_step_direction:
            self.right(self.last_step_value)
        elif 'right' == self.last_step_direction:
            self.left(self.last_step_value)

        self.reinitLastStepDirection()

    def setStep(self, newStep):
        self.step = newStep

    def setKeyUp(self, key):
        self.key_up = key

    def setKeyDown(self, key):
        self.key_down = key

    def setKeyLeft(self, key):
        self.key_left = key

    def setKeyRight(self, key):
        self.key_right = key
