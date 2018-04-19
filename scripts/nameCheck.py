"""From contexts and utterances files chooses only sentences without some introductions and introduction demands.

File: nameCheck.py
Author: Jiří Čechák
Date: 12.04.2018
Python Version: 3.6.3

From contexts and utterances files chooses only sentences without some introductions and introduction demands.
Saves choosed sentences to new files.

Args:
    file with contexts file path
    file with utterances file path
    file with contexts new file path
    file with utterances new file path
"""

import nltk
import sys

lookingForEnc = [["your", "name"], ["who", "are", "you"], [
    "who", "you", "be"], ["how", "call", "you"], ["introduce", "yourself"]]
lookingForDec = [["i", "am"], ["i", "'m"], ["i", "m"],
                 ["my", "name"], ["call", "me"], ["calls", "me"]]


if len(sys.argv) != 5:
    print("Error: Bad format of program arguments.")
    sys.exit()

contextFilePath = sys.argv[1]
utteranceFilePath = sys.argv[2]
newContextFilePath = sys.argv[3]
newUtteranceFilePath = sys.argv[4]


def seqToTokens(seq):
    return nltk.word_tokenize(seq)


try:
    encFile = open(contextFilePath)
    decFile = open(utteranceFilePath)

    encArr = []
    decArr = []

    i = 0
    for encLine, decLine in zip(encFile, decFile):
        encLine = encLine.strip("\n")
        decLine = decLine.strip("\n")

        encLineTokens = seqToTokens(encLine)
        decLineTokens = seqToTokens(decLine)

        for tokens in lookingForEnc:
            flag = True

            for token in tokens:
                if token not in encLineTokens:
                    flag = False
                    break

            if flag:
                break

        if not flag:
            for tokens in lookingForDec:
                flag = True

                for token in tokens:
                    if token not in decLineTokens:
                        flag = False
                        break

                if flag:
                    break

        if not flag:
            encArr.append(encLine)
            decArr.append(decLine)

        i += 1

        if i % 1000 == 0:
            print("\r{}".format(i), end="")

    print("\r", end="")

    encFile.close()
    decFile.close()

    encFile = open(newContextFilePath, "w")
    decFile = open(newUtteranceFilePath, "w")

    for encLine, decLine in zip(encArr, decArr):
        encFile.write("{}\n".format(encLine))
        decFile.write("{}\n".format(decLine))

    encFile.close()
    decFile.close()

    print("TOTAL: {} / {}".format(len(encArr), i))

except Exception as e:
    print(e)
