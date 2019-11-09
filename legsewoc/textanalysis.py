# -*- coding: utf-8 -*-
"""Support to extract sentences from a text.

This module provides functions to extract sentences from a text. Any string of
characters that ends with a terminating punctuation mark such as a period,
exclamation or question mark followed by a whitespace character is
considered to be a sentence, regardless of its grammatical correctness.
Analyzed texts are assumed to be in English; all functions were written and
tested with that assumption. Where decisions had to be made to respect American
or British English conventions, the former was chosen.

The solutions to sentence extraction presented in this module rely heavily
on regular expressions but not on NLP or machine-learning algorithms. Perhaps
because of this, the function 'get_sentences' does not always return sentences
a reader would consider 'complete' when looking upon them. There are
several situations where this may occur:

1) In sentences containing dialogue

"This is ridiculous! What do you mean there's no pizza left?" Marcus asked.

Normally, readers would consider this to be a single, complete sentence while
acknowledging the sentences nested inside. The function 'get_sentences'
doesn't make any such distinction and returns the list

[   '"This is ridiculous!',
    'What do you mean there's no pizza left?',
    '" Marcus asked.'
]

2) In sentences that end with a terminating punctuation mark but with no
   whitespace character afterward.

As mentioned above, a whitespace after a terminating punctuation mark is
required for the module to detect a sentence. A citation symbol or
number immediately after a terminating will prevent this.

For example, in the invented paragraph below, 'get_sentences' should return
two sentences; it will only return one: the whole paragraph.

e.g. The moon is made of green cheese.[6] Scientists discovered this fact in
10 BCE.

Return value of 'get_sentences':

['The moon is made of green cheese.[6] Scientists discovered this fact in
10 BCE.']

3) In sentences that contain 'unfamiliar' abbreviations ending with a period.

As might be suspected, abbreviations such as 'Mr.' or 'U.S.S.R.' might cause
end of sentences to be detected when they shouldn't be. To avoid this,
the module uses a list of abbreviations in the file "abbreviations.txt": any
abbreviation in this file will not be treated as an end of sentence and
ignored as such.

For example, the honorific 'Dr.' is included in 'abbreviations.txt'.
Consequently, the sentence

Dr. Dunne does dissections diligently.

will be parsed as a single sentence,

['Dr. Dunne does dissections diligently.']

whereas the abbreviation 'Bx.', which is not in the abbreviations file, will
result in a sentence being detected prematurely; two 'sentences' are returned.

Bx. Barry borrows bananas.

will be parsed as

['Bx.', 'Barry borrows bananas.']

4) In sentences that end with a 'familiar' abbreviation.

Unfortunately, the fix for the abbreviation above creates a new problem with
sentences that end in an abbreviation. For example, if the abbreviation 'Fl.'
is in 'abbreviations.txt', then the following text

Welcome the Fl. It's the best.

won't be broken into two sentences, but will be parsed as one: the
period in 'Fl.' is not seen as the terminating punctuation mark, but is rather
skipped because the parsing algorithm tells it too!

The only exception to this is if the abbreviation is at the very of the end of
the text: it should be processed then as expected.

5) Sentences containing grawlixes.

E.g. The text

This #$@&%*! module doesn't do what it's supposed to!

would be parsed by get_sentences as

['This #$@&%*!', 'module doesn't do what it's supposed to!']

Note:
The file 'abbreviations.txt' is the product of a separate web-scraping
script 'abbrevscrape.py'. Should you wish to generate the abbreviations file
yourself, its online repository can be found at
https://github.com/dunnesquared/abbrevscrape.

"""


import os   # getcwd, path.join, path.dirname, path.realpath
import sys # getsizeof
import re   # sub
import textwrap  # dedent
import string # punctuation


#==============================SETTING MAX SIZE================================

# Arbitrary text size set to avoid program from gobbling up too much memory
# Set to what you will...
MAX_TEXTSIZE = 100 * 1024 * 1024 # 100 MB

# Check global constant just in case the bizarre happens...
if MAX_TEXTSIZE < 0:
    raise ValueError("MAX_TEXTSIZE set to value less than zero.")

#==============================REGEX GLOBALS===================================

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
SQUOTES = H_SQUOTE + L_SQUOTE + R_SQUOTE + LH_SQUOTE + RH_SQUOTE

# End-of-sentence patterns to help determine the end of a sentence
REGEX_PERIOD = r'[\.' + LEADERS + r']\s'
REGEX_QEXMARK = r'[\?!' + QEX  +  r']\s'
REGEX_QUOTE = r'[\.\?!—' + LEADERS + QEX  + r']"\s'

# These will be replaced by a simpler, straight single/double quotes: ' / "
REGEX_DQUOTE = r'[\“\”' + DQUOTES  +  ']'

# To be removed when counting words
REGEX_ALLSYMOBLS = (r'[' + string.punctuation + LEADERS + QEX + DQUOTES
                    + SQUOTES +']')

#===================INITIALIZING ABBREVIATIONS SET=============================

# Path of abbreviations.txt file
ABBREVIATION_DATA_FILEPATH = "./data/abbreviations.txt"

def _get_dir():
    """Returns absolute path of the directory where module exists.

    Returns:
        dir (str): the unique ('canonical') absolute path of the directory
                   containing the module (i.e. no symbolic links in path).
    """

    # Get the current working directory in Terminal
    # when you try to launch the module as a script
    cwd = os.getcwd()

    # Get the name of the directoy where the module exists
    module_dir = os.path.dirname(__file__)

    # Intelligently cocantenate the two
    joinedpath = os.path.join(cwd, module_dir)

    # Get rid of any possible symbolic links found along and return the
    # absolute path
    return os.path.realpath(joinedpath)


def _load_abbreviations():
    """Gets list of abbreviations as per contents of 'abbreviations.txt'.

    Raises:
        FileNotFoundError: abbreviations.txt not found.

    Returns:
        abbreviations (list): strings found in 'abbreviations.txt'.
    """

    # Get directory where input exists, i.e. same dir as this module
    absdir = _get_dir()

    # Intelligently concatenate the directory and the input file name together
    full_filename = os.path.join(absdir, ABBREVIATION_DATA_FILEPATH)

    with open(full_filename, "r") as fin:
        data = fin.read()

    # Each abbreviation is written on a newline
    abbreviations = data.split('\n')

    # Get rid of extra '' list-entry caused by text editor adding
    # a line after the last abbreviation upon saving the file
    abbreviations.pop()

    return abbreviations


# Common abbreviations found in English language
# Casting them as a set will allow efficient intersection with other data
ABBREVIATIONS = set(_load_abbreviations())

#==============================CLASSES=========================================

class NotInTextError(Exception):
    """String not found in text.

    Attributes:
        message (str): Message regarding string that was not found in a text.
    """

    def __init__(self, message):
        """Init parent class and this class with developer error message."""
        super().__init__(message)
        self.message = message


#==============================PUBLIC FUNCTIONS================================

def get_sentences(text):
    """Returns a list of sentences from a text.

    Any string of characters that ends with a terminating punctuation mark such
    as a period, exclamation or question mark followed by a whitespace character
    is considered to be a sentence, regardless of its grammatical correctness.

    Read the module docstring above for special cases that discuss the
    limitations of this feature.

    Args:
        text (str): Text from which sentences are to be extracted.

    Returns:
        sent_list (list): A sequence of sentences extracted from argument.
    """

    # Check to see whether text is less than defined, yet arbitrary memory max
    _too_big(text)

    # Prepare text for parsing
    text = _clean_text(text)

    # Find index of first non-white space character
    # start (int): index where parsing begins; moves as each sentence extracted
    start = offset(text)

    # Set it up...
    # i (int): index of the end of a sentence
    # sentence (str): extracted sentence from text
    # sent_list (list): list of extracted sentences
    i, sentence, sent_list = 0, "", []

    # Scan text...
    while start < (len(text)-1):

        i = _get_first_punctuation_mark(text, start)

        # No end-of-sentence punctuation marks in sentence
        if i == -1:
            return sent_list

        # _get_first_punctuation_mark returns the index of a terminating
        # punctuation mark, which in a sentence that ends in a quotation mark
        # is does not point to the sentence's end.
        # As such increment the index if sentence ends with a quotation mark.
        pos_lastchar = i
        if text[i+1] == "\"":
            pos_lastchar = i + 1

        # Extract sentence and clean it up a bit
        sentence = text[start:(pos_lastchar + 1)]

        # Add extracted sentence to list
        sent_list.append(sentence)

        # The next sentence starts one character away from the end of the
        # previous sentence
        start = pos_lastchar + 1

    return sent_list


def get_words(sentence):
    """Returns words in a sentence, excluding certain punctuation marks.

    The punctuation marks excluded are . , ! ? : ; “ ” " . Hyphens and
    apostrophes are kept, but em dashes are not.

    Args:
        sentence (str): Sentence from which words are to be extracted.

    Returns:
        words (list): Sequence of words from the given sentence.
     """

    # Remove all symbols and punctuation from sentence
    # e.g. Do not let something like "? ^ & * -" to count as five different
    # words: function should return no words
    sentence = re.sub(REGEX_ALLSYMOBLS, '', sentence)

    # Only symbol not removed from above. Not sure why not...
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
    """Returns start and end indices of a substring within a given text.

    Args:
        substring (str): Substring to search within another string.
        text (str): The string that will be searched for the substring indices.
        start_search (int): The index where the search in text should begin.

    Raises:
        ValueError: Arguments substring and text are empty strings.

    Returns:
        -1 (int): If substring not in text being searched.
        (start_pos, end_pos): An integer tuple representing the start and end
                              indices of the substring in the searched string.
    """

    # Don't bother to find empty substrings in possibly empty texts
    sublen = len(substring.strip())
    textlen = len(text.strip())

    if sublen == 0 or textlen == 0:
        raise ValueError("ValueError in textanalysis.find_start_end:" +
                         "empty string(s) passed to parameters 'substring' " +
                         "or 'text'.")

    # Substrings came from cleaned text. You won't get matches unless you
    # make sure your text is cleaned too.
    text = _clean_text(text)

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

    # Find or calculate the start and end positions of substring in text
    start_pos = text.find(substring, start_search, len(text) + 1)
    end_pos = start_pos + len(substring)

    return (start_pos, end_pos)


def offset(text):
    """Returns index of first non-whitespace character.

    Args:
        text (str): string to be analyzed for whitespaces.

    Returns:
        index (int): index of first non-whitespace character; -1 if none found.
    """

    index = 0 # Assume first character is not a whitespace

    # \s == whitespace character, ^\s == NOT whitespace character
    match = re.search(r'[^\s]', text, re.IGNORECASE)

    # -1 only really possible if whole text is blank or made of whitespace
    # characters
    index = match.start() if match else -1

    return index


# =============================PRIVATE FUNCTIONS===============================

def _clean_text(text):
    """Returns text that is ready for sentence-parsing.

    Args:
        text (str): unedited text to be parsed.

    Returns:
        text (str): edited text ready for parsing.
    """

    # No need to continue cleaning if dealing with an empty string
    if text:

        # Parsing only works for straight quotes
        text = re.sub(REGEX_DQUOTE, '"', text)

        # Add a space at the end of text to make sure last sentence in text is
        # added to sentence list
        text = text + " "

    return text


def _get_first_punctuation_mark(text, start):
    """Returns index of the first terminating punctuation mark encountered after
       start position.

    To illustrate the principles implemented in this function, examine the
    following text:

            Hello, Mr. Darcy! Would you like a cup of tea?

     There are three terminating punctuation marks in this text: one period,
     one exclamation mark and one question mark. Assuming a parsing algorithm
     begins scanning at index 0, which terminating punctuation mark should it
     pick as the end of the first sentence of the text? The exclamation mark,
     of course.

     This is what this function does.

    Args:
        text (str):  text being parsed.
        start (int): index where to start search in text.

    Returns:
        index (int): index of first terminating punctuation mark found; -1
                     if no punctuation mark found
    """

    end_of_text = len(text)

    # Search text for first occurence of the following punctuation marks:

    # Period
    pos_period = 0
    match = re.search(REGEX_PERIOD, text[start:])
    pos_period = start + match.start() if match else -1

    # Exclamation or question mark
    pos_exqmark = 0
    match = re.search(REGEX_QEXMARK, text[start:])
    pos_exqmark = start + match.start() if match else -1

    # Period, question, exclamation, em-dash followed by a quotation mark
    pos_quote = 0
    match = re.search(REGEX_QUOTE, text[start:])
    pos_quote = start + match.start() if match else -1

    # Handle abbreviations
    # Variable will hold the index num right after the period of an
    # abbreviation that should be 'skipped'
    new_start = start

    while True:

        # See whether there's any meaningful text to parse after a period
        not_blank = bool(text[pos_period+1:].strip())

        # Abbreviations at the very end of the text should not be skipped
        # and be recognized as the end of a sentence. Unfortunately, I could
        # not think of a way to make my program smart enough to skip
        # abbreviations in the middle of a sentence, but not at the end of one!
        if _is_abbreviation(text, new_start, pos_period) and not_blank:
            new_start = pos_period + 1
            pos_period = text.find('. ', new_start, end_of_text+1)
        else:
            break

    # Check to see whether first non-whitespace character after end of a
    # quotation is lowercase. If it is, don't treat the end of the
    # quotation as the end of the sentence

    if pos_quote != -1: # quote found
        pos_quote = _ignore_quote(pos_quote, text)

    # Get position of the punctuation mark at the end of the current
    # sentence

    pos_list = [pos_period, pos_exqmark, pos_quote]

    # Negative values will always be the smaller index; get rid of them!!
    pos_list = list(filter(lambda x: x != -1, pos_list))

    # Return position of the punctuation mark at the end of the current
    # sentence assuming there's a mark in the first place!
    index = min(pos_list) if pos_list else -1

    return index


def _is_abbreviation(text, start, end):
    """Returns True if abbreviation found; False otherwise.

    An abbreviation is only considered found if exists in the file
    "abbreviations.txt" accompanying this module.

    Args:
        text (str): String being scanned for abbreviation.
        start (int): Index where to start search in text.
        end (int): Index where to end search in text.

    Returns:
        True (bool):  abbreviation found.
        False (bool): No abbreviation found.
    """

    # Focus only on the part of text that may contain an abbreviation
    part = text[start:end+1]

    # See whether any of the abbreviations are in that part.

    # Need words of sentence since we want to check for a whole abbreviation
    # not a substring of it
    # E.g. In the text "Back in the U.S.S.R." we don't want the abbreviation
    # 'U.S.' cause this function to return True!
    sent_words = set(part.split())

    # Disjoint means two sets share nothing in common (essentially their
    # intersection is the null set). So, if the two sets are NOT disjoint,
    # then you've found an abbreviation; otherwise you (maybe) haven't.
    disjoint = sent_words.isdisjoint(ABBREVIATIONS)

    return not disjoint


def _ignore_quote(pos, text):
    """Check whether quote is truly end of a sentence.

    The end of a quotation may not be the end of the sentence. This function
    does a 'weak' test to find out: if the next non-whitespace character is
    lower case, then you don't have a full-sentence. As such, the quote
    does not mark the end of a sentence; set its position to -1.

    Args:
        pos (int): Relevant index near where quote detected.
        text (str): Text being parsed.

    Returns:
        -1 (int): if quote is not the end of the sentence.
        pos (int): if quote is the end of the sentence.
    """

    # Don't want to look at something outside the bounds of text
    if (pos + 3) < len(text):
        # The 'weak' criterion...
        if text[pos + 3].islower():
            return -1

    # Quote 'may' be end of sentence
    return pos


def _too_big(text):
    """Determine whether text string is larger than arbitrary size limit

    Args:
        text (str): input text to be parsed.

    Raises:
        MemoryError: 'text' memory size > MAX_TEXTSIZE.

    Returns:
        False (bool): 'text' is <= MAX_TEXTSIZE.
    """

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


# ==================================MAIN=======================================
if __name__ == "__main__":

    # Examples to help developers get a quick idea of what the public api can
    # do

    print("\ntextanalysis - module for extracting sentences from text " +
          "and more!")

    print("\nQuickstart Tutorial Examples:")
    print("====================")

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
          "without certain punctuation marks.")
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

    print("\noffset:")
    print("-------")
    print("Returns index of first non-whitespace character.")

    print("\n>>> text = \"    There are four spaces before this sentence.\"")
    print(">>> offset(text)")
    print("4")
    print("")
