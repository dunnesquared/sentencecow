import textanalysis as ta

'''
To Do:
Pass modify_text a function that actually does the modification
'''


def modify_text(text, start, stop):
    '''Modifies text between start and stop indices, inclusive. Returns string
    object referencing modified text'''

    before = text[0:start]
    after = text[stop+1:len(text)+1]
    mod = text[start:stop+1]

    #Make the change! In this case, make text uppercase
    mod = mod.upper()

    return before + mod + after


#Get file data
file_handler = open("input.txt")
file_data = file_handler.read()

#Print file data
print("\nORIGINAL TEXT:")
print("==============")
print(file_data)

#Extract sentences
sent_list = ta.get_sentences(file_data)

#Detect which ones are more than seven words
print("\nSentences more than 7 words long:")
print("=================================")

#Store long sentences in here
long_sent_list = []

for sentence in sent_list:
    word_list = ta.get_words(sentence)
    if len(word_list) > 7:
        long_sent_list.append(sentence)
        print(f"# words = {len(word_list)} => {sentence}")

#Make those upper-case for those that are!
    #get start and end position of long sentences

#Modify text with long sentences so they stand-out; in this case, make them
#upper case
start_pos = 0
positions = ()  #hold the start and end positions of long sentences in text
new_text = file_data    #holds text post-modifications

for sentence in long_sent_list:

    positions = ta.find_start_end(sentence, new_text, start_pos)

    #DEBUG
    #print(positions)
    #print(file_data[positions[0]:positions[1]+ 1])

    #modify text
    new_text = modify_text(new_text, positions[0], positions[1])

    #No point in starting search for the beginning. A relative start position
    #should also help in the case where we may have long sentences that are
    #identical in different parts of the text
    start_pos = positions[1] + 1


#Show the changes!
print("\n\nMODIFIED TEXT:")
print("==============")
print(f"{new_text}")
