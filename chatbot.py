"""Executable script.

File: chatbot.py
Author: Jiří Čechák
Date: 12.04.2018
Python Version: 3.6.3

Executable script which parse program arguments and starts training, chatting or testing.
"""

import sys
import re

from train import train
from chat import chat
from test import test
from utils import printErrorAndExit, printHelpAndExit
import constants as c

if __name__ == '__main__':
    flagArg = True

    mode = c.DEFAULT_MODE
    dataLimit = c.DEFAULT_DATA_LIMIT
    testDataLimit = c.DEFAULT_TEST_DATA_LIMIT
    useSavedWeights = c.DEFAULT_USW
    modelNumber = c.DEFAULT_MODEL
    testing = c.DEFAULT_TESTING
    useChatGui = c.DEFAULT_USE_CHAT_GUI

    for arg in sys.argv:
        if flagArg:
            flagArg = False
            continue

        if arg == "-h" or arg == "--help":
            printHelpAndExit()

        elif arg == "--mode={}".format(c.MODE_CHAT):
            mode = c.MODE_CHAT

        elif arg == "--mode={}".format(c.MODE_TRAIN):
            mode = c.MODE_TRAIN
        
        elif arg == "--mode={}".format(c.MODE_TEST):
            mode = c.MODE_TEST

        elif arg == "--usw={}".format(c.TEXT_ENABLE):
            useSavedWeights = True

        elif arg == "--usw={}".format(c.TEXT_DISABLE):
            useSavedWeights = False

        elif arg == "--testing={}".format(c.TEXT_ENABLE):
            testing = True

        elif arg == "--testing={}".format(c.TEXT_DISABLE):
            testing = False
        
        elif arg == "--gui={}".format(c.TEXT_ENABLE):
            useChatGui = True

        elif arg == "--gui={}".format(c.TEXT_DISABLE):
            useChatGui = False

        elif re.compile(r"^--dataLimit=\d+$").match(arg):
            dataLimit = int(arg[12:])

            if dataLimit < c.MIN_DATA_SIZE:
                printErrorAndExit(c.ERROR_MIN_DATA_SIZE)
        
        elif re.compile(r"^--testDataLimit=\d+$").match(arg):
            testDataLimit = int(arg[16:])

            if testDataLimit < c.MIN_TEST_DATA_SIZE:
                printErrorAndExit(c.ERROR_MIN_TEST_DATA_SIZE)

        elif re.compile(r"^--model=\d+$").match(arg):
            modelNumber = int(arg[8:])

            if modelNumber > c.NUMBER_OF_MODELS:
                printErrorAndExit(c.ERROR_ARGUMENTS)

        else:
            printErrorAndExit(c.ERROR_ARGUMENTS)

    if mode == c.MODE_CHAT:
        chat(modelNumber, useChatGui)
    elif mode == c.MODE_TEST:
        test(modelNumber, testDataLimit)
    else:
        train(modelNumber, dataLimit, useSavedWeights, testing)
