"""Program constants.

File: constants.py
Author: Jiří Čechák
Date: 12.04.2018
Python Version: 3.6.3

Contains all constants used in program.
"""

# chatbot
CHATBOT_NAME = "George"                                                                         # chatbot's name

# sizes
MAX_TOKENS = 30                                                                                 # maximum tokens in sentence
MODEL1_EMBEDDING_WORD_SIZE = 300                                                                # word embedding size for first model (50/100/200/300)
MODEL2_EMBEDDING_WORD_SIZE = 300                                                                # word embedding size for second model (50/100/200/300)
MODEL3_EMBEDDING_WORD_SIZE = 300                                                                # word embedding size for third model (50/100/200/300)
MODEL1_EMBEDDING_SENTENCE_SIZE = 300                                                            # sentence embedding size for first model
MODEL2_EMBEDDING_SENTENCE_SIZE = 300                                                            # sentence embedding size for second model
MODEL3_EMBEDDING_SENTENCE_SIZE = 300                                                            # sentence embedding size for third model
MIN_DATA_SIZE = 100                                                                             # minimal number of training samples (context and utterance)
DEFAULT_DATA_LIMIT = 0                                                                          # default training data limit
MIN_TEST_DATA_SIZE = 1                                                                          # minimal number of testing samples (context and utterance)
DEFAULT_TEST_DATA_LIMIT = 0                                                                     # default testing data limit
MAX_SAMPLES_PER_EPOCH = 7000                                                                    # maximum number of samples (context and utterance) in one training epoch
TEST_DATA_SIZE = 0.05                                                                           # size of testing data part in training
MAX_TEST_SAMPLES = 1000                                                                         # maximum number of test samples (context and utterance) for training

# modes
MODE_TRAIN = "train"                                                                            # mode training
MODE_CHAT = "chat"                                                                              # mode chatting
MODE_TEST = "test"                                                                              # mode testing

# arguments
DEFAULT_MODE = MODE_TRAIN                                                                       # default chatbot mode ("train"/"chat"/"test")
DEFAULT_TESTING = True                                                                          # default enable/disable testing during training
DEFAULT_USW = True                                                                              # using/ignoring saved model weights for training
TEXT_ENABLE = "yes"                                                                             # text for enable in arguments
TEXT_DISABLE = "no"                                                                             # text for disable in arguments

# model
DEFAULT_MODEL = 1                                                                               # default model
NUMBER_OF_MODELS = 3                                                                            # total number of models

# training
EPOCHS_NUM = 100                                                                                # maximal number of training epochs
LEARNING_RATE = 0.00005                                                                         # learning rate
BATCH_SIZE = 128                                                                                # batch size used in training epoch
TRAIN_DATA_TEXT_EPOCH = "Epoch"                                                                 # label for column with epoch number in file with training data
TRAIN_DATA_TEXT_LOSS = "Loss"                                                                   # label for column with loss value in file with training data
TRAIN_DATA_TEXT_ACCURACY = "Accuracy"                                                           # label for column with accuracy value in file with training data
TRAIN_DATA_TEXT_BLEU_TRAIN = "BLEU training score"                                              # label for column with bleu training score in file with training data
TRAIN_DATA_TEXT_BLEU_VALIDATE = "BLEU validation score"                                         # label for column with bleu validation score in file with training data

# chatting
CONVERSATION_SENTENCE_LABEL_CHATBOT = CHATBOT_NAME                                              # label for chatbot's sentences in file with conversation
CONVERSATION_SENTENCE_LABEL_USER = "User"                                                       # label for user's sentences in file with conversation
DEFAULT_USE_CHAT_GUI = True                                                                     # use GUI in chat mode
CLEAR_CONSOLE_BEFORE_CHAT = True                                                                # clear console before chatting (chatting without GUI)
PRINT_CONSOLE_GREETING = True                                                                   # print chatbot's greeting when starting chatting in console (chatting without GUI)
PRINT_CONSOLE_GOODBYE = True                                                                    # print chatbot's goodbye when ending chatting in console (chatting without GUI)
PRINT_CONSOLE_INFO_MESSAGE = True                                                               # print info message when starting chatting in console (chatting without GUI)

# tokens
TOKEN_BOS = "BOS"                                                                               # token "Beginning Of Sentence"
TOKEN_EOS = "EOS"                                                                               # token "End Of Sentence"
TOKEN_UNKNOWN = "something"                                                                     # token to replace unknown tokens with
TOKEN_UNKNOWN_LIMIT = 1                                                                         # limit for unknown tokens in training sentences

# folders
DATA_DIR = "data/"                                                                              # data folder
GLOVE_DIR = DATA_DIR + "glove/"                                                                 # folder with GloVe embedding
MODEL1_DIR = DATA_DIR + "model1/"                                                               # folder with first model data
MODEL2_DIR = DATA_DIR + "model2/"                                                               # folder with second model data
MODEL3_DIR = DATA_DIR + "model3/"                                                               # folder with second model data

# files
VOCABULARY_FILEPATH = DATA_DIR + "vocabulary"                                                   # vocabulary filepath
CONTEXT_FILEPATH = DATA_DIR + "train.enc"                                                       # file with contexts for training
UTTERANCE_FILEPATH = DATA_DIR + "train.dec"                                                     # file with utterances for training
TEST_CONTEXT_FILEPATH = DATA_DIR + "test.enc"                                                   # file with contexts for testing
TEST_UTTERANCE_FILEPATH = DATA_DIR + "test.dec"                                                 # file with utterances for testing
MODEL1_GLOVE_FILEPATH = GLOVE_DIR + "glove.6B." + str(MODEL1_EMBEDDING_WORD_SIZE) + "d.txt"     # file with GloVe embedding of {MODEL1_EMBEDDING_WORD_SIZE} dimension for first model
MODEL2_GLOVE_FILEPATH = GLOVE_DIR + "glove.6B." + str(MODEL2_EMBEDDING_WORD_SIZE) + "d.txt"     # file with GloVe embedding of {MODEL2_EMBEDDING_WORD_SIZE} dimension for second model
MODEL3_GLOVE_FILEPATH = GLOVE_DIR + "glove.6B." + str(MODEL3_EMBEDDING_WORD_SIZE) + "d.txt"     # file with GloVe embedding of {MODEL3_EMBEDDING_WORD_SIZE} dimension for third model
MODEL1_WEIGHTS_FILEPATH_BASE = MODEL1_DIR + "modelWeights"                                      # filename base for file with saved weights for first model (number of training samples and epoch number will be added "modelWeights-{samples}-{epoch}" - e.g. model-1000-1)
MODEL2_WEIGHTS_FILEPATH_BASE = MODEL2_DIR + "modelWeights"                                      # filename base for file with saved weights for second model (number of training samples and epoch number will be added "modelWeights-{samples}-{epoch}" - e.g. model-1000-1)
MODEL3_WEIGHTS_FILEPATH_BASE = MODEL3_DIR + "modelWeights"                                      # filename base for file with saved weights for third model (number of training samples and epoch number will be added "modelWeights-{samples}-{epoch}" - e.g. model-1000-1)
WEIGHTS_FILEPATH_SUFFIX = ".h5"                                                                 # suffix for files with saved weights
MODEL1_IMG_FILEPATH = MODEL1_DIR + "model1.png"                                                 # first model image filepath
MODEL2_IMG_FILEPATH = MODEL2_DIR + "model2.png"                                                 # second model image filepath
MODEL3_IMG_FILEPATH = MODEL3_DIR + "model3.png"                                                 # third model image filepath
MODEL1_TRAINDATA_FILEPATH = MODEL1_DIR + "model1TrainData.csv"                                  # first model loss, accuracy and bleu score from training filepath
MODEL2_TRAINDATA_FILEPATH = MODEL2_DIR + "model2TrainData.csv"                                  # second model loss, accuracy and bleu score from training filepath
MODEL3_TRAINDATA_FILEPATH = MODEL3_DIR + "model3TrainData.csv"                                  # third model loss, accuracy and bleu score from training filepath
MODEL1_TESTDATA_FILEPATH = MODEL1_DIR + "model1TestData.txt"                                    # first model bleu score from testing filepath
MODEL2_TESTDATA_FILEPATH = MODEL2_DIR + "model2TestData.txt"                                    # second model bleu score from testing filepath
MODEL3_TESTDATA_FILEPATH = MODEL3_DIR + "model3TestData.txt"                                    # third model bleu score from testing filepath
MODEL1_CHATDATA_FILEPATH = MODEL1_DIR + "model1Conversation.txt"                                # first model conversation data from chatting filepath
MODEL2_CHATDATA_FILEPATH = MODEL2_DIR + "model2Conversation.txt"                                # second model conversation data from chatting filepath
MODEL3_CHATDATA_FILEPATH = MODEL3_DIR + "model3Conversation.txt"                                # third model conversation data from chatting filepath

# GUI
WINDOW_WIDTH_MIN = 300                                                                          # minimum GUI window width
WINDOW_HEIGHT_MIN = 300                                                                         # minimum GUI window height
WINDOW_WIDTH_DEFAULT = 400                                                                      # default GUI window width
WINDOW_HEIGHT_DEFAULT = 400                                                                     # default GUI window height
WINDOW_LABEL = "Chatbot {}".format(CHATBOT_NAME)                                                # GUI window label
BUTTON_LABEL = "Send"                                                                           # GUI send button label
BUTTON_FONT_SIZE = 16                                                                           # GUI send button font size
TEXT_INPUT_PLACEHOLDER = "Say something..."                                                     # GUI input text field placeholder
TEXT_INPUT_FONT_SIZE = 18                                                                       # GUI input text field font size
TEXT_AREA_TEXT_CHATBOT_FONT_SIZE = 23                                                           # GUI conversation text area chatbot's text font size
TEXT_AREA_TEXT_USER_FONT_SIZE = 18                                                              # GUI conversation text area user's text font size
TEXT_AREA_TEXT_CHATBOT_COLOR = "#0074D9"                                                        # GUI conversation text area chatbot's text color
TEXT_AREA_TEXT_USER_COLOR = "black"                                                             # GUI conversation text area user's text color

# errors
ERROR_ARGUMENTS = 1                                                                             # error in program arguments
ERROR_FILE = 2                                                                                  # error while handling file
ERROR_WEIGHTS_FILE_NOT_FOUND = 3                                                                # error when looking for file with saved weights
ERROR_MIN_DATA_SIZE = 4                                                                         # too few training data loaded error
ERROR_MIN_TEST_DATA_SIZE = 4                                                                    # too few testing data loaded error

# other
CSV_SEPARATOR = ","                                                                             # column seperator for csv files