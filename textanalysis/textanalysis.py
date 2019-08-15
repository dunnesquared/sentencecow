# -*- coding: utf-8 -*-
"""A module for extracting sentences from text and more :-p!

This module provides the following functions

1. get_sentences - extract sentences from a text, *as best as possible*
2. get_words - extract words from a text, minus punctuation marks
3. find_start_last - find the start and end indices of a substring in a text

Functions designed and tested for English texts only, using mostly
American conventions. The solutions to these problems do not rely on any
NLP/machine-learning algorithms. As such, they're a bit wonky.
E.g. Sentences with dialogue attribution show the most errors; unaccounted for
abbreviations will show up as false end-of-sentences. But it works for a lot of
other cases too :-).

This is a 'homemade' module made for learning/enjoyment purposes: do not use
in production code.

To Do:
    * Fix offset handling issue
    * READ REGEX tutorial
    * Need to be able to handle \n\t\r at end of sentences; removing them
     in _clean_text screwing presentation in upper layers
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
import sys # getsizeof
import re   # sub
import textwrap  # dedent
import string # punctuation


# Arbitrary text size set to avoid program from gobbling up too much memory
# Set to what you will...
MAX_TEXTSIZE = 100 * 1024 * 1024 # 100 MB

# Check global just in case the bizarre happens...
if MAX_TEXTSIZE < 0:
    raise ValueError("MAX_TEXTSIZE set to value less than zero.")

# Unicode general punctuation encodes several punctuation marks that can
# appear at the end of a sentence. Module should handle '⁇' no differently
# than '??'

# Other possible end-of-sentence punctuation marks
DOT_1LEADER = '․'
DOT_2LEADER = '‥'
ELLIPSIS = '…'
DOUBLE_EXCLAM = '‼'
DOUBLE_Q = '⁇'
QEXCLAM = '⁈'
EXCLAMQ = '⁉'

# Double quotation marks
H_DQUOTE = '‟' # high double quote
LBIG_DQUOTE = '❝'
RBIG_DQUOTE = '❞'
FW_DQUOTE = '＂' # full-width double-quote
LPRIME_DQUOTE = '〝'
RPRIME_DQUOTE = '〞'

# Single quotation marks
# Module uses the American convention that single quotes should only be
# used within double quotes. Moreover, there is currently no functionality
# to parse a sentence within a sentence. E.g. The quote
# "Don said, 'Go to work!' to Sheila." will be parsed as a single sentence.
# The general punctuation marks are left here, however, for possible future
# versions that could handle this as two separate sentences.
H_SQUOTE = '‛' # High single quote
L_SQUOTE = '‘'
R_SQUOTE = '’' # same as apostrophe
LH_SQUOTE = '❛'
RH_SQUOTE = '❜'

# Group them for concise regular expressions below
LEADERS = DOT_1LEADER + DOT_2LEADER + ELLIPSIS
QEX = DOUBLE_EXCLAM + DOUBLE_Q + QEXCLAM + EXCLAMQ
DQUOTES = (H_DQUOTE + LBIG_DQUOTE + RBIG_DQUOTE + FW_DQUOTE + LPRIME_DQUOTE
           + RPRIME_DQUOTE)

# End-of-sentence patterns to help determine the end of a sentence
REGEX_PERIOD = '[\.' + LEADERS + ']\s'
REGEX_QEXMARK = '[\?!' + QEX  +  ']\s'
REGEX_QUOTE = '[\.\?!—' + LEADERS + QEX  + ']"\s'

# These will be replaced by a simpler, straight single/double quotes: ' / "
REGEX_DQUOTE = r'[\“\”' + DQUOTES  +  ']'

# To be removed when counting words
REGEX_ALLSYMOBLS = r'[' + string.punctuation + LEADERS + QEX + DQUOTES + ']'

#==============================ABBREVIATIONS====================================

def _load_abbreviations():
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
    absdir = _get_dir()

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


def _get_dir():
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


# Common abbreviations found in English language
abbreviations = _load_abbreviations()
#==============================================================================

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

    print("***********DEBUGGING GET_SENTENCES***************")
    print("=================================================")
    print("")

    # Check to see whether text is less than defined memory maximum
    _too_big(text)

    # Prepare text for parsing
    text = _clean_text(text)

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

        i = _get_first_punctuation_mark(text, start)

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

        print(f"sentence, before dedent/strip = {repr(sentence)} ")

        # Clean up each sentence so we're not giving any extra spaces on either
        # side

        # BUG!!

        # sentence = textwrap.dedent(sentence).strip()
        #sentence = sentence.strip()

        print(f"sentence, after dedent/strip = {repr(sentence)} ")


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

    # Remove all symbols and punctuation from sentence
    # Do not something like "? ^ & * -" to count as five different words:
    # should return no words
    sentence = re.sub(REGEX_ALLSYMOBLS, '', sentence)
    # Only symbol not removed from above. Don't know why...
    sentence = sentence.replace('\\', '')

    # Remove en dash – and em dash —
    # An en dash is used to denote a period, e.g. 1914–1918
    # An em dash is used to insert a parenthetical phrase in the middle of or
    # an interruption at the end of a sentence
    # Removing them will prevent two distinct words being counted as one
    if '–' in sentence or '—' in sentence:
        sentence = sentence.replace("–", " ") # en dash
        sentence = sentence.replace("—", " ") # em dash

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

    print("***********DEBUGGING FIND_START_END***************")
    print("==================================================")
    print("")

    '''NEW CODE'''
    # Don't bother to find empty substrings in possibly empty texts
    print(f"\nDEBUG: PRE-STRIP, substring = {repr(substring)}")
    sublen  = len(substring.strip())
    textlen = len(text.strip())

    if sublen == 0 or textlen == 0:
        raise ValueError("ValueError in textanalysis.find_start_end:" +
                         "empty string(s) passed to parameters 'substring' " +
                         "or 'text'.")

    # Substrings came from cleaned text. You won't get matches unless you
    # make sure your text is cleaned too.

    #DEBUG
    print("\nBEFORE CLEANING/RE\n=====================")
    print(f"DEBUG: find_start_end, text = {repr(text)}")
    print(f"\nDEBUG: find_start_end, substring = {repr(substring)}")

    text = _clean_text(text)

    # Clean the substring too of curly quotes
    substring = re.sub(r'[\“\”]', '"', substring)

    #DEBUG
    print("\nAFTER CLEANING/RE\n=====================")
    print(f"\nDEBUG: find_start_end, text = {repr(text)}")
    print(f"\nDEBUG: find_start_end substring, = {repr(substring)}\n")


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

def _clean_text(text):
    '''Returns text that is ready for sentence-parsing

    Args:
        text (str): unedited text to be parsed

    Returns:
        text (str): edited text ready for parsing
    '''

    # No need to continue cleaning if dealing with an empty string
    if text:
        # Parsing only works for straight quotes
        # OLD CODE # text = re.sub(r'[\“\”]', '"', text)
        text = re.sub(REGEX_DQUOTE, '"', text)

        # Add a space at the end so last sentence won't be forgotten
        text = text + " "

    return text


def _get_first_punctuation_mark(text, start):
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
    # OLD CODE # match = re.search('[\.]\s', text[start:])
    match = re.search(REGEX_PERIOD, text[start:])
    pos_period = start + match.start() if match else -1

    # Exclamation or question mark
    pos_exqmark = 0
    # OLD CODE # match = re.search('[\?!]\s', text[start:])
    match = re.search(REGEX_QEXMARK, text[start:])
    pos_exqmark = start + match.start() if match else -1

    # Period, question, exclamation, em-dash followed by a quotation mark
    pos_quote = 0
    # OLD CODE # match = re.search('[\.\?!—]"\s', text[start:])
    match = re.search(REGEX_QUOTE, text[start:])
    pos_quote = start + match.start() if match else -1

    # Abbreviations (e.g. Mr.) give false poisitives. Ignore 'em!!
    new_start = start
    while True:
        if _is_abbreviation(text, new_start, pos_period):
            new_start = pos_period + 1
            pos_period = text.find('. ', new_start, end_of_text+1)
        else:
            break

    # Check to see whether first non-space character after end of a
    # quotation or not is lowercase. If it is, don't treat the end of the
    # quotation as the end of the sentence
    pos_quote = _ignore_quote(pos_quote, text)

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


def _is_abbreviation(text, start, index):
    '''Returns True if abbreviation found; False otherwise.

    Args:
        text (str): String being scanned for abbreviation
        start (int): Index where to start search in text
        index (int): Index where to end search in text

    Returns:
        True (bool):  abbreviation found.
        False (bool): No abbreviation found.
    '''
    
    global abbreviations

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


def _ignore_quote(pos, text):
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


def _too_big(text):
    '''Determine whether text string is larger than programmed-placed size
       limit.

    Args:
        text (str): input text to be parsed
        MAX_TEXTSIZE (int, global): max number of bytes allowed

    Raises:
        MemoryError: 'text' memory size > MAX_TEXTSIZE

    Returns:
        False (bool): 'text' is <= MAX_TEXTSIZE
    '''

    if sys.getsizeof(text) > MAX_TEXTSIZE:
        # Give reading in kilobytes rather than bytes
        max_mb = MAX_TEXTSIZE / 1000
        text_mb = sys.getsizeof(text) / 2**10

        err = textwrap.dedent('''
             Python string object 'text' greater than MAX_TEXTSIZE:
             MAX_TEXTSIZE:\t\t\t{:10.4f} kB
             'text'object size:\t\t{:10.4f} kB'''.format(max_mb, text_mb))

        raise MemoryError(err)

    # Everything good
    return False


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
