from PySide.QtCore import QPoint
from ant import *
from algorithm_A_star import findWayByAStar


class ZombieAnt(Ant):
    def __init__(self, name, up_down_step_value, left_right_step_value):
        super(ZombieAnt, self).__init__(name)
        self._reverse_path = list()
        self._up_down_step_value = up_down_step_value
        self._left_right_step_value = left_right_step_value

    def _getIncidenceList(self, point):
        result = list()
        true_point = self.motion.point

        max_back_x = 100
        if point.x() < max(0, true_point.x() - max_back_x):
            return result

        up_point = point + QPoint(0, -self._up_down_step_value)
        down_point = point + QPoint(0, self._up_down_step_value)
        left_point = point + QPoint(-self._left_right_step_value, 0)
        right_point = point + QPoint(self._left_right_step_value, 0)

        self.motion.point = up_point
        if not self._isFreePlace(self):
            result.append(up_point)

        self.motion.point = down_point
        if not self._isFreePlace(self):
            result.append(down_point)

        self.motion.point = left_point
        if not self._isFreePlace(self):
            result.append(left_point)

        self.motion.point = right_point
        if not self._isFreePlace(self):
            result.append(right_point)

        self.motion.point = true_point

        return result

    def findWayToVerticalLine(self, finish_x, isFreePlace):
        self._isFreePlace = isFreePlace
        try:
            self._reverse_path = findWayByAStar(self.motion.point, lambda point: point.x() >= finish_x, lambda x, y: 1,
                                self._getIncidenceList, lambda point: abs(finish_x - point.x()))
        except:
            self._reverse_path = list()

        self._reverse_path.reverse()

    def isPathExist(self):
        return len(self._reverse_path) > 0

    def move(self, step_value):
        if len(self._reverse_path) == 0:
            return

        if self._reverse_path[-1] == self.motion.point:
            self._reverse_path.pop(-1)

        if len(self._reverse_path) == 0:
            return

        if self.motion.point.x() < self._reverse_path[-1].x():
            self.motion.right(step_value)
        elif self.motion.point.x() > self._reverse_path[-1].x():
            self.motion.left(step_value)
        elif self.motion.point.y() < self._reverse_path[-1].y():
            self.motion.down(step_value)
        elif self.motion.point.y() > self._reverse_path[-1].y():
            self.motion.up(step_value)
