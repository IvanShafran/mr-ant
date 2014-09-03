from PySide.QtCore import QTimer, QObject, SIGNAL
from copy import copy


class AntReverseCalculation():
    """
    Callable function calls every second and at once, and it must has "seconds_before_start" as argument.
    """
    def __init__(self):
        self._seconds_before_start = 0
        self._timer = QTimer()
        QObject.connect(self._timer, SIGNAL('timeout()'), self._action)

    def _action(self):
        self._seconds_before_start -= 1
        if self._seconds_before_start == 0:
            self._timer.stop()

        self._callable(seconds_before_start=self._seconds_before_start)

    def startReverseCalculation(self, number_of_seconds, callable_function):
        self._callable = callable_function
        self._seconds_before_start = copy(number_of_seconds) + 1
        self._timer.start(1000)
        self._action()
