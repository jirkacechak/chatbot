"""Data utility functions.

File: dataUtils.py
Author: Jiří Čechák
Date: 12.04.2018
Python Version: 3.6.3

Contains utility function working with different data.
"""

from __future__ import print_function
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import pickle
import numpy as np
import nltk
import re
from keras.preprocessing import sequence
import os

import constants as c
from utils import oneLinePrint, printErrorAndExit, clearConsoleLine

nltk.download("punkt")


def getFileWithLastSavedWeights(modelNumber, dataLimit):
    """Returns file with saved weights.

    Args:
        modelNumber: number of model
        dataLimit: limit for loaded training data
    
    Returns:
        path to file with saved weights
        data size
        epoch number
    """

    oneLinePrint("Loading weights ... ")

    file = None
    max = -1
    dataSize = 0

    folder = c.MODEL1_DIR if modelNumber == 1 else c.MODEL2_DIR if modelNumber == 2 else c.MODEL3_DIR
    weights_filepath_base = c.MODEL1_WEIGHTS_FILEPATH_BASE if modelNumber == 1 else c.MODEL2_WEIGHTS_FILEPATH_BASE if modelNumber == 2 else c.MODEL3_WEIGHTS_FILEPATH_BASE

    for f in [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]:
        if re.compile("^" + re.escape(weights_filepath_base) + r"-\d+-\d+" + re.escape(c.WEIGHTS_FILEPATH_SUFFIX) + "$").match(folder + f):
            nums = re.findall(r"\d+", f)
            fileDataSize = int(nums[0])
            epochNum = int(nums[1])

            if (dataLimit == None or dataLimit == 0 or fileDataSize <= dataLimit) and epochNum > max:
                max = epochNum
                file = f
                dataSize = int(nums[0])

    if file == None:
        print("not found")
        return file, dataSize, max

    file = folder + file

    print("{} ... done".format(file))

    return file, dataSize, max


def tokenizedInputToIds(tokens, vocabulary):
    """Tokenize input sequence to ids.

    Args:
        tokens: tokens sequence
        vocabulary: word to index vocabulary
    
    Returns:
        array of indexes of tokens
    """

    clearedTokens = []
    for t in tokens:
        if t in vocabulary:
            clearedTokens.append(t)
        else:
            clearedTokens.append(c.TOKEN_UNKNOWN)

    tokensIds = np.zeros((1, c.MAX_TOKENS))

    tokensIds[0, -len(clearedTokens):] = np.asarray([vocabulary[t]
                                                     for t in clearedTokens])

    return tokensIds


def seqToTokens(seq):
    """Returns tokenized sequence.

    Args:
        seq: text sequence
    
    Returns:
        Tokenized sequence.
    """

    return nltk.word_tokenize(seq.lower())


def loadDataAndTokenize(encFilePath, decFilePath, limit, vocabulary):
    """Loads training data a tokenize them.

    Args:
        encFilePath: path to file with contexts
        decFilePath: path to file with utterances
        limit: data limit
        vocabulary: word to index vocabulary
    
    Returns:
        tokenized data
    """

    oneLinePrint("Loading data ... ")

    encArr = []
    decArr = []

    try:
        encFile = open(encFilePath)

        linesNumber = 0
        for _ in encFile:
            linesNumber += 1

        encFile.close()

        encFile = open(encFilePath)
        decFile = open(decFilePath)

        i = 0
        for encLine, decLine in zip(encFile, decFile):
            if limit > 0 and len(encArr) >= limit:
                break

            encLine = encLine.rstrip("\n")
            decLine = decLine.rstrip("\n")

            encTokens = seqToTokens(encLine)
            decTokens = seqToTokens(decLine)

            if len(encTokens) > 0 and len(encTokens) <= c.MAX_TOKENS and len(decTokens) > 0 and len(decTokens) + 2 <= c.MAX_TOKENS:

                encUnknownTokens = 0
                decUnknownTokens = 0

                for encToken, decToken in zip(encTokens, decTokens):
                    if encToken == c.TOKEN_UNKNOWN:
                        encUnknownTokens += 1

                    if decToken == c.TOKEN_UNKNOWN:
                        decUnknownTokens += 1

                encTokens = [
                    token if token in vocabulary else c.TOKEN_UNKNOWN for token in encTokens]
                decTokens = [
                    token if token in vocabulary else c.TOKEN_UNKNOWN for token in decTokens]

                encUnknownTokens = -encUnknownTokens
                decUnknownTokens = -decUnknownTokens
                unknownTokensFlag = True

                for encToken, decToken in zip(encTokens, decTokens):
                    if encToken == c.TOKEN_UNKNOWN:
                        encUnknownTokens += 1

                        if encUnknownTokens > c.TOKEN_UNKNOWN_LIMIT:
                            unknownTokensFlag = False
                            break

                    if decToken == c.TOKEN_UNKNOWN:
                        decUnknownTokens += 1

                        if decUnknownTokens > c.TOKEN_UNKNOWN_LIMIT:
                            unknownTokensFlag = False
                            break

                if not unknownTokensFlag:
                    continue

                encArr.append(encTokens)

                decTokensModified = [c.TOKEN_BOS]

                for token in decTokens:
                    decTokensModified.append(token)

                decTokensModified.append(c.TOKEN_EOS)

                decArr.append(decTokensModified)

            i += 1

            if i % 1000 == 0:
                oneLinePrint(
                    "\rLoading data ... {} ({} / {})".format(len(encArr), i, linesNumber))

        encFile.close()
        decFile.close()
    except Exception as e:
        print(e)
        printErrorAndExit(c.ERROR_FILE)

    clearConsoleLine()

    print("\rLoading data ... {} pairs ... done".format(len(encArr)))

    return encArr, decArr


def loadTestingDataAndTokenize(encFilePath, decFilePath, limit, wordToIndexVocabulary):
    """Loads testing data a tokenize them.

    Args:
        encFilePath: path to file with contexts
        decFilePath: path to file with utterances
        limit: data limit
        vocabulary: word to index vocabulary
    
    Returns:
        tokenized data
    """

    oneLinePrint("Loading testing data ... ")

    encArr = []
    decArr = []

    try:
        encFile = open(encFilePath)

        linesNumber = 0
        for _ in encFile:
            linesNumber += 1

        encFile.close()

        encFile = open(encFilePath)
        decFile = open(decFilePath)

        i = 0
        for encLine, decLine in zip(encFile, decFile):
            if limit > 0 and len(encArr) >= limit:
                break
            
            encLine = encLine.rstrip("\n")
            decLine = decLine.rstrip("\n")

            encTokens = seqToTokens(encLine)
            decTokens = seqToTokens(decLine)

            if len(encTokens) > c.MAX_TOKENS:
                encTokens = encTokens[:c.MAX_TOKENS]

            encArr.append(encTokens)
            decArr.append(decTokens)

            i += 1

            if i % 1000 == 0:
                oneLinePrint(
                    "\rLoading testing data ... {} / {}".format(i, linesNumber))

        encFile.close()
        decFile.close()
    except Exception as e:
        print(e)
        printErrorAndExit(c.ERROR_FILE)

    clearConsoleLine()

    print("\rLoading testing data ... {} pairs ... done".format(len(encArr)))

    return encArr, decArr


def loadVocabulary():
    """Loads vocabulary."""

    oneLinePrint("Loading vocabulary ... ")

    try:
        file = open(c.VOCABULARY_FILEPATH, 'rb')
    except:
        printErrorAndExit(c.ERROR_FILE)

    vocabulary = pickle.load(file)
    file.close()

    indexToWord = [v[0] for v in vocabulary]
    indexToWord.append(c.TOKEN_UNKNOWN)

    wordToIndex = dict([(w, i) for i, w in enumerate(indexToWord)])

    print("{} tokens ... done".format(len(vocabulary)))

    return vocabulary, wordToIndex


def padArray(array, maxlen, padding="pre"):
    """Returns padded sequence.

    Args:
        array: array to pad
        maxlen: length
        padding: 'pre' - padding from begining/'post' - padding from end
    
    Returns:
        padded array
    """

    return sequence.pad_sequences(array, maxlen=maxlen, padding=padding)


def getPaddedEnc(context, vocabulary):
    """Returns padded context.

    Args:
        context: context to pad
        vocabulary: word to index vocabulary
    
    Returns:
        padded context
    """

    return padArray(np.asarray([[vocabulary[w] for w in sent] for sent in context]), c.MAX_TOKENS)


def getPaddedDec(utterance, vocabulary):
    """Returns padded utterance.

    Args:
        utterance: utterance to pad
        vocabulary: word to index vocabulary
    
    Returns:
        padded utterance
    """

    return padArray(np.asarray([[vocabulary[w] for w in sent] for sent in utterance]), c.MAX_TOKENS, "post")


def getEmbedding(modelNumber):
    """Loads token embedding.

    Args:
        modelNumber: number of model
    
    Returns:
        loaded embedding
    """

    oneLinePrint("Loading embedding ... ")

    gloveFilepath = c.MODEL1_GLOVE_FILEPATH if modelNumber == 1 else c.MODEL2_GLOVE_FILEPATH if modelNumber == 2 else c.MODEL3_GLOVE_FILEPATH

    try:
        file = open(gloveFilepath, encoding="utf8")

        linesNumber = 0
        for _ in file:
            linesNumber += 1

        file.close()

        file = open(gloveFilepath, encoding="utf8")

        embedding = {}

        i = 0
        for line in file:
            values = line.split()
            embedding[values[0]] = np.asarray(values[1:], dtype="float32")

            i += 1

            if i % 1000 == 0:
                oneLinePrint(
                    "\rLoading embedding ... {} / {}".format(i, linesNumber))

        file.close()

    except:
        printErrorAndExit(c.ERROR_FILE)

    clearConsoleLine()

    print("\rLoading embedding ... {} tokens ... done".format(len(embedding)))

    return embedding


def removeBOSEOS(tokens):
    """Removes BOS and EOS tokens from sequence.

    Args:
        tokens: tokens sequence to remove tokens BOS and EOS from
    
    Returns:
        sequence without tokens BOS and EOS
    """

    indexBOS = -1
    indexEOS = -1

    for i, token in enumerate(tokens):
        if token == c.TOKEN_BOS:
            indexBOS = i
            break
    
    for i, token in enumerate(tokens):
        if token == c.TOKEN_EOS:
            indexEOS = i
            break

    if indexBOS == -1 and indexEOS == -1:
        return tokens

    retTokens = []
    for i, token in enumerate(tokens):
        if i >= indexEOS:
            break
        if i > indexBOS:
            retTokens.append(token)

    return retTokens
