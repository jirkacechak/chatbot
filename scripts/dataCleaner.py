"""Cleans training or testing data obtained from movie titles.

File: dataCleaner.py
Author: Jiří Čechák
Date: 12.04.2018
Python Version: 3.6.3

Cleans training or testing data obtained from movie titles.
Saves cleared sentences to new files.

Args:
    file with contexts file path
    file with utterances file path
    file with contexts new file path
    file with utterances new file path
"""

import re
import sys


def clearLine(line):
    """Removes subtitles tokens from line.

    Args:
        line to clear

    Returns:
        cleared line
    """

    line = re.sub(
        r"(<[^>]+>|</[^>]+>)", " ", line)
    line = re.sub(
        r"(&amp;)", "&", line)
    line = re.sub(
        r"(&quot;|&lt;|&gt;)", " ", line)
    line = re.sub(
        r"(^-+|-+$)", "", line)
    line = re.sub(
        r"(^\s+|\s+$)", "", line)
    line = re.sub(
        r"((?<!^)\[[^]]*\](?=$)|(?<=^)\[[^]]*\](?!$)|(?<!^)\[[^]]*\](?!$))", " ", line)
    line = re.sub(
        r"(^\[|\]$)", "", line)
    return line


if len(sys.argv) != 5:
    print("Error: Bad format of program arguments.")
    sys.exit()

contextFilePath = sys.argv[1]
utteranceFilePath = sys.argv[2]
newContextFilePath = sys.argv[3]
newUtteranceFilePath = sys.argv[4]

try:
    encFile = open(contextFilePath)
    decFile = open(utteranceFilePath)

    encArr = []
    decArr = []

    for encLine, decLine in zip(encFile, decFile):
        encLine = clearLine(encLine.strip("\n"))
        decLine = clearLine(decLine.strip("\n"))

        encArr.append(encLine)
        decArr.append(decLine)

    encFile.close()
    decFile.close()

    encFile = open(newContextFilePath, "w")
    decFile = open(newUtteranceFilePath, "w")

    for encLine, decLine in zip(encArr, decArr):
        if len(encLine) > 0 and len(decLine) > 0:
            encFile.write("{}\n".format(encLine))
            decFile.write("{}\n".format(decLine))

    encFile.close()
    decFile.close()

except Exception as e:
    print(e)
