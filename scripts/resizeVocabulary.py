"""Script for resizing vocabulary.

File: resizeVocabulary.py
Author: Jiří Čechák
Date: 12.04.2018
Python Version: 3.6.3

This script is for resizing selected vocabulary using selected training or testing data and parameters.

Args:
    vocabulary file path
    new vocabulary file path
    file with contexts file path
    file with utterances file path
"""

import nltk
import sys
import pickle

nltk.download('words')

MAX_TOKENS = 30
MIN_OCC = 50

def seqToTokens(seq):
    """Returns tokenized sequence.

    Args:
        seq: text sequence
    
    Returns:
        Tokenized sequence.
    """

    return nltk.word_tokenize(seq.lower())


def loadVocabulary(vocabularyFilePath):
    """Loads vocabulary.

    Returns:
        index to word vocabulary
        word to index wocabulary
    """

    try:
        file = open(vocabularyFilePath, 'rb')
    except Exception as e:
        print(e)
        sys.exit()

    vocabulary = pickle.load(file)
    file.close()

    indexToWord = [v[0] for v in vocabulary]

    return vocabulary, dict([(w, i) for i, w in enumerate(indexToWord)])

if len(sys.argv) != 5:
    print("Error: Bad format of program arguments.")
    sys.exit()

vocabularyFilePath = sys.argv[1]
newVocabularyFilePath = sys.argv[2]
contextFilePath = sys.argv[3]
utteranceFilePath = sys.argv[4]

try:
    vocabulary, wordToIndex = loadVocabulary(vocabularyFilePath)
    
    newVocabulary = list(vocabulary)
    
    encFile = open(contextFilePath)
    decFile = open(utteranceFilePath)

    tokensDict = dict()
    
    i = 0
    j = 0
    for encLine, decLine in zip(encFile, decFile):
        encLine = encLine.rstrip("\n")
        decLine = decLine.rstrip("\n")

        encTokens = seqToTokens(encLine)
        decTokens = seqToTokens(decLine)
        
        if len(encTokens) > 0 and len(encTokens) <= MAX_TOKENS and len(decTokens) > 0 and len(decTokens) + 2 <= MAX_TOKENS:
            for token in encTokens:
                if token not in wordToIndex:
                    if token in tokensDict:
                        tokensDict[token] += 1
                    else:
                        tokensDict[token] = 1

            for token in decTokens:
                if token not in wordToIndex:
                    if token in tokensDict:
                        tokensDict[token] += 1
                    else:
                        tokensDict[token] = 1
            j += 1

        i += 1

        if i % 1000 == 0:
            print("\r{}/{}".format(j, i), end="")

    encFile.close()
    decFile.close()

    print("\r\t\t\t\t\t\r", end="")

    tokensKeys = []
    tokensKeysChecked = []

    j = 0
    while len(tokensKeys) != len(tokensDict):
        maxKey = None
        maxValue = 0

        for key, value in tokensDict.items():
            if value > maxValue and key not in tokensKeys:
                maxKey = key
                maxValue = value

        if maxValue < MIN_OCC:
            break

        tokensKeys.append(maxKey)

        if maxKey in nltk.corpus.words.words():
            tokensKeysChecked.append(maxKey)
        
        for i, item in enumerate(newVocabulary):
            if item[1] < maxValue:
                newVocabulary.insert(i, (maxKey, maxValue))
                break
            
            if i >= len(newVocabulary) - 1:
                newVocabulary.append((maxKey, maxValue))
                break
        
        j += 1

        if j % 100 == 0:
            print("\r{}/{}".format(j, len(tokensDict)), end="")
        
    print("\r\t\t\t\t\t\r", end="")
                
    print("\nTOTAL: added: {} / loaded: {} / all: {}".format(len(tokensKeysChecked),
                                         len(tokensKeys), len(tokensDict)))
    
    print("OLD SIZE: {}".format(len(vocabulary)))
    print("NEW SIZE: {}".format(len(newVocabulary)))

    file = open(newVocabularyFilePath, 'wb')

    pickle.dump(newVocabulary, file, protocol=pickle.HIGHEST_PROTOCOL)

    file.close()

except Exception as e:
    print(e)
