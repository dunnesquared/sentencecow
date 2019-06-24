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

Attributes:
    punctuation ....

To Do:
    * improve comments for module
    * write code for __main__ below that demonstrate examples of each function
    * get_words:
        * fix bug that removes apostrophes, hyphens from words
        * have switch so user decides whether to keep remove all punctuation
    * all functions
        * improve commenting

Done:
    * bad form re textwrap, and re -- what are you using from the pack/modules?


Notes:
    * To see PyDoc comments in interpreter:
        >>> from textanalysis import textanalyis as ta # if in project dir
        >>> from textanalysis import * #if in texanalysis package dir

"""



from textwrap import dedent
from re import sub
from string import punctuation  # to get rid of punctuation in get words

import os  # for driver test code below


def get_sentences(text):
    '''Parse text into a list of sentences. Parameter 'text' is string object.

    Pre-condition:
    --------------
    String object passed as argument
    --------------
    Post-condition:
    --------------
    Returns a list of strings, each item ending with an
    English end-of-punctuation mark. Hopefully, each item will be a grammatica-
    lly sound English sentence, but there's no checking for this as such.
    If argument is empty or otherwise contains no sentences,
    an empty list is returned.

    Pre-condtion:
    --------------
    Non-String object passed as argument
    --------------
    Post-condition:
    --------------
    Function throws TypeError exception
    '''

    if not isinstance(text, str):
        raise TypeError("TypeError in textanalysis.get_sentences:" +
                        "non-string object passed as argument.")

    # Clean text up a bit: remove trailing/leading spaces, indents
    # You'll need to do this for each sentence too
    text = text.strip()
    text = dedent(text)

    # Parsing only works for straight quotes
    # Replace curly opening/closing quotes with straight quotes
    text = text.replace('“', '"')
    text = text.replace('”', '"')

    # Escape characters such as \n or \t mess up the parsing below; take 'em
    # out
    text = sub('[\n\t\r]', ' ', text)

    # No need to continue if dealing with an empty stirng
    if len(text) == 0:
        return []

    # Add a space at the end so last sentence won't be ignored by parsing
    # algorithm below
    text = text + " "

    # Initialize variable that will keep track of the end of each sentence
    i = 0

    # Set it up...
    start = 0
    end_of_text = len(text)
    sentence = ""
    sent_list = []

    while start < end_of_text:  # <=??
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

        i = __get_first_punctuation_mark(pos_list)

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
        sentence = sentence.strip()
        sentence = dedent(sentence)

        # Add it to your list
        sent_list.append(sentence)

        # Your next sentence starts one character away from the end of the
        # previous sentence (in many langauges there is a space before the
        # first letter of a sentence)
        start = pos_lastchar + 1

    return sent_list


def get_words(sentence):
    '''Retrieve words in a sentence, excluding all punctuation marks
    (. , ! ? : ;). Parameter is a string object; function returns a
    list.'''

    # One of the minor banes of Python being dynamically typed.
    if not isinstance(sentence, str):
        raise TypeError("TypeError in textanalysis.get_words:" +
                        "non-string object passed as argument.")


    # Remove certain punctuation marks from sentence
    no_punct_sentence = sub('[\.\,\!\?\:\;\“\”]', '', sentence)

    # Default delimiter in split is blank space
    word_list = no_punct_sentence.split()

    return word_list


def find_start_end(substring, text, start_search=0):
    '''Find the start and end positions of a substring within a given text.
    Parameters text and substring are both strings; start-pos is a non-negative
    integer. Function returns a tuple with start and end positions or -1 if
    substring not found.
    '''

    # Get rid of all leading and tailing whitespaces
    try:
        substring = substring.strip()
        text = text.strip()
    except AttributeError:
        raise

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


def __get_first_punctuation_mark(pos_list):
    '''Private helper function that returns the lowest index in list of punct-
    ation marks. Returns lowest number (any if all the same value).
    If there is no punctuation mark, return -1'''

    # Negative values will always be the smaller index; get rid of them!!
    while -1 in pos_list:
        pos_list.remove(-1)

    # Return position of the punctuation mark at the end of the current
    # sentence assuming there's a mark in the firs place!
    if len(pos_list) == 0:
        return -1
    else:
        return min(pos_list)


def __is_honorific(text, start, index):
    '''Checks whether detected period belongs to an honorific (e.g. Mr.)
    instead of the end of an sentence. Paramter text is string that's being
    scanned betewen indices start and index, inclusive. Returns True if
    honorific; False otherwise.'''

    # Common honorifics found in English language
    honorifics = [
                    'Mr.',
                    'Mrs.',
                    'Ms.',
                    'Mz.',
                    'Mx.',
                    'Dr.',
                    'M.',
                    'Mme.',
                    'Fr.',
                    'Pr.',
                    'Br.',
                    'Sr.'
                ]

    # Focus on the part of text that may contain an honorific
    part = text[start:index+1]

    # See whether any of the honorifics are in that part.
    for x in honorifics:
        if x in part:
            return True  # Honorific found!!

    # Period is not part of the honorific. Period is at end of sentence
    return False


def __ignore_quote(pos, text):
    '''The end of quotation may not be the end of the sentence. This Function
    does a 'stupid' test to find out: if the next significant character is
    lower case, then you don't have a full-sentence. As such, ignore the end
    of the quote (i.e. set its position to -1)'''

    if pos == -1:
        return pos

    # Don't want to look at something outside the bounds of text
    if (pos + 3) <  len(text):
        # The 'stupid' criterion...
        if text[pos + 3].islower():
            return -1

    # Quote 'may' be end of sentence
    return pos


# helper function
def abspath():
    '''Return absolute path of the directory where script is being run'''

    # Get the current directory in Terminal when you try to launch the script
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

    print("\nget_sentences:", end=" ")
    print("scans input string for sentences; returns list of sentences.")
    print("\n>>> text = 'There once was a man from Nantucket. He liked " +
          "living in a bucket! What about you?" )

    print(">>> sent_list = get_sentences(text)")
    print(">>> sent_list")
    print(">>> ['There once was a man from Nantucket.', 'He liked living " +
    "in a bucket!', 'What about you?']")

    print("\nget_words:", end=" ")
    print("scans input string for words; returns list of words.")



    print("\nTesting get_sentences")

    # text = '''
    # My name is Mr. Giovanni. I have a dog called Gruff. He smells like
    # baby-powder.
    # I also have a cat called Dr. Blinky?! She's special! Would you like
    # to play with her? Let me know!!!! "He ate a donut."'''

    text = "\"He ate a donut?\" she asked."
    print(text)

    sent_list = get_sentences(text)
    print(f"Sentence list length {len(sent_list)}")
    if len(sent_list) > 0:
        for x in sent_list:
            print(x)

    for sentence in sent_list:
        print(f"Length = {len(get_words(sentence))};" +
              f"Words: {get_words(sentence)}")

    print("DOING FILE TEST....")
    print("++++++++++++++++++++")

    # Read input file
    location = abspath()
    fin = open(os.path.join(location, "input.txt"))
    file_data = fin.read()
    # print(file_data)

    sent_list = get_sentences(file_data)

    print(f"Sentence list length {len(sent_list)}")
    if len(sent_list) > 0:
        for x in sent_list:
            print(x)

    print("\n++++++++++++++++++++++++++++++++++")
    print("Sentences more than seven words!!")
    print("++++++++++++++++++++++++++++++++++\n")

    for sentence in sent_list:
        word_list = get_words(sentence)
        if len(word_list) > 7:
            print(f"# words = {len(word_list)} => {sentence}")

    positions = find_start_end(sent_list[0], file_data, 0)
    print(f"Start and end pos for 1st sentence: {positions}")

    test_sentence = file_data[positions[0]:positions[1] + 1]
    print(test_sentence)

    positions = find_start_end(sent_list[1], file_data, positions[0])
    print(f"Start and end pos for 2nd sentence: {positions}")

    # Compare sentences
    test_sentence = file_data[positions[0]:positions[1]+1]
    print(test_sentence)

    if test_sentence == sent_list[1]:
        print("Sentences match!")
    else:
        print("Sentences don't match")
