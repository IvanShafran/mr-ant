from PySide.QtCore import QPoint


def isAntObjectIntersectAnother(first_object, second_object):
    first_up_left_corner = first_object.point
    first_down_right_corner = first_up_left_corner + QPoint(first_object.width(), first_object.height())

    second_up_left_corner = second_object.point
    second_down_right_corner = second_up_left_corner + QPoint(second_object.width(), second_object.height())

    if first_up_left_corner.x() > second_down_right_corner.x() or \
       first_down_right_corner.x() < second_up_left_corner.x() or \
       first_up_left_corner.y() > second_down_right_corner.y() or \
       first_down_right_corner.y() < second_up_left_corner.y():
            return False
    else:
            return True


def isAntIntersectOtherAnts(ant, ants):
    for another_ant in ants:
        if another_ant != ant and isAntObjectIntersectAnother(ant, another_ant):
                return True

    return False


def isAntIntersectAntObjectsWithWorkZone(ant, ant_objects, check_only_work_zone=False):
    if check_only_work_zone:
        iterable = ant_objects.workZone()
    else:
        iterable = ant_objects.objects

    for ant_object_item in iterable:
        if check_only_work_zone:
            ant_object = ant_object_item['object']
        else:
            ant_object = ant_object_item

        if isAntObjectIntersectAnother(ant, ant_object):
            return True

    return False
