"""Script for transforming saved training or testing data from certain one file format to used format.

File: preprocessData.py
Author: Jiří Čechák
Date: 12.04.2018
Python Version: 3.6.3

Script transforms saved training or testing data in one file where line with context begins with 'Q: '
and line with utterance begins with 'A: '. Contexts and utterances are saved to two seperated file, 
context and corresponding utterance to lines with same number in each file.

Args:
    data to transform file path
    new file with contexts file path
    new file with utterances file path
"""

import re
import nltk
import sys

if len(sys.argv) != 4:
    print("Error: Bad format of program arguments.")
    sys.exit()

dataFilePath = sys.argv[1]
contextFilePath = sys.argv[2]
utteranceFilePath = sys.argv[3]

try:
    f = open(dataFilePath)
    fEnc = open(contextFilePath, "w")
    fDec = open(utteranceFilePath, "w")

    lastLine = None

    for line in f:
        
        if re.compile(r"^Q:\s+").match(line) or re.compile(r"^A:\s+").match(line):
            line = line.rstrip("\n")

            if re.compile(r"^Q:\s+").match(line):
                line = re.sub(r"^Q:\s+", "", line)

                if line != "":
                    lastLine = line

                else:
                    lastLine = None

            elif re.compile(r"^A:\s+").match(line):
                line = re.sub(r"^A:\s+", "", line)

                if lastLine != None and line != "":
                    fEnc.write("{}\n".format(lastLine))
                    fDec.write("{}\n".format(line))
                    
                lastLine = None
            
            else:
                lastLine = None

        else:
            lastLine = None


    f.close()
    fEnc.close()
    fDec.close()

except Exception as e:
    print(e)
