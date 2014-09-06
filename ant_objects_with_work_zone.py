from ant_object import *
from copy import deepcopy
from random import randint



class AntObjectsWithWorkZoneByXOptimisation():
    """
    It's storage for AntObjects with some optimisation:
        1) All pictures are in picture_storage, object.picture has link to item of picture_storage
        2) WorkZone is objects in specified interval [min_x, max_x]
    Before using WorkZone you must call updateWorkZone(min_x, max_x)
    """
    def __init__(self):
        self.__picture_storage = list()
        self.objects = list()
        self.__work_zone_left_index = 0
        self.__work_zone_right_index = -1

    def addPicture(self, path):
        """
        Returns index of picture in storage.
        """
        self.__picture_storage.append(QPixmap())
        self.__picture_storage[-1].load(path)
        return self.getNumberOfObjects() - 1

    def __addObject__(self, ant_object, index_of_picture_in_storage, new_object_index):
        self.objects.insert(new_object_index, deepcopy(ant_object))
        self.objects[new_object_index].picture = self.__picture_storage[index_of_picture_in_storage]

    def addObject(self, ant_object, index_of_picture_in_storage=0):
        """ant_object is any descendant of AntObject class."""
        new_object_index = len(self.objects)
        while new_object_index > 0 and self.objects[new_object_index - 1].point.x() > ant_object.point.x():
            new_object_index -= 1

        self.__addObject__(ant_object, index_of_picture_in_storage, new_object_index)

    def getNumberOfObjects(self):
        return len(self.objects)

    def getNumberOfPictureInStorage(self):
        return len(self.__picture_storage)

    def updateWorkZone(self, min_x, max_x, *args):
        """*args for overriding"""

        if self.__work_zone_right_index == -1 or self.objects[self.__work_zone_right_index].point.x() < max_x:
            while ((self.__work_zone_right_index + 1) < self.getNumberOfObjects()) and \
                  (self.objects[self.__work_zone_right_index + 1].point.x() < max_x):
                        self.__work_zone_right_index += 1
        else:
            while self.__work_zone_right_index > -1 and self.objects[self.__work_zone_right_index].point.x() >= max_x:
                self.__work_zone_right_index -= 1


        if self.__work_zone_right_index < self.__work_zone_left_index:
            if self.__work_zone_right_index == -1:
                self.__work_zone_left_index = 0
            else:
                self.__work_zone_left_index = self.__work_zone_right_index + 1


        if self.__work_zone_left_index == self.getNumberOfObjects():
            while self.__work_zone_left_index > 0 and \
                    self.objects[self.__work_zone_left_index - 1].point.x() + \
                    self.objects[self.__work_zone_left_index - 1].width() > min_x:
                        self.__work_zone_left_index -= 1

        elif self.objects[self.__work_zone_left_index].point.x() + \
             self.objects[self.__work_zone_left_index].width() > min_x:
                while self.__work_zone_left_index > 0 and \
                        self.objects[self.__work_zone_left_index - 1].point.x() + \
                        self.objects[self.__work_zone_left_index - 1].width() > min_x:
                            self.__work_zone_left_index -= 1

        else:
            while (self.__work_zone_left_index < self.getNumberOfObjects()) and \
                  ((self.objects[self.__work_zone_left_index].point.x() +
                  self.objects[self.__work_zone_left_index].width()) < min_x):
                        self.__work_zone_left_index += 1

    def isWorkZoneEmpty(self):
        return self.__work_zone_left_index > self.__work_zone_right_index

    def workZone(self):
        """
        Returns list of dicts with two items: ant_object, index.
        You can use index for setObjectEnabled(index).
        """
        if self.isWorkZoneEmpty():
            return ()
        else:
            return (dict((('object', self.objects[i]), ('index', i))) for i in range(self.__work_zone_left_index,
                                                                             self.__work_zone_right_index + 1))

    def setObjectEnabled(self, index, enabled=True):
        self.objects[index].setEnabled(enabled)

    def setRandomPictures(self):
        """ All pictures in storage must have equal size."""
        for ant_object in self.objects:
            index_of_picture = randint(0, self.getNumberOfPictureInStorage() - 1)
            ant_object.picture = self.__picture_storage[index_of_picture]

    def createRandomObjects(self, number_of_objects, min_x, max_x, min_y, max_y):
        for x in range(number_of_objects):
            index_of_picture = randint(0, self.getNumberOfPictureInStorage() - 1)
            point = QPoint(randint(min_x, max_x - self.__picture_storage[index_of_picture].width()),
                           randint(min_y, max_y - self.__picture_storage[index_of_picture].height()))
            self.addObject(AntObject(point), index_of_picture)
