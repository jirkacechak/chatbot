"""Model training module.

File: train.py
Author: Jiří Čechák
Date: 12.04.2018
Python Version: 3.6.3

This module contains function for starting training of the selected model using training data.
"""

from __future__ import print_function
import numpy as np

import constants as c
from utils import fileExistsAndNotEmpty, printErrorAndExit, oneLinePrint
from dataUtils import loadDataAndTokenize, loadVocabulary, getEmbedding, getFileWithLastSavedWeights
from model import trainModel
from utils import oneLinePrint, printErrorAndExit


def train(modelNumber, dataLimit, useSavedWeights, testing):
    """Loads training data and trains model.

    Args:
        modelNumber: number of model to train
        dataLimit: limit for training data
        useSavedWeights: True if saved weight should be loaded into model, False otherwise
        testing: True if model should be tested on training and validation data using BLEU metrics during training, False otherwise
    """

    print("Training")

    vocabulary, wordToIndexVocabulary = loadVocabulary()

    savedWeightsFile = None
    epochNumber = 0
    dataSize = dataLimit

    if useSavedWeights:
        savedWeightsFile, dataSize, epochNumber = getFileWithLastSavedWeights(modelNumber, dataLimit)

        if savedWeightsFile == None:
            dataSize = dataLimit
            epochNumber = 0

    encTokens, decTokens = loadDataAndTokenize(
        c.CONTEXT_FILEPATH, c.UTTERANCE_FILEPATH, dataSize, wordToIndexVocabulary)

    if len(encTokens) < c.MIN_DATA_SIZE:
        printErrorAndExit(c.ERROR_MIN_DATA_SIZE)

    embedding = getEmbedding(modelNumber)
    
    trainModel(modelNumber, encTokens, decTokens, vocabulary, wordToIndexVocabulary, embedding, savedWeightsFile, epochNumber, testing)
