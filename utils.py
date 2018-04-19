"""Utility functions.

File: utils.py
Author: Jiří Čechák
Date: 12.04.2018
Python Version: 3.6.3

This module contains all utility functions.
"""

from __future__ import print_function
import sys
import os
from datetime import timedelta

from data import errorMessages
import constants as c


def oneLinePrint(forPrint):
    """Prints one line text.

    Args:
        forPrint: text for printing
    """

    print(forPrint, end="")
    sys.stdout.flush()


def clearConsoleLine():
    """Clears one line in console."""

    oneLinePrint("\r\t\t\t\t\t\t\t\t\t\t\t\r")


def printDivider():
    """Prints divider to console."""

    print("\n--------------------------------------------------------------------------------\n")


def printErrorAndExit(errNum):
    """Prints error message and exits program.

    Args:
        errNum: error code
    """

    oneLinePrint("Error: " + errorMessages[errNum])
    sys.exit()


def printHelpAndExit():
    """Prints generated help text using constants in file constants.py and exits program."""

    defaultText = " (default)"
    indent = "  "

    print("")
    print("Usage:")
    print("{}py chatbot.py [-h|--help] [--mode=[{}|{}|{}]] [--model=<number>] [--dataLimit=<number>] [--testDataLimit=<number>] [--testing=[{}|{}]] [--usw=[{}|{}]] [--gui=[{}|{}]]".format(
        indent, c.MODE_TRAIN, c.MODE_CHAT, c.MODE_TEST, c.TEXT_ENABLE, c.TEXT_DISABLE, c.TEXT_ENABLE, c.TEXT_DISABLE, c.TEXT_ENABLE, c.TEXT_DISABLE))
    print("")
    print("Options:")

    modelNumberText = "Used model number ("
    for i in range(1, c.NUMBER_OF_MODELS + 1):
        modelNumberText += "{}{}{}".format(i, defaultText if c.DEFAULT_MODEL ==
                                           i else "", "/" if i < c.NUMBER_OF_MODELS else ")")

    rows = [["-h, --help", "Show help."], ["--mode=[{}|{}|{}]".format(c.MODE_TRAIN, c.MODE_CHAT, c.MODE_TEST), "Training{}/chatting{}/testing{} mode.".format(defaultText if c.DEFAULT_MODE == c.MODE_TRAIN else "", defaultText if c.DEFAULT_MODE == c.MODE_CHAT else "", defaultText if c.DEFAULT_MODE == c.MODE_TEST else "")], ["--model=<number>", modelNumberText], ["--dataLimit=<number>", "Limit for training data (<number> >= {} | <number> == 0 (no limit)).".format(c.MIN_DATA_SIZE)], ["--testDataLimit=<number>", "Limit for testing data (<number> >= {} | <number> == 0 (no limit)).".format(c.MIN_TEST_DATA_SIZE)], [
        "--testing=[{}|{}]".format(c.TEXT_ENABLE, c.TEXT_DISABLE), "Enable{}/disable{} testing each training epoch.".format(defaultText if c.DEFAULT_TESTING else "", defaultText if not c.DEFAULT_TESTING else "")], ["--usw=[{}|{}]".format(c.TEXT_ENABLE, c.TEXT_DISABLE), "Train model using{}/without using{} saved model weights.".format(defaultText if c.DEFAULT_USW else "", defaultText if not c.DEFAULT_USW else "")], ["--gui=[{}|{}]".format(c.TEXT_ENABLE, c.TEXT_DISABLE), "Chatting using{}/without using{} GUI.".format(defaultText if c.DEFAULT_USE_CHAT_GUI else "", defaultText if not c.DEFAULT_USE_CHAT_GUI else "")]]

    col0Width = max(len(row[0]) for row in rows) + 2
    for row in rows:
        print("{}{}{}".format(indent, row[0].ljust(col0Width), row[1]))

    print("")
    print("Examples:")
    print("{}py chatbot.py --help".format(indent))
    print("{}py chatbot.py --model=1 --dataLimit=1000 --testing={} --usw={}".format(
        indent, c.TEXT_DISABLE, c.TEXT_DISABLE))
    print("{}py chatbot.py --mode={} --model=1".format(indent, c.MODE_CHAT))
    print("{}py chatbot.py --mode={} --model=1 --gui={}".format(indent,
                                                                c.MODE_CHAT, c.TEXT_DISABLE))
    print("{}py chatbot.py --mode={} --model=1 --testDataLimit=100".format(indent, c.MODE_TEST))

    sys.exit()


def fileExistsAndNotEmpty(fileName):
    """Checks if file exists and is not empty.

    Args:
        fileName: path to file for check
    
    Returns:
        True if file exists and is not empty, False otherwise.
    """

    return os.path.isfile(fileName) and os.stat(fileName).st_size > 0


def clearConsole():
    """Clears console."""

    os.system("cls")


def timestampToTime(timestamp):
    """Returns seconds converted to hours, minutes and seconds (HH:mm:ss).

    Args:
        timestamp: seconds
    
    Returns:
        Hours, minutes and seconds in HH:mm:ss format.
    """

    return str(timedelta(seconds=timestamp)).split(".")[0]
