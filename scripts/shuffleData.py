"""Shuffles training or testing data.

File: shuffleData.py
Author: Jiří Čechák
Date: 12.04.2018
Python Version: 3.6.3

Shuffles training or testing data which consists of pairs of context and utterance and
saves them to new files.

Args:
    file with contexts file path
    file with utterances file path
    file with contexts new file path
    file with utterances new file path
"""

import nltk
import sys
from sklearn.model_selection import train_test_split

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
        encArr.append(encLine)
        decArr.append(decLine)

    encFile.close()
    decFile.close()

    encArrNew, _, decArrNew, _ = train_test_split(
        encArr, decArr, test_size=0, shuffle=True)

    encFileNew = open(newContextFilePath, "w")
    decFileNew = open(newUtteranceFilePath, "w")

    for encLine, decLine in zip(encArrNew, decArrNew):
        encFileNew.write(encLine)
        decFileNew.write(decLine)

    encFileNew.close()
    decFileNew.close()

except Exception as e:
    print(e)
