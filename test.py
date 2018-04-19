"""Model testing module.

File: test.py
Author: Jiří Čechák
Date: 12.04.2018
Python Version: 3.6.3

In this module is function for testing the selected trained model on testing data using BLEU metric.
"""

from __future__ import print_function
from time import time

from utils import printErrorAndExit, timestampToTime
import constants as c
from dataUtils import loadVocabulary, getFileWithLastSavedWeights, loadTestingDataAndTokenize, tokenizedInputToIds
from model import createModel, testBLEU


def test(modelNumber, dataLimit):
    """Testing on testing data using BLEU metrick.

    Args:
        modelNumber: number of a model to test
        dataLimit: limit for testing data
    """

    print("Testing")

    savedWeightsFile, _, _ = getFileWithLastSavedWeights(modelNumber, None)

    if savedWeightsFile == None:
        printErrorAndExit(c.ERROR_WEIGHTS_FILE_NOT_FOUND)

    vocabulary, wordToIndexVocabulary = loadVocabulary()

    encTokens, decTokens = loadTestingDataAndTokenize(
        c.TEST_CONTEXT_FILEPATH, c.TEST_UTTERANCE_FILEPATH, dataLimit, wordToIndexVocabulary)

    if len(encTokens) < c.MIN_TEST_DATA_SIZE:
        printErrorAndExit(c.ERROR_MIN_TEST_DATA_SIZE)

    encTokensIds = []

    for tokens in encTokens:
        encTokensIds.append(tokenizedInputToIds(tokens, wordToIndexVocabulary)[0])

    model = createModel(modelNumber, vocabulary, None, savedWeightsFile)

    print("")

    timeStart = time()

    bleuTestScore = testBLEU(encTokensIds, decTokens, model, vocabulary, text="Testing on testing data")

    print("BLEU testing score: {}".format(bleuTestScore))

    testDataFilepath = c.MODEL1_TESTDATA_FILEPATH if modelNumber == 1 else c.MODEL2_TESTDATA_FILEPATH if modelNumber == 2 else c.MODEL3_TESTDATA_FILEPATH

    try:
        testDataFile = open(testDataFilepath, "w")
        testDataFile.write("{}\n".format(bleuTestScore))
        testDataFile.close()
    except Exception as e:
        print(e)
    
    timeEnd = time()
    timeTotal = timeEnd - timeStart
    
    print("\nTOTAL TIME: {}".format(timestampToTime(timeTotal)))