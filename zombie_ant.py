from PySide.QtCore import QPoint
from ant import Ant
from ant_object_movement import AntObjectMovement
from algorithm_A_star import findWayByAStar


class ZombieAnt(AntObjectMovement):
    def __init__(self, name, up_down_step_value, left_right_step_value):
        super(ZombieAnt, self).__init__()
        self.name = name
        self.__is_zombie = False
        self.__reverse_path = list()
        self.__up_down_step_value = up_down_step_value
        self.__left_right_step_value = left_right_step_value
        self.__is_zombie = True

    def isZombie(self):
        return self.__is_zombie

    def __checkPoint__(self, point):
        fake_ant = Ant('fake')
        fake_ant.picture = self.picture
        fake_ant.point = point

        return not self.__isAntIntersectAnything(fake_ant)

    def __getIncidenceList__(self, point):
        result = list()

        up_point = point + QPoint(0, -self.__up_down_step_value)
        down_point = point + QPoint(0, self.__up_down_step_value)
        left_point = point + QPoint(-self.__left_right_step_value, 0)
        right_point = point + QPoint(self.__left_right_step_value, 0)

        if self.__checkPoint__(up_point):
            result.append(up_point)

        if self.__checkPoint__(down_point):
            result.append(down_point)

        if self.__checkPoint__(left_point):
            result.append(left_point)

        if self.__checkPoint__(right_point):
            result.append(right_point)

        return result

    def findWayToVerticalLine(self, finish_x, isAntIntersectAnything):
        """
        finish_x - vertical finish line x coordinate
        isFreePlace - function with three arguments - point, width, height
        """

        self.__isAntIntersectAnything = isAntIntersectAnything
        try:
            self.__reverse_path = findWayByAStar(self.point, lambda point: point.x() >= finish_x, lambda x, y: 1,
                self.__getIncidenceList__, lambda point: abs(finish_x - point.x()))
        except:
            self.__reverse_path = list()

        self.__reverse_path.reverse()

    def isPathExist(self):
        return len(self.__reverse_path) > 0

    def move(self, step_value):
        if not self.isPathExist():
            return

        if self.__reverse_path[-1] == self.point:
            self.__reverse_path.pop(-1)

        if not self.isPathExist():
            return

        if self.point.x() < self.__reverse_path[-1].x():
            self.right(step_value)
        elif self.point.x() > self.__reverse_path[-1].x():
            self.left(step_value)
        elif self.point.y() < self.__reverse_path[-1].y():
            self.down(step_value)
        elif self.point.y() > self.__reverse_path[-1].y():
            self.up(step_value)
