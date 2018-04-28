# Chatbot George
Chatbot Based on Artificial Neural Networks.

### Usage
`py chatbot.py [-h|--help] [--mode=[train|chat|test]] [--model=<number>] [--dataLimit=<number>] [--testDataLimit=<number>] [--testing=[yes|no]] [--usw=[yes|no]] [--gui=[yes|no]]`

#### Options
| Parameter | Description |
| - | - |
| `-h`, `--help` | Show help. |
| `--mode=[train\|chat\|test]` | Training (default)/chatting/testing mode. |
| `--model=<number>` | Used model number (1 (default)/2/3). |
| `--dataLimit=<number>` | Limit for training data (\<number\> >= 100 \| \<number\> == 0 (no limit)). |
| `--testDataLimit=<number>` | Limit for testing data (\<number\> >= 1 \| \<number\> == 0 (no limit)). |
| `--testing=[yes\|no]` | Enable (default)/disable testing each training epoch. |
| `--usw=[yes\|no]` | Train model using (default)/without using saved model weights. |
| `--gui=[yes\|no]` | Chatting using (default)/without using GUI. |

#### Examples
`py chatbot.py --help`

`py chatbot.py --model=1 --dataLimit=1000 --testing=no --usw=no`

`py chatbot.py --mode=chat --model=1`

`py chatbot.py --mode=chat --model=1 --gui=no`

`py chatbot.py --mode=test --model=1 --testDataLimit=100`

### Before using
Download pretrained vectors for word representation from https://nlp.stanford.edu/projects/glove/ and unzip downloaded file in /data/glove folder. Then edit the appropriate constants in the `constants.py` file.

### Requirements
- Microsoft Windows 10
- Python 3.6.3

#### Libraries
- gensim 3.3.0
- graphviz 2.38
- h5py 2.7.1
- keras 2.1.4
- nltk 3.2.5
- numpy 1.14.0
- pydot 1.2.4
- pydot-ng 1.0.0
- pydotplus 2.0.2
- pyQt5 5.10.1
- python-dateutil 2.6.1
- scipy 1.0.0
- sklearn 0.0
- tensorflow 1.5.0
- tensorflow-tensorboard 1.5.1
- theano 1.0.1

### References and Credits
1. https://github.com/oswaldoludwig/Seq2seq-Chatbot-for-Keras
2. https://github.com/codedak/chatbot
3. https://github.com/bshao001/ChatLearner
