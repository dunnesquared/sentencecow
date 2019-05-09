
'''
Notes: What about ?! or !!!!! or ...  ? Replace them before parsing??
'''

import textwrap



def get_sentences(text):
    '''Parse text into a list of sentences. Each list item contains the original
     sentence as well as its start and end position in the text. Parameter text
     is string object.'''

    #Clean text up a bit: remove trailing/leading spaces, indents
    #You'll need to do this for each sentence too
    text = text.strip()
    text = textwrap.dedent(text)

    start = 0
    end_of_text = len(text)

    #Initialize variable that will keep track of the end of each sentence
    i = 0

    sentence = ""
    sent_list = []

    while start <= end_of_text:
        #Search text for first occurence of the following punctuation marks
        pos_period = text.find('.', start, end_of_text+1)
        pos_qmark = text.find('?', start, end_of_text+1)
        pos_exclam = text.find('!', start, end_of_text+1)

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

        #Your next sentence starts two characters away from the end of the
        #previous sentence (in many langauges there is a space before the
        #first letter of a sentence)
        start = i + 2

    return sent_list



def wordcount_leq(phrase, limit):
    '''Determine whether number of words in given string is lesss than or equal to
    indicated limit. Parameter phrase is a string, limit a positive integer'''
    pass



if __name__ == "__main__":
    print("\nTesting get_sentences")

    text = '''
    My name is Alex. I have dog called Gruff. He smells like baby-powder.
    I also have a cat called Blinky. She's special! Would you like
    to play with him? Let me know.'''

    sent_list = get_sentences(text)
    print(f"Sentence list length {len(sent_list)}")
    if len(sent_list) > 0:
        for x in sent_list:
            print(x)
