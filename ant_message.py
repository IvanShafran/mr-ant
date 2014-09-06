from PySide.QtGui import QPixmap


class AntMessage():
    def __init__(self):
        self.__messages = dict()
        self.__message_text = 'no_message'

    def sendMessage(self, message):
        self.__message_text = message

    def noMessage(self):
        self.sendMessage('no_message')

    def isThereMessage(self):
        return not self.__message_text == 'no_message'

    def add(self, message, picture_path):
        self.__messages[message] = QPixmap(picture_path)

    def getMessageText(self):
        return self.__message_text

    def getMessagePicture(self):
        return self.__messages[self.__message_text]
