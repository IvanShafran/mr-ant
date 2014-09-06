from ant_object_movement import AntObjectUserMovement


class Ant(AntObjectUserMovement):
    def __init__(self, name):
        super(Ant, self).__init__()
        self.name = name
        self.__is_zombie = False

    def isZombie(self):
        return self.__is_zombie
