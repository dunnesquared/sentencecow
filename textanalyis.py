
'''
Notes: What about ?! or !!!!! or ...  ? Replace them before parsing??

To Do:

* Refactor get_sentences so to only return a list of sentences
* Write a function that will find the
* Refactor get_words so that delimiters are ". ", etc, so as to handle !!! or ?! or ...
* Test get_sentences and get words
* Create a Sentence class; return a Sentence object in get_sentences??

Done:
* Refactor get_sentences to return map of data
* Refactor get_sentences so that delimiters are ". ", etc, so as to handle !!! or ?! or ...

'''

import textwrap
import re


def get_sentences(text):
    '''Parse text into a map of sentences. Each item in the returned map
     contains the original sentence as well as its start and end position in
     the text. Parameter 'text' is string object.'''

    #Clean text up a bit: remove trailing/leading spaces, indents
    #You'll need to do this for each sentence too
    text = text.strip()
    text = textwrap.dedent(text)

    #Escape characters such as \n or \t mess up the parsing below; take 'em out
    text = re.sub('[\n\t\r]', ' ', text)

    #Add a space at the end so last sentence won't be ignored
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

        #Each item in the list isn't just a sentence; it also returns info
        #of where it starts and ends. You'll want to create a new entry every
        #time to avoid reference issueslear
        entry = {}
        entry['content'] = sentence
        entry['start_pos'] = start
        entry['end_pos'] = i


        #Add it to your list
        #sent_list.append(sentence)
        sent_list.append(entry)


        #Your next sentence starts two characters away from the end of the
        #previous sentence (in many langauges there is a space before the
        #first letter of a sentence)
        #start = i + 2
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
    word_list[-1] = last_word[:-1]

    return word_list



if __name__ == "__main__":

    print("\nTesting get_sentences")
    print("========================")

    text = '''
    My name is Alex. I have a dog called Gruff. He smells like baby-powder.
    I also have a cat called Blinky?! She's special! Would you like
    to play with her? Let me know...'''


    sent_list = get_sentences(text)
    print(f"Sentence list length {len(sent_list)}")
    if len(sent_list) > 0:
        for x in sent_list:
            print(x['content'])

    for sentence in sent_list:
        print(f"Length = {len(get_words(sentence['content']))}; Words: {get_words(sentence['content'])}")

    print("DOING FILE TEST....")
    print("++++++++++++++++++++")

    file_handler = open("input.txt")
    file_data = file_handler.read()
    #print(file_data)

    sent_list = get_sentences(file_data)

    print(f"Sentence list length {len(sent_list)}")
    if len(sent_list) > 0:
        for x in sent_list:
            print(x['content'])


    print("\n++++++++++++++++++++++++++++++++++")
    print("Sentences more than seven words!!")
    print("++++++++++++++++++++++++++++++++++\n")

    for sentence in sent_list:
        #print(f"Length = {len(get_words(sentence))}; Words: {get_words(sentence)}")
        word_list = get_words(sentence['content'])
        if len(word_list) > 7:
            print(f"# words = {len(word_list)} => {sentence['content']}")

    """
    print("\nTesting get_sentences")

    text = '''
    My name is Alex. I have a dog called Gruff. He smells like baby-powder.
    I also have a cat called Blinky. She's special! Would you like
    to play with her? Let me know.'''

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

        """




    #TO DO
    #Copy story into input.txt
    #Algo
        #Open file
        #Read file into string
        #Pass string into get sentences
        #Pass sentence list to get words
        #Iterate through word_list for each sentence; print sentences that
        #are more than 7 words long.
