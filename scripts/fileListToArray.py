"""Creates string representing python's array from lines in file.

File: fileListToArray.py
Author: Jiří Čechák
Date: 12.04.2018
Python Version: 3.6.3

Creates string representing python's array from lines in file and saves it to another file.
Lines limit can be provided.

Args:
    path to file to convert to array
    path to file containing created string which represents python's array
    loaded line limit
"""

import re
import nltk
import sys

if len(sys.argv) != 3 and len(sys.argv) != 4:
    print("Error: Bad format of program arguments.")
    sys.exit()

file = sys.argv[1]
arrayFile = sys.argv[2]
limit = 0

if len(sys.argv) == 4:
    try:
        limit = int(sys.argv[3])
    except Exception as e:
        print("Error: Bad format of program arguments.")
        sys.exit()

try:
    f = open(file)
    array = []

    for i, line in enumerate(f):
        if limit != 0 and i >= limit:
            break
        array.append(re.sub(r"^\s*", "", re.sub(r"\s.*$", "", line)).lower())

    f.close()

    arrayString = '["{}"]'.format('", "'.join(array))

    try:
        f = open(arrayFile, "w")
        f.write(arrayString)
        f.close()

    except Exception as e:
        print(e)

except Exception as e:
    print(e)
