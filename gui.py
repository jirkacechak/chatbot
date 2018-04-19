"""GUI module.

File: gui.py
Author: Jiří Čechák
Date: 12.04.2018
Python Version: 3.6.3

Contains classes for creating chatting GUI.
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QScrollArea, QTextEdit
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt

import constants as c


class ChatGUI():
    """Creates and starts chatting GUI."""

    def __init__(self, chatManager):
        """Creates chatting GUI.
        
        Args:
            chatManager: chatting manager
        """

        self.app = QApplication(sys.argv)

        self.window = Window(chatManager)

    def start(self):
        """Starts chatting GUI."""

        sys.exit(self.app.exec_())


class Window(QWidget):
    """Creates main chatting GUI window."""

    def __init__(self, chatManager, parent=None):
        """Creates main chatting GUI window.
        
        Args:
            chatManager: chatting manager
            parent: parent
        """

        super(Window, self).__init__(parent)

        self.chatManager = chatManager
        self.conversation = []

        self.setMinimumSize(c.WINDOW_WIDTH_MIN, c.WINDOW_HEIGHT_MIN)
        self.resize(c.WINDOW_WIDTH_DEFAULT, c.WINDOW_HEIGHT_DEFAULT)
        self.setWindowTitle(c.WINDOW_LABEL)

        self.textArea = QTextEdit()
        self.textArea.setReadOnly(True)
        self.textArea.setLineWrapMode(QTextEdit.NoWrap)

        self.textInput = TextInput(
            self, placeholderText=c.TEXT_INPUT_PLACEHOLDER)
        self.textInput.selectAll()
        self.textInput.setFocus()

        self.button = QPushButton(c.BUTTON_LABEL)
        self.button.clicked.connect(self.onButtonClick)
        font = self.button.font()
        font.setPointSize(c.BUTTON_FONT_SIZE)
        self.button.setFont(font)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.addWidget(self.textInput)
        self.bottomLayout.addWidget(self.button)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.textArea)
        self.mainLayout.addLayout(self.bottomLayout)

        self.setLayout(self.mainLayout)
        self.show()

    def getStyledConversation(self):
        """Returns formated conversation text."""

        styledConversation = ""

        for i, text in enumerate(self.conversation):
            styledConversation += "<p style='color: {}; font-size: {}px;'>{}</p>".format(c.TEXT_AREA_TEXT_USER_COLOR if (
                i + 1) % 2 else c.TEXT_AREA_TEXT_CHATBOT_COLOR, c.TEXT_AREA_TEXT_USER_FONT_SIZE if (i + 1) % 2 else c.TEXT_AREA_TEXT_CHATBOT_FONT_SIZE, text)

        styledConversation += "<p style='color: white; font-size: 1px;'> </p>"

        return styledConversation

    def onInput(self):
        """Handles context input signal."""

        if self.textInput.text() != "":
            text = self.textInput.text()
            self.textInput.setText("")

            self.conversation.append(text)
            self.conversation.append(self.chatManager.getAnswer(text))
            self.textArea.setText(self.getStyledConversation())
            self.textArea.moveCursor(QTextCursor.End)

        self.textInput.selectAll()
        self.textInput.setFocus()

    def onButtonClick(self):
        """Handles send button click."""

        self.onInput()


class TextInput(QLineEdit):
    """Creates input text field."""

    def __init__(self, parent, placeholderText):
        """Creates input text field.
        
        Args:
            parent: parent
            placeholderText: placeholder
        """

        super().__init__(parent, placeholderText=placeholderText)

        self.parent = parent
        font = self.font()
        font.setPointSize(c.TEXT_INPUT_FONT_SIZE)
        self.setFont(font)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.parent.onInput()
        else:
            super().keyPressEvent(e)
