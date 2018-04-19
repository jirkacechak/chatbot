"""Generates some introductions, introduction demands and other similar dialogs using chatbot's name.

File: dialogGenerator.py
Author: Jiří Čechák
Date: 12.04.2018
Python Version: 3.6.3

Generates some introductions, introduction demands and other similar dialogs using chatbot's name.
Generated sentences are saved to context and utterance files.

Args:
    file with contexts file path
    file with utterances file path
"""

from random import randint
import nltk
import sys

CHATBOT_NAME = "George"
TOKEN_UNKNOWN = "something"
MAX_TOKENS = 30

names = ["james", "john", "robert", "michael", "mary", "william", "david", "richard", "charles", "joseph", "thomas", "patricia", "christopher", "linda", "barbara", "daniel", "paul", "mark", "elizabeth", "donald", "jennifer", "george", "maria", "kenneth", "susan", "steven", "edward", "margaret", "brian", "ronald", "dorothy", "anthony", "lisa", "kevin", "nancy", "karen", "betty", "helen", "jason", "matthew", "gary", "timothy", "sandra", "jose", "larry", "jeffrey", "frank", "donna", "carol", "ruth", "scott", "eric", "stephen", "andrew", "sharon", "michelle", "laura", "sarah", "kimberly", "deborah", "jessica", "raymond", "shirley", "cynthia", "angela", "melissa", "brenda", "amy", "jerry", "gregory", "anna", "joshua", "virginia", "rebecca", "kathleen", "dennis", "pamela", "martha", "debra", "amanda", "walter", "stephanie", "willie", "patrick", "terry", "carolyn", "peter", "christine", "marie", "janet", "frances", "catherine", "harold", "henry", "douglas", "joyce", "ann", "diane", "alice", "jean", "julie", "carl", "kelly", "heather", "arthur", "teresa", "gloria", "doris", "ryan", "joe", "roger", "evelyn", "juan", "ashley", "jack", "cheryl", "albert", "joan", "mildred", "katherine", "justin", "jonathan", "gerald", "keith", "samuel", "judith", "rose", "janice", "lawrence", "ralph", "nicole", "judy", "nicholas", "christina", "roy", "kathy", "theresa", "benjamin", "beverly", "denise", "bruce", "brandon", "adam", "tammy", "irene", "fred", "billy", "harry", "jane", "wayne", "louis", "lori", "steve", "tracy", "jeremy", "rachel", "andrea", "aaron", "marilyn", "robin", "randy", "leslie", "kathryn", "eugene", "bobby", "howard", "carlos", "sara", "louise", "jacqueline", "anne", "wanda", "russell", "shawn", "victor", "julia", "bonnie", "ruby", "chris", "tina", "lois", "phyllis", "jamie", "norma", "martin", "paula", "jesse", "diana", "annie", "shannon", "ernest", "todd", "phillip", "lee", "lillian", "peggy", "emily", "crystal", "kim", "craig", "carmen", "gladys", "connie", "rita", "alan", "dawn", "florence", "dale", "sean", "francis", "johnny", "clarence", "philip", "edna", "tiffany", "tony", "rosa", "jimmy", "earl", "cindy", "antonio", "luis", "mike", "danny", "bryan", "grace", "stanley", "leonard", "wendy", "nathan", "manuel", "curtis", "victoria", "rodney", "norman", "edith", "sherry", "sylvia", "josephine", "allen", "thelma", "sheila", "ethel", "marjorie", "lynn", "ellen", "elaine", "marvin", "carrie", "marion", "charlotte", "vincent", "glenn", "travis", "monica", "jeffery", "jeff", "esther", "pauline", "jacob", "emma", "chad", "kyle", "juanita", "dana", "melvin", "jessie", "rhonda", "anita", "alfred", "hazel", "amber", "eva", "bradley", "ray", "jesus", "debbie", "herbert", "eddie", "joel", "frederick", "april", "lucille", "clara", "gail", "joanne", "eleanor", "valerie", "danielle", "erin", "edwin", "megan", "alicia", "suzanne", "michele", "don", "bertha", "veronica", "jill", "darlene", "ricky", "lauren", "geraldine", "troy", "stacy", "randall", "cathy", "joann", "sally", "lorraine", "barry", "alexander", "regina", "jackie", "erica", "beatrice", "dolores", "bernice", "mario", "bernard", "audrey", "yvonne", "francisco", "micheal", "leroy", "june", "annette", "samantha", "marcus", "theodore", "oscar", "clifford", "miguel", "jay", "renee", "ana", "vivian", "jim", "ida", "tom", "ronnie", "roberta", "holly", "brittany", "angel", "alex", "melanie", "jon", "yolanda", "tommy", "loretta", "jeanette", "calvin", "laurie", "leon", "katie", "stacey", "lloyd", "derek", "bill", "vanessa", "sue", "kristen", "alma", "warren", "elsie", "beth", "vicki", "jeanne", "jerome", "darrell", "tara", "rosemary", "leo", "floyd", "dean", "carla", "wesley", "terri", "eileen", "courtney", "alvin", "tim", "jorge", "greg", "gordon", "pedro", "lucy", "gertrude", "dustin", "derrick", "corey", "tonya", "dan", "ella", "lewis", "zachary", "wilma", "maurice", "kristin", "gina", "vernon", "vera", "roberto", "natalie", "clyde", "agnes", "herman", "charlene", "charlie", "bessie", "shane", "delores", "sam", "pearl", "melinda", "hector", "glen", "arlene", "ricardo", "tamara", "maureen", "lester", "gene", "colleen", "allison", "tyler", "rick", "joy", "johnnie", "georgia", "constance", "ramon", "marcia", "lillie", "claudia", "brent", "tanya", "nellie", "minnie", "gilbert", "marlene", "heidi", "glenda", "marc", "viola", "marian", "lydia", "billie", "stella", "guadalupe", "caroline", "reginald", "dora", "jo", "cecil", "casey", "brett", "vickie", "ruben", "jaime", "rafael", "nathaniel", "mattie", "milton", "edgar", "raul", "maxine", "irma", "myrtle", "marsha", "mabel", "chester", "ben", "andre", "adrian", "lena", "franklin", "duane", "christy", "tracey", "patsy", "gabriel", "deanna", "jimmie", "hilda", "elmer", "christian", "bobbie", "gwendolyn", "nora", "mitchell", "jennie", "brad", "ron", "roland", "nina", "margie", "leah", "harvey", "cory", "cassandra",
         "arnold", "priscilla", "penny", "naomi", "kay", "karl", "jared", "carole", "olga", "jan", "brandy", "lonnie", "leona", "dianne", "claude", "sonia", "jordan", "jenny", "felicia", "erik", "lindsey", "kerry", "darryl", "velma", "neil", "miriam", "becky", "violet", "kristina", "javier", "fernando", "cody", "clinton", "tyrone", "toni", "ted", "rene", "mathew", "lindsay", "julio", "darren", "misty", "mae", "lance", "sherri", "shelly", "sandy", "ramona", "pat", "kurt", "jody", "daisy", "nelson", "katrina", "erika", "claire", "allan", "hugh", "guy", "clayton", "sheryl", "max", "margarita", "geneva", "dwayne", "belinda", "felix", "faye", "dwight", "cora", "armando", "sabrina", "natasha", "isabel", "everett", "ada", "wallace", "sidney", "marguerite", "ian", "hattie", "harriet", "rosie", "molly", "kristi", "ken", "joanna", "iris", "cecilia", "brandi", "bob", "blanche", "julian", "eunice", "angie", "alfredo", "lynda", "ivan", "inez", "freddie", "dave", "alberto", "madeline", "daryl", "byron", "amelia", "alberta", "sonya", "perry", "morris", "monique", "maggie", "kristine", "kayla", "jodi", "janie", "isaac", "genevieve", "candace", "yvette", "willard", "whitney", "virgil", "ross", "opal", "melody", "maryann", "marshall", "fannie", "clifton", "alison", "susie", "shelley", "sergio", "salvador", "olivia", "luz", "kirk", "flora", "andy", "verna", "terrance", "seth", "mamie", "lula", "lola", "kristy", "kent", "beulah", "antoinette", "terrence", "gayle", "eduardo", "pam", "kelli", "juana", "joey", "jeannette", "enrique", "donnie", "candice", "wade", "hannah", "frankie", "bridget", "austin", "stuart", "karla", "evan", "celia", "vicky", "shelia", "patty", "nick", "lynne", "luther", "latoya", "fredrick", "della", "arturo", "alejandro", "wendell", "sheri", "marianne", "julius", "jeremiah", "shaun", "otis", "kara", "jacquelyn", "erma", "blanca", "angelo", "alexis", "trevor", "roxanne", "oliver", "myra", "morgan", "luke", "leticia", "krista", "homer", "gerard", "doug", "cameron", "sadie", "rosalie", "robyn", "kenny", "ira", "hubert", "brooke", "bethany", "bernadette", "bennie", "antonia", "angelica", "alexandra", "adrienne", "traci", "rachael", "nichole", "muriel", "matt", "mable", "lyle", "laverne", "kendra", "jasmine", "ernestine", "chelsea", "alfonso", "rex", "orlando", "ollie", "neal", "marcella", "loren", "krystal", "ernesto", "elena", "carlton", "blake", "angelina", "wilbur", "taylor", "shelby", "rudy", "roderick", "paulette", "pablo", "omar", "noel", "nadine", "lorenzo", "lora", "leigh", "kari", "horace", "grant", "estelle", "dianna", "willis", "rosemarie", "rickey", "mona", "kelley", "doreen", "desiree", "abraham", "rudolph", "preston", "malcolm", "kelvin", "johnathan", "janis", "hope", "ginger", "freda", "damon", "christie", "cesar", "betsy", "andres", "wm", "tommie", "teri", "robbie", "meredith", "mercedes", "marco", "lynette", "eula", "cristina", "archie", "alton", "sophia", "rochelle", "randolph", "pete", "merle", "meghan", "jonathon", "gretchen", "gerardo", "geoffrey", "garry", "felipe", "eloise", "ed", "dominic", "devin", "cecelia", "carroll", "raquel", "lucas", "jana", "henrietta", "gwen", "guillermo", "earnest", "delbert", "colin", "alyssa", "tricia", "tasha", "spencer", "rodolfo", "olive", "myron", "jenna", "edmund", "cleo", "benny", "sophie", "sonja", "silvia", "salvatore", "patti", "mindy", "may", "mandy", "lowell", "lorena", "lila", "lana", "kellie", "kate", "jewel", "gregg", "garrett", "essie", "elvira", "delia", "darla", "cedric", "wilson", "sylvester", "sherman", "shari", "roosevelt", "miranda", "marty", "marta", "lucia", "lorene", "lela", "josefina", "johanna", "jermaine", "jeannie", "israel", "faith", "elsa", "dixie", "camille", "winifred", "wilbert", "tami", "tabitha", "shawna", "rena", "ora", "nettie", "melba", "marina", "leland", "kristie", "forrest", "elisa", "ebony", "alisha", "aimee", "tammie", "simon", "sherrie", "sammy", "ronda", "patrice", "owen", "myrna", "marla", "latasha", "irving", "dallas", "clark", "bryant", "bonita", "aubrey", "addie", "woodrow", "stacie", "rufus", "rosario", "rebekah", "marcos", "mack", "lupe", "lucinda", "lou", "levi", "laurence", "kristopher", "jewell", "jake", "gustavo", "francine", "ellis", "drew", "dorthy", "deloris", "cheri", "celeste", "cara", "adriana", "adele", "abigail", "trisha", "trina", "tracie", "sallie", "reba", "orville", "nikki", "nicolas", "marissa", "lourdes", "lottie", "lionel", "lenora", "laurel", "kerri", "kelsey", "karin", "josie", "janelle", "ismael", "helene", "gilberto", "gale", "francisca", "fern", "etta", "estella", "elva", "effie", "dominique", "corinne", "clint", "brittney", "aurora", "wilfred", "tomas", "toby", "sheldon", "santos", "maude", "lesley", "josh", "jenifer", "iva", "ingrid", "ina", "ignacio", "hugo", "goldie", "eugenia", "ervin", "erick", "elisabeth", "dewey", "christa", "cassie", "cary", "caleb", "caitlin", "bettie"]

greetings = ["hi", "hi!", "hi there", "hi there!", "hello", "hello!", "hey", "hey!", "hey hey", "hey hey!", "howdy", "howdy!", "hallo", "hallo!",
             "ciao", "ciao!", "see you", "see you!", "good morning", "good morning!", "good afternoon", "good afternoon!", "good evening", "good evening!"]

specialGreetings = ["good morning", "good morning!", "good afternoon",
                    "good afternoon!", "good evening", "good evening!"]

goodbyes = ["bye", "bye!", "bye bye", "bye bye!", "goodbye", "goodbye!", "see you later", "see you later!", "see you soon", "see you soon!", "talk to you later", "i'm off", "have a nice day", "have a nice day!",
            "have a good day", "have a good day!", "i look forward to our next meeting", "take care", "take care!", "it was nice to see you again", "it was nice seeing you", "good night", "later", "laters", "catch you later"]

introductions = ["i am", "i'm", "my name is", "my first name is", "everybody calls me",
                 "call me", "please, call me", "you can call me", "they call me"]

introductionsDemands = ["what is your name?", "what's your name?", "what was your name?", "what was your name again?", "can you tell me your name?", "tell me your name", "tell me your first name", "name?", "name, please?", "name", "name, please", "your name", "do you have name?", "do you have any name?", "who might you be?", "who might you be, please?", "have you got name?", "have you got any name?", "your name?", "your name, please", "your name, please?", "tell me your name, please", "please, tell me your name", "you are...", "and you are...", "tell me your first name, please",
                        "please, tell me your first name", "can you tell me your name, please?", "who are you?", "who you?", "who are you, please?", "who you, please?", "who you are?", "who you are, please?", "how can i call you?", "how should i call you?", "how do they call you?", "you are?", "you are who?", "and you are?", "and you are who?", "your name is?", "and your name is?", "your first name?", "your first name is?", "and your first name is?", "first name", "first name, please", "first name?", "first name, please?", "introduce yourself", "please, introduce yourself", "introduce yourself, please"]

introductionsAnswer = ["nice to meet you", "it is nice to meet you", "it's nice to meet you", "nice name", "beautiful name", "you have beautiful name",
                       "pleased to meet you", "it's a pleasure to meet you", "pleasure to meet you", "lovely to meet you", "glad to meet you"]

honorificPhrases = ["how are you?", "how are you today?", "how are you doing?", "how are you doing today?", "how you doing?", "how's everything?", "how's everything today?", "how are things?", "how are things today?", "how's life?", "how's life today?", "you good?", "you ok?",
                    "how's your day?", "how's your day going?", "how you doing today?", "how's it going?", "how's it going today?", "what's up?", "what's new?", "what's going on?", "what's going on today?", "good to see you", "nice to see you", "how do you do?", "how do you do today?"]

honorificPhrasesAnswers = ["i am fine", "i am fine, thanks", "i am fine, thank you", "i'm fine", "i'm fine, thanks", "i'm fine, thank you", "i am good", "i am good, thank you", "i'm doing great", "i'm doing great today",
                           "i'm doing great, thanks", "doing well", "doing well, thank you", "thanks for asking, i'm doing fine", "everything is fine today", "everything is fine, thanks", "i'm alright", "i am alright, thanks"]

nameQuestions = ["is your name", "your name is", "are you", "you are",
                 "they call you", "everyone calls you", "you are called", "are you called"]

nameQuestionsAnswers = ["yes", "yes, i am", "yes, i'm", "i am", "i'm", "it's me", "it is me", "yes, it's me", "yes, it is me", "yes, who are you?", "yes, i am and who are you?", "yes, i'm. tell me your name",
                        "i am, who asks?", "i'm. what is your name?", "it's me. can you tell me your name?", "it is me. tell me your name, please", "yes, it's me. how can i call you?", "yes, it is me. what's your name?"]

nameAnswers = ["it's me", "it is me", "yes, it's me", "yes, it is me", "yes, who are you?", "it's me. can you tell me your name?", "it is me. tell me your name, please", "yes, it's me. how can i call you?", "it is my name", "it's my name",
               "yes, it is my name", "yes, it's my name", "yes, it is me. what's your name?", "i am {}".format(CHATBOT_NAME), "i'm {}".format(CHATBOT_NAME), "yes, my name is {}".format(CHATBOT_NAME), "i am {}".format(CHATBOT_NAME), "yes, i'm {}".format(CHATBOT_NAME)]

wrongNameAnswers = ["it's not me", "it is not me", "no, it's not me", "no, it is not me", "no, not me, who are you?", "it's not me. can you tell me your name?", "it is not me. tell me your name, please", "no, it's not me. how can i call you?", "it is not my name",
                    "it's not my name", "no, it is not my name", "no, it's not my name", "no, it is not me. what's your name?", "i am {}".format(CHATBOT_NAME), "i'm {}".format(CHATBOT_NAME), "no, my name is {}".format(CHATBOT_NAME), "i am {}".format(CHATBOT_NAME), "no, i'm {}".format(CHATBOT_NAME)]

wrongNameQuestionsAnswersWithName = ["no, i'm", "no, i am", "no, my name", "no, call me",
                                     "no, i am not. My name is", "no, i'm not. My name is", "no, i am not. i am", "no, i'm not. i'm"]

notUnderstand = ["What?", "I do not understand.", "What? I do not understand.", "Again?", "What did you say?", "That is too complicated.", "That's too complicated.", "That is too complicated for me.",
                 "That's too complicated for me.", "That does not make any sense.", "That does not make any sense for me.", "Can you repeat it?", "Can you repeat it, please?", "It makes no sense at all.", "It makes no sense at all for me."]

sentenceEndCharacters = [".", "!", "?"]


def seqToTokens(seq):
    """Tokenize text sequence.

    Args:
        seq: text sequence for tokenization
    
    Returns:
        tokenized sequence
    """

    return nltk.word_tokenize(seq)


def randomDotOrComma():
    """Returns dot or comma randomly."""

    if randint(0, 1):
        return ","
    else:
        return "."


def randomSeperatorBasedOnEnd(text):
    """Randomly generates separator before text.

    Args:
        text: text to generate separator before

    Returns:
        new text
    """

    if text[len(text) - 1] in sentenceEndCharacters:
        return " "

    else:
        return "{} ".format(randomDotOrComma())


def generateIntroductionPair(name):
    """Generates introduction demand and introduction pair.
    Args:
        name: some name

    Returns:
        introduction demand and introduction pair
    """

    while True:
        greetingIndex = randint(0, len(greetings) * 2 - 1)
        introductionsIndex = randint(0, len(introductions) - 1)
        introductionsDemandsIndex = randint(
            0, len(introductionsDemands) * 2 - 1)
        honorificPhrasesIndex = randint(0, len(honorificPhrases) * 2 - 1)

        context = ""

        if greetingIndex < len(greetings):
            context += greetings[greetingIndex]

        if context != "":
            context += randomSeperatorBasedOnEnd(context)

        if honorificPhrasesIndex < len(honorificPhrases):
            context += "{}".format(honorificPhrases[honorificPhrasesIndex])

            if context != "":
                context += randomSeperatorBasedOnEnd(context)

        context += "{} {}".format(
            introductions[introductionsIndex], name)

        if introductionsDemandsIndex < len(introductionsDemands):
            context += "{} {}".format(randomDotOrComma(),
                                      introductionsDemands[introductionsDemandsIndex])

        if len(seqToTokens(context)) <= MAX_TOKENS:
            break

    contextGreetingIndex = greetingIndex
    contextHonorificPhrasesIndex = honorificPhrasesIndex

    while True:
        greetingIndex = randint(0, len(greetings) * 2 - 1)

        if contextGreetingIndex < len(greetings) and greetingIndex < len(greetings) and greetings[greetingIndex] in specialGreetings and greetings[greetingIndex] != greetings[contextGreetingIndex] and "{}!".format(greetings[greetingIndex]) != greetings[contextGreetingIndex] and greetings[greetingIndex] != "{}!".format(greetings[contextGreetingIndex]):
            continue

        introductionsIndex = randint(0, len(introductions) - 1)
        introductionsAnswerIndex = randint(0, len(introductionsAnswer) * 2 - 1)
        honorificPhrasesAnswersIndex = randint(
            0, len(honorificPhrasesAnswers) * 2 - 1)
        honorificPhrasesIndex = randint(0, len(honorificPhrases) * 2 - 1)

        answer = ""

        if greetingIndex < len(greetings):
            answer += greetings[greetingIndex]

        if answer != "":
            answer += randomSeperatorBasedOnEnd(answer)

        if honorificPhrasesAnswersIndex < len(honorificPhrasesAnswers) and contextHonorificPhrasesIndex < len(honorificPhrases):
            answer += "{}".format(
                honorificPhrasesAnswers[honorificPhrasesAnswersIndex])

            if answer != "":
                answer += randomSeperatorBasedOnEnd(answer)

        if introductionsAnswerIndex < len(introductionsAnswer):
            answer += "{}".format(
                introductionsAnswer[introductionsAnswerIndex])

            if answer != "":
                answer += randomSeperatorBasedOnEnd(answer)

        answer += "{} {}".format(
            introductions[introductionsIndex], CHATBOT_NAME)

        if honorificPhrasesIndex < len(honorificPhrases):
            answer += "{} {}".format(randomDotOrComma(),
                                     honorificPhrases[honorificPhrasesIndex])

        if answer[len(answer) - 1] not in sentenceEndCharacters:
            answer += "."

        if len(seqToTokens(answer)) <= MAX_TOKENS:
            break

    return context, answer


def generateIntroductions():
    """Returns generated introduction demands and introductions."""

    contexts = []
    answers = []

    for name in names:
        context, answer = generateIntroductionPair(name)
        contexts.append(context)
        answers.append(answer)

    return contexts, answers


def generateIntroductionsDemands():
    """Returns generated introduction demands."""

    contexts = []
    answers = []

    for introductionsDemand in introductionsDemands:
        contexts.append(introductionsDemand)
        answers.append("{} {}".format(
            introductions[randint(0, len(introductions) - 1)], CHATBOT_NAME))

    return contexts, answers


def generateGreetings():
    """Returns generated greetings."""

    contexts = []
    answers = []

    for i, greeting in enumerate(greetings):
        if greeting[len(greeting) - 1] not in sentenceEndCharacters:
            contexts.append("{}, {}".format(greeting, CHATBOT_NAME))

            while True:
                greetingIndex = randint(0, len(greetings) - 1)

                if not (i < len(greetings) and greetingIndex < len(greetings) and greetings[greetingIndex] in specialGreetings and greetings[greetingIndex] != greetings[i] and "{}!".format(greetings[greetingIndex]) != greetings[i] and greetings[greetingIndex] != "{}!".format(greetings[i])):
                    break

            answers.append(greetings[greetingIndex])

    for i, greeting in enumerate(greetings):
        if greeting[len(greeting) - 1] not in sentenceEndCharacters:
            contexts.append("{}, {}{} {}".format(greeting, CHATBOT_NAME, randomDotOrComma(
            ), honorificPhrases[randint(0, len(honorificPhrases) - 1)]))

            while True:
                greetingIndex = randint(0, len(greetings) - 1)

                if not (i < len(greetings) and greetingIndex < len(greetings) and greetings[greetingIndex] in specialGreetings and greetings[greetingIndex] != greetings[i] and "{}!".format(greetings[greetingIndex]) != greetings[i] and greetings[greetingIndex] != "{}!".format(greetings[i])):
                    break

            answer = greetings[greetingIndex]

            if answer[len(answer) - 1] not in sentenceEndCharacters:
                answer += randomDotOrComma()

            answer += " {}".format(
                honorificPhrasesAnswers[randint(0, len(honorificPhrasesAnswers) - 1)])

            answers.append(answer)

    return contexts, answers


def generateWrongGreetings():
    """Returns generated wrong greetings."""

    contexts = []
    answers = []

    for i, greeting in enumerate(greetings):
        if greeting[len(greeting) - 1] not in sentenceEndCharacters:
            while True:
                name = names[randint(0, len(names) - 1)]
                if name != CHATBOT_NAME:
                    break

            contexts.append("{}, {}".format(greeting, name))

            while True:
                greetingIndex = randint(0, len(greetings) - 1)

                if not (i < len(greetings) and greetingIndex < len(greetings) and greetings[greetingIndex] in specialGreetings and greetings[greetingIndex] != greetings[i] and "{}!".format(greetings[greetingIndex]) != greetings[i] and greetings[greetingIndex] != "{}!".format(greetings[i])):
                    break

            answer = greetings[greetingIndex]

            if answer[len(answer) - 1] not in sentenceEndCharacters:
                answer += ", but"

            answer += " {} {}".format(
                introductions[randint(0, len(introductions) - 1)], CHATBOT_NAME)

            answers.append(answer)

    for i, greeting in enumerate(greetings):
        if greeting[len(greeting) - 1] not in sentenceEndCharacters:
            while True:
                name = names[randint(0, len(names) - 1)]
                if name != CHATBOT_NAME:
                    break

            contexts.append("{}, {}{} {}".format(greeting, name, randomDotOrComma(
            ), honorificPhrases[randint(0, len(honorificPhrases) - 1)]))

            while True:
                greetingIndex = randint(0, len(greetings) - 1)

                if not (i < len(greetings) and greetingIndex < len(greetings) and greetings[greetingIndex] in specialGreetings and greetings[greetingIndex] != greetings[i] and "{}!".format(greetings[greetingIndex]) != greetings[i] and greetings[greetingIndex] != "{}!".format(greetings[i])):
                    break

            answer = greetings[greetingIndex]

            if answer[len(answer) - 1] not in sentenceEndCharacters:
                answer += ", but"

            answer += " {} {}".format(
                introductions[randint(0, len(introductions) - 1)], CHATBOT_NAME)

            answers.append(answer)

    return contexts, answers


def generateGoodbyes():
    """Returns generated goodbyes."""

    contexts = []
    answers = []

    for goodbye in goodbyes:
        if goodbye[len(goodbye) - 1] not in sentenceEndCharacters:
            contexts.append("{}, {}".format(goodbye, CHATBOT_NAME))
            answers.append(goodbyes[randint(0, len(goodbyes) - 1)])

    return contexts, answers


def generateWrongGoodbyes():
    """Returns generated wrong greetings."""

    contexts = []
    answers = []

    linker = ["but", "for the next time...", "but for the next time..."]

    for goodbye in goodbyes:
        if goodbye[len(goodbye) - 1] not in sentenceEndCharacters:
            while True:
                name = names[randint(0, len(names) - 1)]
                if name != CHATBOT_NAME:
                    break

            contexts.append("{}, {}".format(goodbye, name))

            answer = goodbyes[randint(0, len(goodbyes) - 1)]

            if answer[len(answer) - 1] not in sentenceEndCharacters:
                answer += randomDotOrComma()

            answer += " {}".format(linker[randint(0, len(linker) - 1)])

            answer += " {} {}".format(
                introductions[randint(0, len(introductions) - 1)], CHATBOT_NAME)

            answers.append(answer)

    return contexts, answers


def generateNameQuestions():
    """Returns generated name questions."""

    contexts = []
    answers = []

    for goodbye in goodbyes:
        if goodbye[len(goodbye) - 1] not in sentenceEndCharacters:
            contexts.append("{} {}?".format(
                nameQuestions[randint(0, len(nameQuestions) - 1)], CHATBOT_NAME))
            answers.append(nameQuestionsAnswers[randint(
                0, len(nameQuestionsAnswers) - 1)])

    return contexts, answers


def generateWrongNameQuestions():
    """Returns generated wrong name questions."""

    contexts = []
    answers = []

    for goodbye in goodbyes:
        if goodbye[len(goodbye) - 1] not in sentenceEndCharacters:
            while True:
                name = names[randint(0, len(names) - 1)]
                if name != CHATBOT_NAME:
                    break

            contexts.append("{} {}?".format(
                nameQuestions[randint(0, len(nameQuestions) - 1)], name))
            answers.append("{} {}".format(wrongNameQuestionsAnswersWithName[randint(
                0, len(wrongNameQuestionsAnswersWithName) - 1)], CHATBOT_NAME))

    return contexts, answers


def generateTokenUnkownSentences():
    """Returns generated lines with unknown tokens."""

    contexts = []
    answers = []

    for length in range(1, MAX_TOKENS + 1):
        context = ""

        for _ in range(length):
            context += "{} ".format(TOKEN_UNKNOWN)

        contexts.append(context)
        answers.append(notUnderstand[randint(0, len(notUnderstand) - 1)])

    return contexts, answers


def generateChatbotNameSentences():
    """Returns generated lines with chatbot's name."""

    contexts = []
    answers = []

    for length in range(1, MAX_TOKENS + 1):
        context = ""

        for _ in range(length):
            context += "{} ".format(CHATBOT_NAME)

        contexts.append(context)
        answers.append(nameAnswers[randint(0, len(nameAnswers) - 1)])

    return contexts, answers


def generateWrongNames():
    """Returns generated lines with names."""

    contexts = []
    answers = []

    for name in names:
        if name == CHATBOT_NAME:
            continue

        length = randint(1, MAX_TOKENS + 1)
        context = ""

        for _ in range(length):
            context += "{} ".format(name)

        contexts.append(context)

        answers.append(wrongNameAnswers[randint(0, len(wrongNameAnswers) - 1)])

    return contexts, answers


if len(sys.argv) != 3:
    print("Error: Bad format of program arguments.")
    sys.exit()

contextFilePath = sys.argv[1]
utteranceFilePath = sys.argv[2]

try:
    fEnc = open(contextFilePath, "w")
    fDec = open(utteranceFilePath, "w")

    contextsAndAnswers = [generateIntroductions(), generateIntroductionsDemands(), generateGreetings(), generateGoodbyes(), generateWrongGreetings(
    ), generateWrongGoodbyes(), generateNameQuestions(), generateWrongNameQuestions(), generateTokenUnkownSentences(), generateChatbotNameSentences(), generateWrongNames()]

    generatedTotal = 0

    for contexts, answers in contextsAndAnswers:
        for context in contexts:
            fEnc.write("{}\n".format(context))

            generatedTotal += 1

        for answer in answers:
            fDec.write("{}\n".format(answer))

    fEnc.close()
    fDec.close()

    print("Number of generated sentences: {}".format(generatedTotal))

except Exception as e:
    print(e)
