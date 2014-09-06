from PySide.QtCore import QTimer, QObject, SIGNAL


class AntReverseCalculation():
    """
    Callable function calls every second and at once, and it must have "seconds_before_start" as argument.
    """
    def __init__(self):
        self.__seconds_before_start = 0
        self.__timer = QTimer()
        QObject.connect(self.__timer, SIGNAL('timeout()'), self.__action__)

    def __action__(self):
        self.__seconds_before_start -= 1
        if self.__seconds_before_start == 0:
            self.__timer.stop()

        self.__callable(seconds_before_start=self.__seconds_before_start)

    def startReverseCalculation(self, number_of_seconds, callable_function):
        self.__callable = callable_function
        self.__seconds_before_start = number_of_seconds + 1
        self.__timer.start(1000)
        self.__action__()
