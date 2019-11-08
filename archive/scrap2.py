"""

To Do:
    * have textbox to enter max words
    * add word count to long sentence output
    * create a corrections page to merge sentences

"""
#old driver from textanalysis

import os  # for driver test code below

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


        '''
        i = 0
        for i in range(len(self.sentences)) :
            if self.more_than(sentences[i], max):
                start, end = ta.find_start_end(sentences[i], self.text, start_pos)
                item = {'sentence':sentences[i], 'start': start, 'end': end, 'index': i}
                long_sentences.append(item)
                start_pos = end + 1
        '''


<!---
{% if answer >= 0 %}
    <p class="answer"> {{answer}} </p>
{% else %}
    No answer possible.
{% endif %}
-->

'''
Once upon a time, there was a dog called Tutu. He was nice. If you met him, you would like him too.
Have you a dog? Say yes!!
'''


'''
BUGGY TEXT

#Last sentence is ignored. Why?
#If you put a period at the end of the last R in U.S.S.R., the sentence is processed

Once upon a time, there was a dog called Tutu. He was nice. If you met him, you would like him too. Have you a dog? Say yes!! He lived in the U.S.S.R I think.
'''


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


        '''Problem text
        - You pay a royalty fee of 20% of the gross profits you derive from
             the use of Project Gutenberg-tm works calculated using the method
             you already use to calculate your applicable taxes.  The fee is
             owed to the owner of the Project Gutenberg-tm trademark, but he
             has agreed to donate royalties under this paragraph to the
             Project Gutenberg Literary Archive Foundation.  Royalty payments
             must be paid within 60 days following each date on which you
             prepare (or are legally required to prepare) your periodic tax
             returns.  Royalty payments should be clearly marked as such and
             sent to the Project Gutenberg Literary Archive Foundation at the
             address specified in Section 4, "Information about donations to
             the Project Gutenberg Literary Archive Foundation."

        '''



        <!--Once upon a time, there was a dog called Tutu. He was nice. If you met him, you would like him too. Have you a dog? Say yes!! He lived in the U.S.S.R. I think. Or was it the U.S. of good ole A?-->



          <!-- Display message if input text over word count -->
        {% if is_over == True %}
          <textarea name="input_text" wrap="soft" onload="updateWordCount();" oninput="enableSubmit();">{{ input_text }}</textarea>
          <p class="over"> {{ msg }} </p>
        {% else %}
          <textarea name="input_text" wrap="soft" onload="updateWordCount();" oninput="enableSubmit();">Testing script...</textarea>
        {% endif %}


Problem text:
JS Issues
- [x] ‘!  !  !’ as three words in JS but three sentences with no words in Python??
- [x] ––– ——— being counted as words??
- [ ] Take out trailing white space so it’s not sent to user
- [ ] Have word_max set by app.py


Python Domain Issues
- [x] ‘!  !  !’ as three words in JS but three sentences with no words in Python??
- [x] Check in flask, ta that global values are being respected
- [x] Retest get_words to make sure it’s handling \n\t between words (I don’t believe it is); this is more a problem for server-side checking of numwords
- [x] Remove excess trailing whitespace from original text  (leave leading!!)
- [ ] Have word_max set by app.py
- [ ] Change LeGuinn to Le Guin
- [ ] Implement security fixes
- [x] See whether any speed or memory optimizations can be made (e.g. replacing lists with generators)
    - [x] No need to load abbreviations file at every iteration of getsentences
    - [x] Use set.disjoint to check abbreviations


Test

This is a sentence with a footnote.[1] Crazy! It's followed by another.[2] And another.[3] This sentence is free.
Just insane.
Here's one last sentence with a footnote.[3]
This sentence is on a separate line, but still atttached to the previous sentence.
