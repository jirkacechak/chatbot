"""Chatting module.

File: constants.py
Author: Jiří Čechák
Date: 12.04.2018
Python Version: 3.6.3

Manages chatting with user in console or in chatting GUI.
"""

from __future__ import print_function
from sys import stdin
import numpy as np
from random import randint

from utils import oneLinePrint, printErrorAndExit, clearConsole, printDivider
import constants as c
from dataUtils import loadVocabulary, getEmbedding, getFileWithLastSavedWeights, seqToTokens, tokenizedInputToIds
from model import createModel, getPredictionString
from data import iDoNotUnderstandAnswers, infoMessage, greetings, goodbyes, introductions, sentenceEndCharacters
from gui import ChatGUI


class ChatManager():
    """Manages getting answer for chatting and saves conversation."""

    def __init__(self, modelNumber, model, vocabulary, wordToIndexVocabulary):
        """Creates chat manager.
        
        Args:
            modelNumber: number of model
            model: model
            vocabulary: index to word vocabulary
            wordToIndexVocabulary: word to index vocabulary
        """

        self.model = model
        self.vocabulary = vocabulary
        self.wordToIndexVocabulary = wordToIndexVocabulary
        self.conversationFile = None

        try:
            self.conversationFile = open(c.MODEL1_CHATDATA_FILEPATH if modelNumber ==
                                         1 else c.MODEL2_CHATDATA_FILEPATH if modelNumber == 2 else c.MODEL3_CHATDATA_FILEPATH, "w")
        except Exception as e:
            print(e)

    def __del__(self):
        if self.conversationFile != None:
            self.conversationFile.close()

    def getAnswer(self, context):
        """Returns predicted answer.

        Args:
            context: context
        
        Returns:
            predicted answer
        """

        tokens = seqToTokens(context)

        if len(tokens) > c.MAX_TOKENS:
            tokens = tokens[:c.MAX_TOKENS]

        tokensIndexes = tokenizedInputToIds(tokens, self.wordToIndexVocabulary)

        answer = getPredictionString(tokensIndexes, self.model, self.vocabulary)

        if answer == "":
            answer = iDoNotUnderstandAnswers[randint(0, len(iDoNotUnderstandAnswers) - 1)]

        if self.conversationFile != None:
            self.conversationFile.write("{}: {}\n".format(
                c.CONVERSATION_SENTENCE_LABEL_USER, context))
            self.conversationFile.write("{}: {}\n".format(
                c.CONVERSATION_SENTENCE_LABEL_CHATBOT, answer))

        return answer


def chat(modelNumber, useChatGui):
    """Chats with user.

    Args:
        modelNumber: number of model
        useChatGui: True if chatting GUI should be used, False if chatting in console
    """

    print("Chatting")

    savedWeightsFile, _, _ = getFileWithLastSavedWeights(modelNumber, None)

    if savedWeightsFile == None:
        printErrorAndExit(c.ERROR_WEIGHTS_FILE_NOT_FOUND)

    vocabulary, wordToIndexVocabulary = loadVocabulary()

    model = createModel(modelNumber, vocabulary, None, savedWeightsFile)

    chatManager = ChatManager(modelNumber, model, vocabulary, wordToIndexVocabulary)

    if useChatGui:
        gui = ChatGUI(chatManager)
        gui.start()

    else:
        if c.CLEAR_CONSOLE_BEFORE_CHAT:
            clearConsole()
        else:
            printDivider()

        if c.PRINT_CONSOLE_GREETING:
            welcomeMessage = greetings[randint(0, len(greetings) - 1)]

            if welcomeMessage[len(welcomeMessage) - 1] in sentenceEndCharacters:
                introduction = introductions[randint(
                    0, len(introductions) - 1)]
                welcomeMessage += " {}{}".format(
                    introduction[0].upper(), introduction[1:])
            else:
                welcomeMessage += ", {}".format(
                    introductions[randint(0, len(introductions) - 1)])

            welcomeMessage += " {}.{}".format(c.CHATBOT_NAME, " {}".format(
                infoMessage) if c.PRINT_CONSOLE_INFO_MESSAGE else "")

            print(welcomeMessage)

        elif c.PRINT_CONSOLE_INFO_MESSAGE:
            print(infoMessage)

        while True:
            oneLinePrint(">")

            for line in stdin:
                context = line
                break

            if context[len(context) - 1] == "\n":
                context = context[:-1]

            if context == "":
                break

            answer = chatManager.getAnswer(context)

            print(answer)

        if c.PRINT_CONSOLE_GOODBYE:
            print(goodbyes[randint(0, len(goodbyes) - 1)])
