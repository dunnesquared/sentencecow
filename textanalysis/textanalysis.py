# -*- coding: utf-8 -*-
"""A module for extracting sentences from text and more :-p!

This module provides the following functions

1. get_sentences - extract sentences from a text, *as best as possible*
2. get_words - extract words from a text, minus punctuation marks
3. find_start_last - find the start and end indices of a substring in a text

Functions designed and tested for English texts only. The solutions to these
problems do not rely on any NLP/machine-learning algorithms. As such,
they're a bit wonky. E.g. Sentences with dialogue attribution show the most
errors; unaccounted for abbreviations will show up as false end-of-sentences.
But it works for a lot of other cases too :-).

This is a 'homemade' module made for learning/enjoyment purposes: do not use
in production code.


To Do:
    * Fix offset handling issue
    * READ REGEX tutorial
    * Need to be able to handle \n\t\r at end of sentences; removing them
     in __clean_text screwing presentation in upper layers
    * Handle curly quotes via regex instead cleaning the text of them
    * Be able handle sentences ending with quote then new line:  ."\n
    * check documentation in interpreter
    * use pyreverse to generate uml doc
    * determine big-Oh performance for each function

Last Done:
    * Fix bug with where a substring of an abbreviation gets flagged as the
      full abbreviation (e.g. U.S. in U.S.S.R)


"""

import os   # getcwd, path.join, path.dirname, path.realpath
import re   # sub
import textwrap  # dedent


class NotInTextError(Exception):
    '''Exception for instances when sentence is not in a text

    Attributes:
        message (str): Message showing string that was not found in text.
    '''

    def __init__(self, message):
        super().__init__(message)
        self.message = message


def get_sentences(text):
    '''Return a list of sentences from a text written in English.

    Note that this algorithms does sentence extraction as best as possible.
    Certain sentences may not be parsed correctly. For example,

                "He ate a donut?" Alex asked.

    does not parse to one sentence, but to two: "He ate a donut?"
    and "Alex said."

    Args:
        text (str): Text from which sentences are to be extracted.

    Returns:
        sent_list (list): A sequence of sentences extracted from argument.
    '''

    # Prepare text for parsing
    text = __clean_text(text)

    # Find index of first non-white space character
    # start (int): index where parsing begins; moves as each sentence extracted
    start = offset(text)

    # Set it up...
    # i (int): index of the end of a sentence
    # start (int): index where parsing begins; moves as each sentence extracted
    # sentence (str): extracted sentence from text
    # sent_list (list): list of extracted sentences
    #i, start, sentence, sent_list = 0, 0, "", []
    i, sentence, sent_list = 0, "", []

    while start < len(text):

        i = __get_first_punctuation_mark(text, start)

        # No end-of-sentence punctuation marks in sentence
        if i == -1:
            return sent_list

        # find() returns the index of the first character in the string your
        # searching for.
        # As such increment the index if sentence ends with a quotation mark
        pos_lastchar = i
        if text[i+1] == "\"":
            pos_lastchar = i + 1

        # Extract sentence and clean it up a bit
        sentence = text[start:(pos_lastchar + 1)]

        # Clean up each sentence so we're not giving any extra spaces on either
        # side
        sentence = textwrap.dedent(sentence).strip()

        # Add it to your list
        sent_list.append(sentence)

        # Your next sentence starts one character away from the end of the
        # previous sentence (in many langauges there is a space before the
        # first letter of a sentence)
        start = pos_lastchar + 1

    return sent_list


def get_words(sentence):
    '''Return words in a sentence, excluding certain punctuation marks.

    The punctuation marks excluded are . , ! ? : ; “ ” " . Hyphens and
    apostrophes are kept, but em dashes are not.

    Args:
        sentence (str): Sentence from which words are to be extracted

    Returns:
        words (list): Sequence of words from the given sentence
     '''

    # Remove certain punctuation marks from sentence
    sentence = re.sub(r'[\.\,\!\?\:\;\“\”\"]', '', sentence)

    # Since em dash can separate two clauses, you'll want to avoid
    # the case where you get a word that is a suture of the last word in the
    # first clause and the first word in the next one.
    if '—' in sentence:
        sentence = sentence.replace("—", " ")

    # Default delimiter in split is blank space
    words = sentence.split()

    return words


def find_start_end(substring, text, start_search=0):
    '''Return start and end indices of a substring within a given text.

    Args:
        substring (str): Substring to search within another string
        text (str): The string that will be searched for the substring indices
        start_search (int): The index where the search in text should begin

    Raises:
        ValueError: Arguments substring and text are empty strings

    Return:
        -1 (int): If substring not in text being searched
        (start_pos, end_pos) tuple(int, int): If substring is found,
        the start and end indices of the substring in the searched string
    '''

    '''NEW CODE'''
    # Don't bother to find empty substrings in possibly empty texts
    sublen  = len(substring.strip())
    textlen = len(text.strip())

    if sublen == 0 or textlen == 0:
        raise ValueError("ValueError in textanalysis.find_start_end:" +
                         "empty string(s) passed to parameters 'substring' " +
                         "or 'text'.")

    # Substrings came from cleaned text. You won't get matches unless you
    # make sure your text is cleaned too.
    text = __clean_text(text)

    # Clean the substring too of curly quotes
    substring = re.sub(r'[\“\”]', '"', substring)

    # Make sure our start position is something sensible
    if start_search < 0:
        raise ValueError("ValueError in textanalysis.find_start_end:" +
                         "argument for parameter 'start_search' less than" +
                         "zero.")

    # No point in continuing if substring not in text
    if substring not in text:
        raise NotInTextError(f"Substring '{substring}' not found in text.'")

    # Initialize start and end positions of substring in text
    start_pos = 0
    end_pos = 0

    # Find out start and end positions of substring in text
    start_pos = text.find(substring, start_search, len(text) + 1)
    end_pos = start_pos + len(substring)

    return (start_pos, end_pos)

    # DEPRECATED CODE
    # Too complicated to escape all metacharacters in regex module
    # Get start and end positions of substring in text; None if not there

    # Required so pattern-matching doesn't ignore the question mark at
    # # end of string
    # substring = re.sub('[\?]', r'\?', substring)
    #
    # m = re.search(substring, text)
    #
    # if m:
    #     print(f"DEBUG: regex object search result = {m.group()}")
    #     start, end = m.span()
    # else:
    #     raise NotInTextError(f"Substring '{substring}' not found in text.'")
    #
    # return (start, end)

def offset(text):
    '''Return index of first non white-space character from left.
    Args:
        text (str): string to be analyzed for white-spaces

    Returns:
        index (int): index of first non-white-space character; -1 if none found
    '''
    index = 0
    match = re.search('[^\s]', text, re.IGNORECASE)
    index = match.start() if match else -1

    return index

# +++++++++++++++++++++++++++++PRIVATE++++++++++++++++++++++++++++++++++++++
# Private module helper functions

def __clean_text(text):
    '''Returns text that is ready for sentence-parsing

    Args:
        text (str): unedited text to be parsed

    Returns:
        text (str): edited text ready for parsing
    '''

    # No need to continue cleaning if dealing with an empty string
    if text:
        # Parsing only works for straight quotes
        text = re.sub(r'[\“\”]', '"', text)

        # Add a space at the end so last sentence won't be forgotten
        text = text + " "

    return text


def __get_first_punctuation_mark(text, start):
    '''Return index of the punctuation mark that marks the end of a sentence

    Args:
        text (str): text being parsed
        start (int): index where to start search in text


    Returns:
        index (int): index of first end-of sentence punctuation mark; -1
                     if no punctuation mark found
    '''
    end_of_text = len(text)

    # Search text for first occurence of the following punctuation marks:
    # Period
    pos_period = 0
    match = re.search('[\.]\s', text[start:])
    pos_period = start + match.start() if match else -1
    # Exclamation or question mark
    pos_exqmark = 0
    match = re.search('[\?!]\s', text[start:])
    pos_exqmark = start + match.start() if match else -1
    # Period, question, exclamation, em-dash followed by a quotation mark
    pos_quote = 0
    match = re.search('[\.\?!—]"\s', text[start:])
    pos_quote = start + match.start() if match else -1

    # Abbreviations (e.g. Mr.) give false poisitives. Ignore 'em!!
    new_start = start
    while True:
        if __is_abbreviation(text, new_start, pos_period):
            new_start = pos_period + 1
            pos_period = text.find('. ', new_start, end_of_text+1)
        else:
            break

    # Check to see whether first non-space character after end of a
    # quotation or not is lowercase. If it is, don't treat the end of the
    # quotation as the end of the sentence
    pos_quote = __ignore_quote(pos_quote, text)

    # Get position of the punctuation mark at the end of the current
    # sentence
    pos_list = [pos_period, pos_exqmark, pos_quote]

    # Negative values will always be the smaller index; get rid of them!!
    while -1 in pos_list:
        pos_list.remove(-1)

    # Return position of the punctuation mark at the end of the current
    # sentence assuming there's a mark in the firs place!
    index = min(pos_list) if pos_list else -1

    return index


def __is_abbreviation(text, start, index):
    '''Returns True if abbreviation found; False otherwise.

    Args:
        text (str): String being scanned for abbreviation
        start (int): Index where to start search in text
        index (int): Index where to end search in text

    Returns:
        True (bool):  abbreviation found.
        False (bool): No abbreviation found.
    '''

    # Common abbreviations found in English language
    abbreviations = __load_abbreviations()

    # Focus on the part of text that may contain an abbreviation
    part = text[start:index+1]

    # See whether any of the abbreviations are in that part.
    # Need words of sentence since we want to check for a whole abbreviation
    # not a substring of it
    # E.g. "Back in the U.S.S.R." the abbreviation U.S. should not return
    # True!
    word_list = part.split()
    for abbreviation in abbreviations:
        if abbreviation in word_list:
            return True  # Abbreviation found!!

    # Period is not part of the abbreviation. Period is at end of sentence
    return False


def __ignore_quote(pos, text):
    '''Check whether quote is truly end of a sentence.

    The end of quotation may not be the end of the sentence. This function
    does a 'stupid' test to find out: if the next significant character is
    lower case, then you don't have a full-sentence. As such, ignore the end
    of the quote (i.e. set its position to -1)

    Args:
        pos (int): Relevant index near where quote detected
        text (str): Text being parsed

    Returns:
        -1 (int): if quote is not the end of the sentence
        pos (int): if quote is the end of the sentence
    '''

    if pos == -1:
        return pos

    # Don't want to look at something outside the bounds of text
    if (pos + 3) < len(text):
        # The 'stupid' criterion...
        if text[pos + 3].islower():
            return -1

    # Quote 'may' be end of sentence
    return pos


def __load_abbreviations():
    '''Return list of abbreviations as per contents of abbreviations.txt

    Args:
        None

    Raises:
        FileNotFoundError: abbreviations.txt not found

    Returns:
        abbreviations (list): list of common English abbreviations
    '''

    # File to be read
    input_filename = "abbreviations.txt"

    # Get directory where input exists, i.e. same dir as this module
    absdir = __get_dir()

    # Intelligently concatenate the directory and the input file name together
    full_filename = os.path.join(absdir, input_filename)

    # Read input file
    # 'with as' ensures file is closed even if exception raised
    with open(full_filename, "r") as fin:
        data = fin.read()

    # Parse data and put into list
    abbreviations = data.split('\n')

    # Get rid of extra '' entry caused by text editor inexplicably adding
    # a line after the last abbreviation upon saving the file
    abbreviations.pop()

    return abbreviations


def __get_dir():
    '''Return absolute path of the directory where script exists

    Args:
        None

    Returns:
        dir (str): the unique ('canonical') absolute path of the directory
                   (i.e. no symbolic links in path)
    '''

    # Get the current working directory in Terminal
    # when you try to launch the script
    cwd = os.getcwd()

    # Get the name of the directoy where this script exists
    script_dir = os.path.dirname(__file__)

    # Intelligently cocantenate the two
    joinedpath = os.path.join(cwd, script_dir)

    # Get rid of any possible symbolic links found along and return the
    # absolute path
    return os.path.realpath(joinedpath)


# ++++++++++++++++++++++++++++++++=MAIN++++++++++++++++++++++++++++++++++++++
if __name__ == "__main__":

    print("\ntextanalysis - module for extracting sentences from text " +
          "and more!")

    print("\nExamples:")
    print("=========")

    print("\nget_sentences:")
    print("--------------")
    print("Scans input string for sentences; returns list of sentences.")
    print("\n>>> text = 'There once was a man from Nantucket. He liked " +
          "living in a bucket! What about you?'")
    print(">>> sent_list = get_sentences(text)")
    print(">>> sent_list")
    print("['There once was a man from Nantucket.', 'He liked living " +
          "in a bucket!', 'What about you?']")
    print("")

    print("\nget_words:")
    print("----------")
    print("Scans input string for words; returns list of words " +
          "without certain punctuation marks")
    print("\n>>> text = \"Dog-lovers, like me, hate cats—false!\"")
    print(">>> words = get_words(text)")
    print(">>> words")
    print("[Dog-lovers, like, me, hate, cats, false]")
    print("")

    print("\nfind_start_end:")
    print("---------------")
    print("Returns start and end indices of a substring in a string.")

    print("\n>>> text = \"Your pizza is delicious.\"")
    print(">>> find_start_end(\"pizza\", text, start_search=0)")
    print("(5, 9)")
    print("")
