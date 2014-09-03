from PySide.QtGui import QPixmap


class AntMessage():
    def __init__(self):
        self._messages = dict()
        self._message = 'no_message'

    def sendMessage(self, message):
        self._message = message

    def noMessage(self):
        self.sendMessage('no_message')

    def isThereMessage(self):
        return not self._message == 'no_message'

    def add(self, message, picture_path):
        self._messages[message] = QPixmap(picture_path)

    def getMessageText(self):
        return self._message

    def getMessagePicture(self):
        return self._messages[self._message]
