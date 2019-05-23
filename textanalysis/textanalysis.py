
'''
Notes: What about ?! or !!!!! or ...  ? Replace them before parsing??

To Do:

* Unit test get_sentences and get_words using nosetests
* Create a Sentence class; return a Sentence object in get_sentences??

Done:
* Write driver to detect whether sentences are 7 words or less
* Refactor get_sentences to return map of data
* Refactor get_sentences so that delimiters are ". ", etc, so as to handle !!! or ?! or ...
* Refactor get_sentences so to only return a list of sentences
* Refactor get_words so that delimiters are ". ", etc, so as to handle !!! or ?! or ...
* Debug find_start_end
* Write a function that will find the beginning and end of sentence in a text
* Refactor get_sentences and get_word to encapsulate duplicate code in a method
(i.e. finding the first end-of-sentence punctuation point)
'''

import textwrap
import re


def get_sentences(text):
    '''Parse text into a list of sentences. Parameter 'text' is string object.

    Pre-condition:
    --------------
    String object passed as argument
    --------------
    Post-condition:
    --------------
    Returns a list of strings, each item ending with an
    English end-of-punctuation mark. Hopefully, each item will be a grammatically-
    sound English sentence, but there's no checking for this as such.
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
        raise TypeError("TypeError in textanalysis.get_sentences: non-string object passed as argument.")

    #Clean text up a bit: remove trailing/leading spaces, indents
    #You'll need to do this for each sentence too
    text = text.strip()
    text = textwrap.dedent(text)

    #Escape characters such as \n or \t mess up the parsing below; take 'em out
    text = re.sub('[\n\t\r]', ' ', text)

    #No need to continue if dealing with an empty stirng
    if len(text) == 0:
        return []

    #Add a space at the end so last sentence won't be ignored by parsing
    #algorithm below
    text = text + " "

    #Initialize variable that will keep track of the end of each sentence
    i = 0

    #Set it up...
    start = 0
    end_of_text = len(text)
    sentence = ""
    sent_list = []

    while start <= end_of_text:
        #Search text for first occurence of the following punctuation marks
        pos_period = text.find('. ', start, end_of_text+1)
        pos_qmark = text.find('? ', start, end_of_text+1)
        pos_exclam = text.find('! ', start, end_of_text+1)

        #Get position of the punctuation mark at the end of the current sentence
        i = __get_first_punctuation_mark(pos_period, pos_qmark, pos_exclam)

        #No end-of-sentence punctuation marks in sentence
        if i == -1:
            return sent_list

        #Extract sentence and clean it up a bit
        sentence = text[start:(i+1)]

        #Clean up each sentence so we're not giving any extra spaces on either
        #side
        sentence = sentence.strip()
        sentence = textwrap.dedent(sentence)

        #Add it to your list
        sent_list.append(sentence)

        #Your next sentence starts one character away from the end of the
        #previous sentence (in many langauges there is a space before the
        #first letter of a sentence)
        start = i + 1

    return sent_list



def get_words(sentence):
    '''Retrieve words in a sentence, excluding ending punctuation mark
    (e.g. '.', '?', etc.). Parameter is a string object; function returns a
    list.'''

    #Default delimiter is blank space
    word_list = sentence.split()

    #Assume last word has the period, question mark etc; excise the
    #punctuation mark from last word
    last_word = word_list[-1]

    pos_period = last_word.find('.', 0, len(last_word)+1)
    pos_qmark = last_word.find('?', 0, len(last_word)+1)
    pos_exclam = last_word.find('!', 0, len(last_word)+1)

    #Get position of the punctuation mark at the end of the current sentence
    i = __get_first_punctuation_mark(pos_period, pos_qmark, pos_exclam)

    #No end-of-sentence punctuation mark in word
    if i == -1:
        return word_list

    #Replace last word in word list sans punctuation
    word_list[-1] = last_word[:i]

    return word_list



def find_start_end(sentence, text, start_search=0):
    '''Find the start and end positions of a sentence within a given text.
    Parameters text and sentence are both strings; start-pos is a non-negative
    integer. Function returns a tuple with start and end positions
    '''

    start_pos = 0
    end_pos = 0


    if sentence in text:
        start_pos = text.find(sentence, start_search, len(text) + 1)
        end_pos = start_pos + len(sentence) - 1
    else:
        return -1

    return (start_pos, end_pos)



def __get_first_punctuation_mark(period, qmark, exclam):
    '''Private helper function that returns the lowest index out of three.
    Returns lowest number (any if all the same value). If there is no punctuat-
    ion mark, return -1'''

    #No end-of-sentence punctuation mark
    if period == -1 and qmark == -1 and exclam == -1:
        return -1

    #We need to figure out which of the following end-sentence-punctuation
    #happens first in a text. The one with the smallest index
    #is one we're looking for
    pos_list = [period, exclam, qmark]

    #Negative values will always be the smaller index; get rid of them!!
    if period == -1 or qmark == -1 or exclam == -1:
        val = -1
        while val in pos_list:
            pos_list.remove(val)

    #Get position of the punctuation mark at the end of the current sentence
    return min(pos_list)

"""
Untested method - development cancelled 

def __is_expletive(text, pos):
    '''Determine whether end-of-sentence punctuation mark is the end of a
    cartoon bubble, e.g. "that god dosh-darn #$%!? rabbit!!"  We can do this
    by check the two previous characters. If they're not part of an ellipsis
    but have a !@#$%^&*? character,  then it's highly-likely its an expletive.

    Parameter text is the string object being examined; pos is the non-Negative
    integer position of the end-of-sentence punctuation mark. Return True if
    expletive found; False otherwise.
    '''
    #English sentences don't start with end-of-sentence punctuation marks;
    #index should be positive
    if i < 2:
        return False

    c_pos = text[pos]

    #Cartoon-bubble expletives don't end in a period
    if c_pos == '.':
        return False

    #Look at previous characters before pos
    c_1 = text[pos - 1]
    c_2 = text[pos - 2]

    #If previous two characters are periods, ignore => ellipsis
    if c_1 == '.' or c_2 == '.':
        return False

    #See whether the next two characters for part of an expletive
    if c_1 in "!@#$%^&*?" and c_2 in "!@#$%^&*?":
        return True

"""


if __name__ == "__main__":


    print("\nTesting get_sentences")

    text = '''
    My name is Alex. I have a dog called Gruff. He smells like baby-powder.
    I also have a cat called Blinky?! She's special! Would you like
    to play with her? Let me know!!!!'''

    sent_list = get_sentences(text)
    print(f"Sentence list length {len(sent_list)}")
    if len(sent_list) > 0:
        for x in sent_list:
            print(x)

    for sentence in sent_list:
        print(f"Length = {len(get_words(sentence))}; Words: {get_words(sentence)}")

    print("DOING FILE TEST....")
    print("++++++++++++++++++++")

    file_handler = open("input.txt")
    file_data = file_handler.read()
    #print(file_data)

    sent_list = get_sentences(file_data)

    print(f"Sentence list length {len(sent_list)}")
    if len(sent_list) > 0:
        for x in sent_list:
            print(x)

    print("\n++++++++++++++++++++++++++++++++++")
    print("Sentences more than seven words!!")
    print("++++++++++++++++++++++++++++++++++\n")

    for sentence in sent_list:
        #print(f"Length = {len(get_words(sentence))}; Words: {get_words(sentence)}")
        word_list = get_words(sentence)
        if len(word_list) > 7:
            print(f"# words = {len(word_list)} => {sentence}")

    positions = find_start_end(sent_list[0], file_data, 0)
    print(f"Start and end pos for 1st sentence: {positions}")

    test_sentence = file_data[positions[0]:positions[1] +1]
    print(test_sentence)

    positions = find_start_end(sent_list[1], file_data, positions[0])
    print(f"Start and end pos for 2nd sentence: {positions}")

    #Compare sentences
    test_sentence = file_data[positions[0]:positions[1]+1]
    print(test_sentence)

    if test_sentence == sent_list[1]:
        print("Sentences match!")
    else:
        print("Sentences don't match")
