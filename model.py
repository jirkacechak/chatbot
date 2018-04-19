"""Manages model and model testing.

File: model.py
Author: Jiří Čechák
Date: 12.04.2018
Python Version: 3.6.3

Manages work with model and model testing.
"""

from keras.layers import Input, LSTM, Embedding, Dense, Permute, RepeatVector, Activation, Flatten, Lambda, concatenate, multiply
from keras.optimizers import Adam
from keras.models import Model
from keras.utils import plot_model
from keras import backend
import numpy as np
import os
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from sklearn.model_selection import train_test_split
from time import time

import constants as c
from utils import oneLinePrint, printErrorAndExit, printDivider, clearConsoleLine, timestampToTime, fileExistsAndNotEmpty
from dataUtils import removeBOSEOS, getPaddedEnc, getPaddedDec
from data import outputSpecialCharacters, outputSpecialCharacters2, sentenceEndCharacters, names


def createModel(modelNumber, vocabulary, embedding, savedWeightsFile):
    """Creates model.

    Args:
        modelNumber: number of model
        vocabulary: index to word vocabulary
        embedding: word embedding
        savedWeightsFile: file with saved model weights or None
    
    Returns:
        created model
    """

    oneLinePrint("Creating model ... ")

    vocabularySize = len(vocabulary) + 1

    embeddingWordSize = c.MODEL1_EMBEDDING_WORD_SIZE if modelNumber == 1 else c.MODEL2_EMBEDDING_WORD_SIZE if modelNumber == 2 else c.MODEL3_EMBEDDING_WORD_SIZE
    embeddingSentenceSize = c.MODEL1_EMBEDDING_SENTENCE_SIZE if modelNumber == 1 else c.MODEL2_EMBEDDING_SENTENCE_SIZE if modelNumber == 2 else c.MODEL3_EMBEDDING_SENTENCE_SIZE

    if savedWeightsFile == None: # creating weights
        embeddingMatrix = np.zeros((vocabularySize, embeddingWordSize))

        for i, token in enumerate(vocabulary): # getting vectors representing given token
            tokenEmbedding = embedding.get(token[0])

            if tokenEmbedding is not None:
                embeddingMatrix[i] = tokenEmbedding

        embeddingLayer = Embedding(output_dim=embeddingWordSize, input_dim=vocabularySize, weights=[
            embeddingMatrix], input_length=c.MAX_TOKENS) # shared embedding layer

    else:
        embeddingLayer = Embedding(
            output_dim=embeddingWordSize, input_dim=vocabularySize, input_length=c.MAX_TOKENS)  # shared embedding layer (weights will be loaded)

    encInput = Input(shape=(c.MAX_TOKENS,), dtype="int32")
    decInput = Input(shape=(c.MAX_TOKENS,), dtype="int32")

    if modelNumber == 3: # attention
        embeddedInput = embeddingLayer(encInput)

        attention = Dense(1, activation='tanh')(embeddedInput)
        attention = Flatten()(attention)
        attention = Activation('softmax')(attention)
        attention = RepeatVector(embeddingWordSize)(attention)
        attention = Permute([2, 1])(attention)

        encLSTM = LSTM(embeddingSentenceSize, kernel_initializer="lecun_uniform")(
            multiply([embeddedInput, attention]))
    else:
        encLSTM = LSTM(embeddingSentenceSize, kernel_initializer="lecun_uniform")(
            embeddingLayer(encInput))

    decLSTM = LSTM(embeddingSentenceSize, kernel_initializer="lecun_uniform")(
        embeddingLayer(decInput))

    merged = concatenate([encLSTM, decLSTM], axis=1)

    out = None

    if modelNumber == 2:
        out = Dense(int(3 * vocabularySize / 4), activation="relu")(Dense(int(vocabularySize / 2),
                                                                          activation="relu")(Dense(int(vocabularySize / 4), activation="relu")(merged)))
    else:
        out = Dense(int(vocabularySize/2), activation="relu")(merged)

    out = Dense(vocabularySize, activation="softmax")(out)

    model = Model(inputs=[encInput, decInput], outputs=[out])

    model.compile(loss="categorical_crossentropy", optimizer=Adam(
        lr=c.LEARNING_RATE), metrics=["accuracy"])

    if savedWeightsFile != None:
        model.load_weights(savedWeightsFile) # loading saved weights from file

    modelImgFilePath = c.MODEL1_IMG_FILEPATH if modelNumber == 1 else c.MODEL2_IMG_FILEPATH if modelNumber == 2 else c.MODEL3_IMG_FILEPATH

    plot_model(model, to_file=modelImgFilePath, show_shapes=True) # ploting model structure

    print("done")

    return model


def getPrediction(sequence, model, vocabulary):
    """Returns predicted tokens.

    Args:
        sequence: context sequence
        model: model
        vocabulary: index to word vocabulary
    
    Returns:
        predicted tokens
    """

    decPartial = np.zeros((1, c.MAX_TOKENS))
    decPartial[0, -1] = 2 # token BOS has index 2 in vocabulary
    for k in range(c.MAX_TOKENS - 1):
        nextIdx = np.argmax(model.predict([sequence, decPartial])) # predicting next token index
        decPartial[0, 0:-1] = decPartial[0, 1:] # shifting present utterance
        decPartial[0, -1] = nextIdx # adding next token index

    out = []
    for k in decPartial[0]: # vocabulary indexes to tokens
        k = k.astype(int)
        if k < len(vocabulary) - 2:
            out.append(vocabulary[k][0])

    return out


def getPredictionString(sequence, model, vocabulary):
    """Returns predicted answer.

    Args:
        sequence: context sequence
        model: model
        vocabulary: index to word vocabulary
    
    Returns:
        predicted answer
    """

    prediction = getPrediction(sequence, model, vocabulary)

    text = ""
    lastToken = None

    for token in prediction:
        if token == c.TOKEN_BOS:
            continue

        if token == c.TOKEN_EOS:
            break

        if text != "" and not token in outputSpecialCharacters and not lastToken in outputSpecialCharacters2 and not token[0] == "'": # space not before tokens begining with ' and tokens it not belongs to and not behind tokens it not belongs to
            text += " "

        if lastToken == None or (lastToken in sentenceEndCharacters) or token in names: # capitalizing first letters in senteces and names
            text += token.capitalize()
        else:
            text += token

        lastToken = token

    return text


def getBleuScore(reference, hypothesis):
    """Returns BLEU score for given reference and hypothesis.

    Args:
        reference: utterance reference
        hypothesis: utterance hypothesis
    
    Returns:
        bleu score for hypothesis
    """

    if len(reference) == 0 and len(hypothesis) == 0:
        return 1

    weights = (0.25, 0.25, 0.25, 0.25) # initial weight is 4-gram

    if len(reference) < 4 or len(hypothesis) < 4: # adjusting weights to short reference or hypothesis
        if len(reference) == 0 or len(hypothesis) == 0:
            weights = (1,)
        elif len(reference) < len(hypothesis):
            weights = (1 / len(reference),) * len(reference)
        else:
            weights = (1 / len(hypothesis),) * len(hypothesis)

    return sentence_bleu([reference], hypothesis, smoothing_function=SmoothingFunction().method4, weights=weights) # calculating BLEU score for the hypothesis


def testBLEU(encData, decData, model, vocabulary, text="Testing"):
    """Returns data BLEU score.

    Args:
        encData: indexes of tokens of contexts
        decData: reference utterances
        model: model
        vocabulary: index to word vocabulary
        text: text to display as label while testing
    
    Returns:
        bleu score for predicted answers
    """

    bleuSum = 0

    for i, seq in enumerate(encData):

        bleuSum += getBleuScore(decData[i], removeBOSEOS(
            getPrediction(np.asarray([seq]), model, vocabulary)))
        
        oneLinePrint("{}: {} ({} / {})\t\r".format(text, bleuSum / (i + 1), i + 1, len(encData)))

    clearConsoleLine()

    return bleuSum / len(encData)


def trainModel(modelNumber, encTokens, decTokens, vocabulary, wordToIndexVocabulary, embedding, savedWeightsFile, epochNumber, testing):
    """Trains model.

    Args:
        modelNumber: number of model
        encTokens: tokens of contexts
        decTokens: tokens of utterances
        vocabulary: index to word vocabulary
        wordToIndexVocabulary: word to index vocabulary
        embedding: word embedding
        savedWeightsFile: file with saved model weights or None
        epochNumber: number of epoch to continue
        testing: True if model should be tested on training and validation data using BLEU metrics during training, False otherwise
    """

    vocabularySize = len(vocabulary) + 1
    dataSize = len(encTokens)

    testSize = c.MAX_TEST_SAMPLES if dataSize * \
        c.TEST_DATA_SIZE > c.MAX_TEST_SAMPLES else c.TEST_DATA_SIZE

    encTrainTokens, encTestTokens, decTrainTokens, decTestTokens = train_test_split(
        encTokens, decTokens, test_size=testSize, shuffle=False) # spliting to training and validation data

    encTrain = getPaddedEnc(encTrainTokens, wordToIndexVocabulary)
    decTrain = getPaddedDec(decTrainTokens, wordToIndexVocabulary)
    encTest = getPaddedEnc(encTestTokens, wordToIndexVocabulary)

    _, encTrainForTest, _, decTrainTokensForTest = train_test_split(
        encTrain, decTrainTokens, test_size=len(encTest), random_state=1, shuffle=True) # choosing training data for testing

    model = createModel(modelNumber, vocabulary, embedding, savedWeightsFile)

    subsetsNum = int(len(encTrain) / c.MAX_SAMPLES_PER_EPOCH) + 1

    step = int(np.around(len(encTrain) / subsetsNum)) # calculation of number of subsets
    stop = int(step * subsetsNum)

    trainDataFilepath = c.MODEL1_TRAINDATA_FILEPATH if modelNumber == 1 else c.MODEL2_TRAINDATA_FILEPATH if modelNumber == 2 else c.MODEL3_TRAINDATA_FILEPATH
    trainDataFile = None

    if not fileExistsAndNotEmpty(trainDataFilepath):
        try:
            trainDataFile = open(trainDataFilepath, "w")
            trainDataFile.write("{}{}{}{}{}{}{}{}{}\n".format(c.TRAIN_DATA_TEXT_EPOCH, c.CSV_SEPARATOR, c.TRAIN_DATA_TEXT_LOSS, c.CSV_SEPARATOR,
                                                              c.TRAIN_DATA_TEXT_ACCURACY, c.CSV_SEPARATOR, c.TRAIN_DATA_TEXT_BLEU_TRAIN, c.CSV_SEPARATOR, c.TRAIN_DATA_TEXT_BLEU_VALIDATE))
            trainDataFile.close()
        except Exception as e:
            print(e)

    print("\n\nTraining model {}".format(modelNumber))

    for iteration in range(epochNumber + 1, c.EPOCHS_NUM + 1):
        printDivider()
        print("\t\t\t\tEpoch {}/{}".format(iteration, c.EPOCHS_NUM))

        timeStart = time()

        subsetNum = 0
        lossSum = 0
        accuracySum = 0
        for n in range(0, stop, step): # iterate over subsets
            subsetNum += 1

            print("\n\t\t\t\tSubset {}/{}".format(subsetNum, subsetsNum))

            count = 0
            for i, sentence in enumerate(decTrain[n:n + step]):
                count += np.where(sentence == 3)[0][0] + 1 # token EOS is on index 3 in vocabulary

            enc = np.zeros((count, c.MAX_TOKENS)) # contexts
            dec = np.zeros((count, c.MAX_TOKENS)) # utterances
            out = np.zeros((count, vocabularySize)) # output will be next token

            encTrain2 = encTrain[n:n + step]
            count = 0
            for i, sentence in enumerate(decTrain[n:n + step]):
                decPartial = np.zeros((1, c.MAX_TOKENS))

                for k in range(1, np.where(sentence == 3)[0][0] + 1): # token EOS is on index 3 in vocabulary
                    outPart = np.zeros((1, vocabularySize)) # out layers has vocabulary size
                    outPart[0, sentence[k]] = 1 # output will be next token
                    decPartial[0, -k:] = sentence[0:k] # part of utterance padded from beginning
                    enc[count, :] = encTrain2[i:i + 1] # context to this utternace
                    dec[count, :] = decPartial # utterance to same place as context
                    out[count, :] = outPart # output will be next token
                    count += 1

            history = model.fit(
                [enc, dec], out, batch_size=c.BATCH_SIZE, epochs=1) # fit one subset

            lossSum += history.history["loss"][0]
            accuracySum += history.history["acc"][0]

        loss = lossSum / subsetNum
        accuracy = accuracySum / subsetNum

        print("\nLoss: {}".format(loss))
        print("Accuracy: {}".format(accuracy))

        timeEndTrain = time()

        if testing:
            decTrainTokensForTestModified = []

            for tokens in decTrainTokensForTest:
                decTrainTokensForTestModified.append(removeBOSEOS(tokens))

            bleuTrainScore = testBLEU(
                encTrainForTest, decTrainTokensForTestModified, model, vocabulary, "Testing on training data")

            print("BLEU train score: {}".format(bleuTrainScore))

            decTestTokensModified = []

            for tokens in decTestTokens:
                decTestTokensModified.append(removeBOSEOS(tokens))

            bleuTestScore = testBLEU(
                encTest, decTestTokensModified, model, vocabulary, "Testing on validation data")

            print("BLEU validation score: {}".format(bleuTestScore))

        weights_filepath_base = c.MODEL1_WEIGHTS_FILEPATH_BASE if modelNumber == 1 else c.MODEL2_WEIGHTS_FILEPATH_BASE if modelNumber == 2 else c.MODEL3_WEIGHTS_FILEPATH_BASE

        model.save_weights("{}-{}-{}{}".format(weights_filepath_base,
                                               dataSize, iteration, c.WEIGHTS_FILEPATH_SUFFIX), overwrite=True)

        try:
            trainDataFile = open(trainDataFilepath, "a")
            if testing:
                trainDataFile.write("{}{}{}{}{}{}{}{}{}\n".format(iteration, c.CSV_SEPARATOR, loss,
                                                                  c.CSV_SEPARATOR, accuracy, c.CSV_SEPARATOR, bleuTrainScore, c.CSV_SEPARATOR, bleuTestScore))
            else:
                trainDataFile.write("{}{}{}{}{}\n".format(
                    iteration, c.CSV_SEPARATOR, loss, c.CSV_SEPARATOR, accuracy))
            trainDataFile.close()
        except Exception as e:
            print(e)

        timeEnd = time()

        timeTotal = timeEnd - timeStart
        timeTraining = timeEndTrain - timeStart
        timeTesting = timeTotal - timeTraining

        if testing:
            print("\nTOTAL TIME: {} [training: {} | testing: {}]".format(timestampToTime(
                timeTotal), timestampToTime(timeTraining), timestampToTime(timeTesting)))
        else:
            print("\nTOTAL TIME: {}".format(timestampToTime(timeTotal)))
