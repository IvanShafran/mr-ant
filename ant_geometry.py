from PySide.QtCore import QPoint


def isObjectIntersectAnother(first_point, first_width, first_height,
                             second_point, second_width, second_height):
    first_up_left_corner = first_point
    first_down_right_corner = first_point + QPoint(first_width, first_height)

    second_up_left_corner = second_point
    second_down_right_corner = second_point + QPoint(second_width, second_height)

    if first_up_left_corner.x() > second_down_right_corner.x() or \
       first_down_right_corner.x() < second_up_left_corner.x() or \
       first_up_left_corner.y() > second_down_right_corner.y() or \
       first_down_right_corner.y() < second_up_left_corner.y():
            return False
    else:
            return True


def isAntIntersectOtherAnts(ant, ants):
    for another_ant in ants:
        if another_ant != ant and isObjectIntersectAnother(ant.motion.point, ant.width(), ant.height(),
                                    another_ant.motion.point, another_ant.width(), another_ant.height()):
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

        if isObjectIntersectAnother(ant.motion.point, ant.width(), ant.height(),
                                    ant_object.point, ant_object.width(), ant_object.height()):
            return True

    return False
