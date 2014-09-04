from encodings.punycode import selective_find

import sys
from PySide.QtGui import QWidget, QPainter, QApplication, QPixmap
from PySide.QtCore import QTimer, QObject, SIGNAL, Qt, QPoint
from ant import Ant
from ant_objects_with_work_zone import AntObjectsWithWorkZoneByXOptimisation
from ant_message import AntMessage
from reverse_calculation import AntReverseCalculation
from ant_geometry import isAntIntersectOtherAnts, isAntIntersectAntObjectsWithWorkZone
from zombie_ant import ZombieAnt


class FieldProperty():
    def __init__(self):
        self.focus_point = QPoint()
        self.width = 0
        self.height = 0
        self.number_of_barriers = 0
        self.number_of_background_pictures = 0
        self.number_of_ants = 0
        self.number_of_zombie_ants = 0
        self.start_line_x = 0
        self.finish_line_x = 0
        self.field_motion_step = 0
        self.distance_before_first_barrier = 200
        self.critical_distance_before_screen_end = 400


class AntBordersForRace(list):
    def __init__(self):
        super(AntBordersForRace, self).__init__()
        self.width = 0
        self.height = 0


class GameRunToAnthill(QWidget):
    #--------------------- initialization ---------------------
    def __init__(self):
        super(GameRunToAnthill, self).__init__()
        self.init_game('init')
        self.repaint()

    def init_game(self, type_of_init):
        self.game_started = False
        if type_of_init != 'restart':
            self.initScreenSize()
            self.fieldInit()
            self.windowInit()
            self.otherInit()
            self.timerInit()
            self.messageInit()
        else:
            self.timer.stop()
            self.field.focus_point = QPoint(0, 0)
            self.message.noMessage()

        self.antsInit()
        self.bordersInit()
        self.barriersInit()
        self.backgroundInit()
        self.zombieInit()
        self.updateState()

    def initScreenSize(self):
        self.show()
        self.close()

    def fieldInit(self):
        self.field = FieldProperty()
        self.field.focus_point = QPoint(0, 0)
        self.field.height = 500
        self.field.width = 8000
        self.field.number_of_barriers = 120
        self.field.start_line_x = 50
        self.field.finish_line_x = self.field.width - 80
        self.field.number_of_background_pictures = 0
        self.field.field_motion_step = 2
        self.field.number_of_ants = 1
        self.field.number_of_zombie_ants = 1

    def windowInit(self):
        self.setMaximumHeight(self.field.height + self.field.focus_point.y())
        self.setGeometry(2, 30, min(self.maximumWidth(), self.field.width), self.maximumHeight())
        self.setWindowTitle('Run to anthill')

    def otherInit(self):
        self.pressed_keys = set()
    def timerInit(self):
        self.reverse_calculation = AntReverseCalculation()

        self.timer = QTimer(self)
        self.timer.setInterval(10)
        QObject.connect(self.timer, SIGNAL('timeout()'), self.doGameStep)

    def messageInit(self):
        self.message = AntMessage()
        self.message.add('second_0', '.\\pictures\\messages\\go.png')
        self.message.add('second_1', '.\\pictures\\messages\\second_1.png')
        self.message.add('second_2', '.\\pictures\\messages\\second_2.png')
        self.message.add('second_3', '.\\pictures\\messages\\second_3.png')
        self.message.add('pause', '.\\pictures\\messages\\pause.png')
        self.message.add('tie', '.\\pictures\\messages\\tie.png')

    def antsInit(self):
        names = tuple(('red', 'blue', 'green'))
        keys = tuple((tuple((Qt.Key_W, Qt.Key_S, Qt.Key_A, Qt.Key_D)),
                      tuple((Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right)),
                      tuple((Qt.Key_I, Qt.Key_K, Qt.Key_J, Qt.Key_L))))
        self.ants = list()
        for index in range(self.field.number_of_ants):
            self.ants.append(Ant(names[index]))
            self.ants[index].picture.load('.\\pictures\\ants\\' + names[index] + '_ant.png')
            self.ants[index].motion.point = QPoint(0,
                self.field.height // (self.field.number_of_ants + self.field.number_of_zombie_ants + 1) * (index + 1))
            self.ants[index].motion.setKeyUp(keys[index][0])
            self.ants[index].motion.setKeyDown(keys[index][1])
            self.ants[index].motion.setKeyLeft(keys[index][2])
            self.ants[index].motion.setKeyRight(keys[index][3])
            self.message.add(self.ants[index].name + '_ant_wins', '.\\pictures\\messages\\'
                             + self.ants[index].name + '_ant_wins.png')

    def bordersInit(self):
        self.borders = AntBordersForRace()
        self.borders.height = 16
        self.borders.width = 64
        self.borders.append(AntObjectsWithWorkZoneByXOptimisation())
        self.borders.append(AntObjectsWithWorkZoneByXOptimisation())
        for x in range(4):
            self.borders[0].addPicture('.\\pictures\\borders\\border_' + str(x) + '.bmp')
            self.borders[1].addPicture('.\\pictures\\borders\\border_' + str(x) + '.bmp')

        for x in range(0, self.field.width, self.borders.width):
            self.borders[0].addObject(QPoint(x, 0), 0)
            self.borders[1].addObject(QPoint(x, self.field.height - self.borders.height), 1)
        self.borders[0].setRandomPictures()
        self.borders[1].setRandomPictures()

    def barriersInit(self):
        self.barriers = AntObjectsWithWorkZoneByXOptimisation()
        self.barriers.addPicture('.\\pictures\\barriers\\box.bmp')
        self.barriers.addPicture('.\\pictures\\barriers\\heisenberg.bmp')
        self.barriers.createRandomObjects(self.field.number_of_barriers,
                                          self.field.start_line_x + self.field.distance_before_first_barrier,
                                          self.field.finish_line_x,
                                          self.borders.height, self.field.height - self.borders.height)

    def backgroundInit(self):
        self.background_pictures = AntObjectsWithWorkZoneByXOptimisation()
        self.background_pictures.addPicture('.\\pictures\\background\\grass.png')
        for index in range(9):
            self.background_pictures.addPicture('.\\pictures\\background\\leaf_' + str(index) + '.png')
        self.background_pictures.createRandomObjects(self.field.number_of_background_pictures,
                                                     0, self.field.finish_line_x,
                                                     self.borders.height, self.field.height - self.borders.height)

    def zombieInit(self):
        self.message.add('zombie_are_waking_up', '.\\pictures\\messages\\zombie_are_waking_up.png')
        names = tuple(('red_zombie', 'blue_zombie', 'green_zombie'))
        for index in range(self.field.number_of_zombie_ants):
            self.ants.append(ZombieAnt(names[index], 30, 60))
            self.ants[-1].zombie = True
            self.ants[-1].picture.load('.\\pictures\\zombie_ants\\' + names[index] + '_ant.png')
            self.ants[-1].motion.point = QPoint(0,
                self.field.height // (self.field.number_of_ants + self.field.number_of_zombie_ants + 1) *
                (index + self.field.number_of_ants + 1))

            self.message.add(self.ants[-1].name + '_ant_wins',
                             '.\\pictures\\messages\\' + self.ants[-1].name + '_ant_wins.png')

        #--------------------- drawing ---------------------

    def paintBackground(self, painter):
        painter.setPen(Qt.white)
        painter.setBrush(Qt.white)
        painter.drawRect(0, 0, self.width(), self.height())

        for background_picture_item in self.background_pictures.workZone():
            background_picture = background_picture_item['object']
            painter.drawPixmap(background_picture.point + self.field.focus_point, background_picture.picture)

    def paintAnts(self, painter):
        for ant in self.ants:
            painter.drawPixmap(ant.motion.point + self.field.focus_point, ant.picture)

    def paintBarriers(self, painter):
        for barrier_item in self.barriers.workZone():
            barrier = barrier_item['object']
            painter.drawPixmap(barrier.point + self.field.focus_point, barrier.picture)

    def paintBorders(self, painter):
        for index in range(len(self.borders)):
            for border_item in self.borders[index].workZone():
                border = border_item['object']
                painter.drawPixmap(border.point + self.field.focus_point, border.picture)

    def paintStartAndFinishLine(self, painter):
        start = QPixmap()
        start.load('.\\pictures\\start-finish\\start.bmp')
        finish = QPixmap()
        finish.load('.\\pictures\\start-finish\\finish.bmp')

        for y in range(0, self.field.height, start.height()):
            painter.drawPixmap(QPoint(self.field.start_line_x, y) + self.field.focus_point, start)
            painter.drawPixmap(QPoint(self.field.finish_line_x, y) + self.field.focus_point, finish)

    def paintMessage(self, painter):
        if self.message.isThereMessage():
            point = QPoint((self.width() - self.message.getMessagePicture().width()) // 2,
                           (self.height() - self.message.getMessagePicture().height()) // 2)
            painter.drawPixmap(point, self.message.getMessagePicture())

    def paintEvent(self, event):
        painter = QPainter(self)

        self.updateState()

        self.paintBackground(painter)
        self.paintStartAndFinishLine(painter)
        self.paintAnts(painter)
        self.paintBarriers(painter)
        self.paintBorders(painter)
        self.paintMessage(painter)

    #--------------------- updating ---------------------

    def updateFieldFocusPoint(self):
        for ant in self.ants:
            if (self.width() - (ant.motion.point.x() + self.field.focus_point.x())) \
                    < self.field.critical_distance_before_screen_end:
                self.field.focus_point.setX(self.field.focus_point.x() - self.field.field_motion_step)
                return
            """if (ant.motion.point.x() + self.field.focus_point.x()) \
                    < self.field.critical_distance_before_screen_end:
                self.field.focus_point.setX(self.field.focus_point.x() + self.field.field_motion_step)
                return"""

    def updateConstants(self):
        self.field.critical_distance_before_screen_end = self.width() // 5 * 2

    def updateState(self):
        self.updateFieldFocusPoint()

        min_x = 0 - self.field.focus_point.x()
        max_x = self.width() - self.field.focus_point.x()
        self.barriers.updateWorkZone(min_x, max_x)
        self.background_pictures.updateWorkZone(min_x, max_x)
        for index in range(len(self.borders)):
            self.borders[index].updateWorkZone(min_x, max_x)

        self.updateConstants()

    def moveZombie(self):
        for ant in self.ants:
            if ant.zombie:
                self._moveAnt(ant, ant.move)

    def buildZombiePath(self):
        self.message.sendMessage('zombie_are_waking_up')
        self.repaint()
        for ant in self.ants:
            if ant.zombie:
                ant.findWayToVerticalLine(self.field.finish_line_x + 100, self.isAntIntersectAnything)
        self.message.noMessage()
        self.repaint()

    #--------------------- Game control ---------------------

    def reverseCalculationWorker(self, seconds_before_start):
        self.message.sendMessage('second_' + str(seconds_before_start))
        if seconds_before_start == 0:
            self.timer.start()
            QTimer.singleShot(1000, self.message.noMessage)
        self.repaint()

    def fastStart(self):
        self.game_started = True
        self.buildZombiePath()
        self.reverse_calculation.startReverseCalculation(0, self.reverseCalculationWorker)

    def start(self):
        self.game_started = True
        self.buildZombiePath()
        if self.timer.isActive():
            self.fastStart()
        else:
            self.reverse_calculation.startReverseCalculation(3, self.reverseCalculationWorker)

    def stop(self):
        self.timer.stop()
        self.message.sendMessage('pause')
        self.repaint()

    def restart(self):
        self.init_game('restart')
        self.repaint()

    def doGameStep(self):
        self.updateState()
        self.processPressedKeys()
        self.moveZombie()
        self.checkFinishLine()
        self.repaint()

    #--------------------- I'm afraid. We need to use ... math! ---------------------

    def _areTwoAntFinished(self):
        finished_count = 0
        for ant in self.ants:
            if self.isAntFinished(ant):
                finished_count += 1

        return finished_count >= 2

    def checkFinishLine(self):
        if self.message.getMessageText() in tuple(ant.name + '_ant_wins' for ant in self.ants) or \
           self.message.getMessageText() == 'tie':
                return

        if self._areTwoAntFinished():
            self.message.sendMessage('tie')
            return

        for ant in self.ants:
            if self.isAntFinished(ant):
                self.message.sendMessage(ant.name + '_ant_wins')

    def isAntFinished(self, ant):
        return ant.motion.point.x() + ant.width() >= self.field.finish_line_x

    def isAntIntersectBarriers(self, ant, check_only_work_zone=False):
        return isAntIntersectAntObjectsWithWorkZone(ant, self.barriers, check_only_work_zone)

    def isAntIntersectBorders(self, ant, check_only_work_zone=False):
        return isAntIntersectAntObjectsWithWorkZone(ant, self.borders[0], check_only_work_zone) or \
               isAntIntersectAntObjectsWithWorkZone(ant, self.borders[1], check_only_work_zone)

    def isAntIntersectAnything(self, ant, check_only_work_zone=False):
        return self.isAntIntersectBarriers(ant, check_only_work_zone) or \
               self.isAntIntersectBorders(ant, check_only_work_zone) or \
               isAntIntersectOtherAnts(ant, self.ants)

    #--------------------- Key processing ---------------------

    def _moveAnt(self, ant, doStep, diagonal_direction=False):
        if diagonal_direction:
            max_step_value = ant.motion.step_value // 2
        else:
            max_step_value = ant.motion.step_value

        for step_value in range(max_step_value):
            doStep(1)
            if self.isAntIntersectAnything(ant, True):
                ant.motion.cancelLastStep()
                return

    def _processPressedMotionKey(self, ant, key, doStep, diagonal_direction):
        if key not in self.pressed_keys:
            return

        self._moveAnt(ant, doStep, diagonal_direction)

    def processPressedMotionKeys(self):
        for ant in self.ants:
            if not ant.zombie:
                motion_key_set = {ant.motion.key_up, ant.motion.key_down, ant.motion.key_left, ant.motion.key_right}
                diagonal_direction = len(motion_key_set & self.pressed_keys) > 1

                self._processPressedMotionKey(ant, ant.motion.key_up, ant.motion.up, diagonal_direction)
                self._processPressedMotionKey(ant, ant.motion.key_down, ant.motion.down, diagonal_direction)
                self._processPressedMotionKey(ant, ant.motion.key_left, ant.motion.left, diagonal_direction)
                self._processPressedMotionKey(ant, ant.motion.key_right, ant.motion.right, diagonal_direction)

    def processPressedKeys(self):
        self.processPressedMotionKeys()

    def _addPlayer(self):
        if self.field.number_of_ants < 3:
            self.field.number_of_ants += 1
            self.antsInit()
            self.zombieInit()
            self.repaint()

    def _delPlayer(self):
        if self.field.number_of_ants > 0:
            self.field.number_of_ants -= 1
            self.antsInit()
            self.zombieInit()
            self.repaint()

    def _addZombie(self):
        if self.field.number_of_zombie_ants < 3:
            self.field.number_of_zombie_ants += 1
            self.antsInit()
            self.zombieInit()
            self.repaint()

    def _delZombie(self):
        if self.field.number_of_zombie_ants > 0:
            self.field.number_of_zombie_ants -= 1
            self.antsInit()
            self.zombieInit()
            self.repaint()

    def _processGameControlKey(self, key):
        if not self.game_started:
            if Qt.Key_Plus in self.pressed_keys and Qt.Key_Z in self.pressed_keys:
                self._addZombie()
            elif Qt.Key_Minus in self.pressed_keys and Qt.Key_Z in self.pressed_keys:
                self._delZombie()
            elif key == Qt.Key_Plus:
                self._addPlayer()
            elif key == Qt.Key_Minus:
                self._delPlayer()

        if key == Qt.Key_F5:
            self.restart()

        if self.message.getMessageText() not in ('red_ant_wins', 'blue_ant_wins', 'green_ant_wins', 'tie'):
            if key == Qt.Key_F8:
                self.fastStart()
            elif key == Qt.Key_F9:
                self.start()
            elif key == Qt.Key_F10:
                self.stop()

    def keyPressEvent(self, event):
        self.pressed_keys.add(event.key())
        self._processGameControlKey(event.key())

    def keyReleaseEvent(self, event):
        self.pressed_keys.remove(event.key())


def _main():
    app = QApplication(sys.argv)
    ex = GameRunToAnthill()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    _main()
