
'''
Notes: What about ?! or !!!!! or ...  ? Replace them before parsing??

To Do:
* Write driver to detect whether sentences are 7 words or less

* Unit test get_sentences and get_words using nosetests
* Create a Sentence class; return a Sentence object in get_sentences??
* Refactor get_sentences and get_word to encapsulate duplicate code in a method
(i.e. finding the first end-of-sentence punctuation point)

Done:
* Refactor get_sentences to return map of data
* Refactor get_sentences so that delimiters are ". ", etc, so as to handle !!! or ?! or ...
* Refactor get_sentences so to only return a list of sentences
* Refactor get_words so that delimiters are ". ", etc, so as to handle !!! or ?! or ...
* Debug find_start_end
* Write a function that will find the beginning and end of sentence in a text
'''

import textwrap
import re


def get_sentences(text):
    '''Parse text into a list of sentences. Parameter 'text' is string object.'''

    #Clean text up a bit: remove trailing/leading spaces, indents
    #You'll need to do this for each sentence too
    text = text.strip()
    text = textwrap.dedent(text)

    #Escape characters such as \n or \t mess up the parsing below; take 'em out
    text = re.sub('[\n\t\r]', ' ', text)

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

        #No end-of-sentence punctuation marks left in text => no more sentences!
        if pos_period == -1 and pos_qmark == -1 and pos_exclam == -1:
            return sent_list #empty list

        #To get the next sentence we need to figure out which of the following
        #end-sentence-punctuation happens first. The one with the smallest index
        #is one we're looking for
        pos_list = [pos_period, pos_exclam, pos_qmark]

        #Negative values will always be the smaller index; get rid of them!!
        if pos_period == -1 or pos_qmark == -1 or pos_exclam == -1:
            val = -1
            while val in pos_list:
                pos_list.remove(val)

        #Get position of the punctuation mark at the end of the current sentence
        i = min(pos_list)

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

    #No end-of-sentence punctuation marks in word
    if pos_period == -1 and pos_qmark == -1 and pos_exclam == -1:
        return word_list

    #To get the next sentence we need to figure out which of the following
    #end-sentence-punctuation happens first. The one with the smallest index
    #is one we're looking for
    pos_list = [pos_period, pos_exclam, pos_qmark]

    #Negative values will always be the smaller index; get rid of them!!
    if pos_period == -1 or pos_qmark == -1 or pos_exclam == -1:
        val = -1
        while val in pos_list:
            pos_list.remove(val)

    #Get position of the punctuation mark at the end of the current sentence
    i = min(pos_list)

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

    #See whether sentence is text; if not return -1
    #If yes, then get start_pos of sentence staring from
    #start_pos parameter ; end pos should be start_pos + len(sentence)
    #return (start, end)


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
