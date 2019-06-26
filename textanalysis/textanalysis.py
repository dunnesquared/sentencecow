# -*- coding: utf-8 -*-
"""textanalysis -  a module for extracting sentences from text and more :-p!

This module provides the following functions

1. get_sentences - extract sentences from a text, *as best as possible*
2. get_words - extract words from a text, minus punctuation marks
3. find_start_last - find the start and end indices of a substring in a text

Functions designed and tested for English texts only. The solutions to these
problems do not rely on any NLP/machine-learning algorithms. As such,
they're a bit 'hacky.' Sentences with dialogue attribution show the most errors.

This is a 'homemade' module made for learning/enjoyment purposes; do not use
as a production-ready code.


To Do:
    * improve comments for module
    * consider using helper functions in get_sentences to reduce complexity
      of function
    * Add support for abbreviations
        * put abbreviations in text file: decouple data from code

Done:
    * bad form re textwrap, and re -- what are you using from the pack/modules?
    * get_words:
        * fix bug that removes apostrophes, hyphens from words
    * write code for __main__ below that demonstrate examples of each function
        * all functions
            * improve commenting

Notes:
    * To see PyDoc comments in interpreter:
        >>> from textanalysis import textanalyis as ta # if in project dir
        >>> from textanalysis import * #if in texanalysis package dir

"""

from textwrap import dedent
from re import sub


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

    # Set it up...
    # i (int): index of the end of a sentence
    # start (int): index where parsing begins; moves as each sentence extracted
    # sentence (str): extracted sentence from text
    # sent_list (list): list of extracted sentences
    i, start, sentence, sent_list = 0, 0, "", []

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
        sentence = dedent(sentence).strip()

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
    sentence = sub('[\.\,\!\?\:\;\“\”\"]', '', sentence)

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
        AttributeError: Bad argument type for substring or text
        ValueError: Arguments substring and text are empty strings

    Return:
        -1 (int): If substring not in text being searched
        (start_pos, end_pos) tuple(int, int): If substring is found,
        the start and end indices of the substring in the searched string
    '''

    # Get rid of all leading and tailing whitespaces
    substring = substring.strip()
    text = text.strip()


    # Don't bother to find empty substrings in possibly empty texts
    if len(substring) == 0 or len(text) == 0:
        raise ValueError("ValueError in textanalysis.find_start_end:" +
                         "empty string(s) passed to parameters 'substring' or " +
                         "'text'.")

    # Make sure our start position is something sensible
    if start_search < 0:
        raise ValueError("ValueError in textanalysis.find_start_end:" +
                         "argument for parameter 'start_search' less than" +
                         "zero.")

    # No point in continuing is substring not in text
    if substring not in text:
        return -1

    # Initialize start and end positions of substring in text
    start_pos = 0
    end_pos = 0

    # Find out start and end positions of substring in text
    start_pos = text.find(substring, start_search, len(text) + 1)
    end_pos = start_pos + len(substring) - 1

    return (start_pos, end_pos)

# +++++++++++++++++++++++++++++PRIVATE++++++++++++++++++++++++++++++++++++++
# Private module helper functions

def __clean_text(text):
    '''Returns text that is ready for sentence-parsing

    Args:
        text (str): unedited text to be parsed

    Returns:
        text (str): edited text ready for parsing
    '''

    # Remove trailing/leading spaces, indents on subsequent lines
    text = dedent(text).strip()

    # No need to continue cleaning if dealing with an empty string
    if text:
        # Parsing only works for straight quotes
        text = sub('[\“\”]', '"', text)

        # Escape characters such as \n or \t mess up the parsing
        text = sub('[\n\t\r]', ' ', text)

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

    # Search text for first occurence of the following punctuation marks
    pos_period = text.find('. ', start, end_of_text+1)
    pos_qmark = text.find('? ', start, end_of_text+1)
    pos_exclam = text.find('! ', start, end_of_text+1)
    # Look for these too..
    pos_qper = text.find('." ', start, end_of_text+1)
    pos_qque = text.find('?" ', start, end_of_text+1)
    pos_qexc = text.find('!" ', start, end_of_text+1)
    pos_qdsh = text.find('—" ', start, end_of_text+1)

    # Honorifics (e.g. Mr.) give false poisitives. Ignore 'em!!
    new_start = start
    while True:
        if __is_honorific(text, new_start, pos_period):
            new_start = pos_period + 1
            pos_period = text.find('. ', new_start, end_of_text+1)
        else:
            break

    # Check to see whether first non-space character after end of a
    # quotation or not is lowercase. If it is, don't treat the end of the
    # quotation as the end of the sentence
    pos_qque = __ignore_quote(pos_qque, text)
    pos_qexc = __ignore_quote(pos_qexc, text)
    pos_qdsh = __ignore_quote(pos_qdsh, text)

    # Get position of the punctuation mark at the end of the current
    # sentence
    pos_list = [pos_period, pos_qmark, pos_exclam, pos_qper, pos_qque,
                pos_qexc, pos_qdsh]

    # Negative values will always be the smaller index; get rid of them!!
    while -1 in pos_list:
        pos_list.remove(-1)

    # Return position of the punctuation mark at the end of the current
    # sentence assuming there's a mark in the firs place!
    if pos_list:
        index = min(pos_list)
    else:
        index = -1

    return index


def __is_honorific(text, start, index):
    '''Returns True if honorific found; False otherwise.

    Args:
        text (str): String being scanned for honorific
        start (int): Index where to start search in text
        index (int): Index where to end search in text

    Returns:
        True (bool): Honorific found.
        False (bool): No honorific found.
    '''

    # Common honorifics found in English language
    honorifics = ['Mr.', 'Mrs.', 'Ms.', 'Mz.', 'Mx.', 'Dr.', 'M.', 'Mme.',
                  'Fr.', 'Pr.', 'Br.', 'Sr.']

    # Focus on the part of text that may contain an honorific
    part = text[start:index+1]

    # See whether any of the honorifics are in that part.
    for honorific in honorifics:
        if honorific in part:
            return True  # Honorific found!!

    # Period is not part of the honorific. Period is at end of sentence
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
