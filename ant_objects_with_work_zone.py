from ant_object import *
from copy import copy
from random import randint


class AntObjectsWithWorkZoneByXOptimisation():
    """
    It's storage for AntObjects with some optimisation:
    WorkZone is objects in specified interval [min_x, max_x]
    Before using WorkZone you must call updateWorkZone(min_x, max_x)
    """
    def __init__(self):
        self.objects = list()
        self.__work_zone_left_index = 0
        self.__work_zone_right_index = -1

    def getNumberOfObjects(self):
        return len(self.objects)

############################ object adding #################################################

    def __addObject__(self, ant_object, new_object_index):
        self.objects.insert(new_object_index, copy(ant_object))

    def __updateWorkZoneAfterObjectAdding__(self, new_object_index):
        if new_object_index <= self.__work_zone_left_index and new_object_index <= self.__work_zone_right_index:
            self.__work_zone_left_index += 1
            self.__work_zone_right_index += 1
        elif self.__work_zone_left_index < new_object_index <= self.__work_zone_right_index:
            self.__work_zone_right_index += 1

    def addObject(self, ant_object):
        """ant_object is any of descendants of AntObject class."""
        new_object_index = len(self.objects)
        while new_object_index > 0 and self.objects[new_object_index - 1].point.x() > ant_object.point.x():
            new_object_index -= 1

        self.__addObject__(ant_object, new_object_index)
        self.__updateWorkZoneAfterObjectAdding__(new_object_index)

    def addRandomObjects(self, number_of_objects, ant_objects_list, min_x, max_x, min_y, max_y):
        if len(ant_objects_list) == 0:
            raise Exception("addRandomObjects: ant_object_list is empty")

        if (max_x < min_x) or (max_y < min_y):
            raise Exception("addRandomObjects: (max_x < min_x) or (max_y < min_y)")

        for x in range(number_of_objects):
            ant_object = copy(ant_objects_list[randint(0, len(ant_objects_list) - 1)])
            ant_object.point = QPoint(randint(min_x, max_x - ant_object.width()),
                                      randint(min_y, max_y - ant_object.height()))
            self.addObject(ant_object)

############################ work zone #################################################

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
        You can use index for modifyObject(self, modifier, index).
        """
        if self.isWorkZoneEmpty():
            return ()
        else:
            return (dict((('object', self.objects[i]), ('index', i)))
                    for i in range(self.__work_zone_left_index, self.__work_zone_right_index + 1))

############################ modifying #################################################

    def modifyObject(self, modifier, index):
        modifier(self.objects[index])

    def modifyAllObjects(self, modifier):
        for ant_object in self.objects:
            modifier(ant_object)

    def modifyWorkZone(self, modifier):
        for ant_object in self.workZone():
            modifier(ant_object['object'])
