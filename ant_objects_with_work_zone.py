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
        self._picture_storage = list()
        self.objects = list()
        self.initWorkZone()

    def initWorkZone(self):
        self.work_zone_left_bound = 0
        self.work_zone_right_bound = -1

    def addPicture(self, path):
        """
        Returns index of picture in storage.
        """
        self._picture_storage.append(QPixmap())
        self._picture_storage[-1].load(path)
        return self.getNumberOfObjects() - 1

    def _addObject(self, point, index_of_picture_in_storage, index):
        ant_object = AntObject(point)
        self.objects.insert(index, deepcopy(ant_object))
        self.objects[index].picture = self._picture_storage[index_of_picture_in_storage]

    def addObject(self, point, index_of_picture_in_storage=0):
        index = len(self.objects)
        while index > 0 and self.objects[index - 1].point.x() > point.x():
            index -= 1

        self._addObject(point, index_of_picture_in_storage, index)

    def getNumberOfObjects(self):
        return len(self.objects)

    def getNumberOfPictureInStorage(self):
        return len(self._picture_storage)

    def updateWorkZone(self, min_x, max_x, *args):
        """*args for overriding"""

        

        if (self.work_zone_right_bound == -1 or self.objects[self.work_zone_right_bound].point.x() < max_x): 
            while ((self.work_zone_right_bound + 1) < self.getNumberOfObjects()) and \
                  (self.objects[self.work_zone_right_bound + 1].point.x() < max_x):
                    self.work_zone_right_bound += 1
        else:
            while(self.work_zone_right_bound > -1 and self.objects[self.work_zone_right_bound].point.x() >= max_x):
                self.work_zone_right_bound -= 1

        if(self.work_zone_right_bound < self.work_zone_left_bound):
            if(self.work_zone_right_bound == -1):
                self.work_zone_left_bound = 0
            else:
                self.work_zone_left_bound = self.work_zone_right_bound + 1

        if(self.work_zone_left_bound == self.getNumberOfObjects()):
            while(self.work_zone_left_bound > 0 and self.objects[self.work_zone_left_bound - 1].point.x() + self.objects[self.work_zone_left_bound - 1].width() > min_x):
                self.work_zone_left_bound -= 1
        elif (self.objects[self.work_zone_left_bound].point.x() + self.objects[self.work_zone_left_bound].width() > min_x):
            while(self.work_zone_left_bound > 0 and self.objects[self.work_zone_left_bound - 1].point.x() + self.objects[self.work_zone_left_bound - 1].width() > min_x):
                self.work_zone_left_bound -= 1
        else:
            while (self.work_zone_left_bound < self.getNumberOfObjects()) and \
                  ((self.objects[self.work_zone_left_bound].point.x() + self.objects[self.work_zone_left_bound].width())
                    < min_x):
                        self.work_zone_left_bound += 1

    def isWorkZoneEmpty(self):
        return self.work_zone_left_bound > self.work_zone_right_bound

    def workZone(self):
        """
        Returns list of dicts with two items: ant_object, index.
        You can use index for setObjectEnabled(index).
        """
        if self.isWorkZoneEmpty():
            return ()
        else:
            return (dict((('object', self.objects[i]), ('index', i))) for i in range(self.work_zone_left_bound,
                                                                             self.work_zone_right_bound + 1))

    def setObjectEnabled(self, index, enabled=True):
        self.objects[index].enabled = enabled

    def setRandomPictures(self):
        """ All pictures in storage must have equal size."""
        for ant_object in self.objects:
            index_of_picture = randint(0, self.getNumberOfPictureInStorage() - 1)
            ant_object.picture = self._picture_storage[index_of_picture]

    def createRandomObjects(self, number_of_objects, min_x, max_x, min_y, max_y):
        for x in range(number_of_objects):
            index_of_picture = randint(0, self.getNumberOfPictureInStorage() - 1)
            point = QPoint(randint(min_x, max_x - self._picture_storage[index_of_picture].width()),
                           randint(min_y, max_y - self._picture_storage[index_of_picture].height()))
            self.addObject(point, index_of_picture)
