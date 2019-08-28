"""A module containing class necessary to implement functionality that will
check whether number of words in a sentence is below a certain threshold

To Do:
    * Comment code properly
    * pylint/pycode style code
    * Clean up main
    * add attributes to module doc
    * design flask app/jinja pages
    * test LeGuinnSentence, generate_LGSentenceList

Done:
    * implement for loop in sentences_more_than as while loop to get index
    * Figure out indent bug with triple quotes
    * Write test code

Notes:
    * Merge sentences can't be done with long sentences (makes no sense);
    user needs to see all the sentences and select which ones to merge

"""

from textanalysis import textanalysis as ta
import textwrap as tw
import re


class LeGuinnSentence:
    """Contains contents of sentence in text as well relevant meta-data for
    this application.
    """

    def __init__(self, content="", start="0", end="0", isOver=False):
        self.content = content
        self.start = start
        self.end = end
        self.isOver = isOver
        self.whitespace = ""

    def __str__(self):
        '''Print vitals'''

        return f'''
                    content: {self.content}
                    start: {self.start}
                    end : {self.end}
                    isOver: {self.isOver}
                '''


class LeGuinnCounter:
    """Checks that sentences in a text are less than X number of words.
    """

    def __init__(self, text):
        '''Save original text and sentence-parsing of it

        Attributes:
            sentences (list): list of sentences from parsed text
        '''
        self.parse(text)


    def parse(self, text):
        '''Return sentences in text; saves text for future processing

        Attributes:
            text (str): text to be parsed

        Returns:
            sentences (list): list of sentences from parsed text
        '''

        # Save text for future processing
        self.text = text
        self.sentences = ta.get_sentences(text)

        return self.sentences


    def count_words(self, sentence):
        '''Count the number of words in a sentence

        Args:
            text (str): string in which words are to be counted

        Returns:
            (int): number of words in text
        '''

        return len(ta.get_words(sentence))


    def more_than(self, sentence, max = 20):
        '''Returns whether sentence has more than max words

        Args:
            sentence (str): sentence whose words are to be counted
            max (int): max number of words allowed per sentence. If no max,
                       is specified the default is 20 words.

        Raises:
            ValueError: max is a non-positive integer (i.e. less than 1)

        Returns:
            True (bool): sentence has more than max words
            False (bool): sentence has fewer or the same max words
        '''

        if max < 1:
            raise ValueError("Max must be a number >= 1.")

        num_words = self.count_words(sentence)

        if num_words > max:
            return True

        return False


    def sentences_more_than(self, max = 20):
        '''Returns list of maps. Each map contains the sentence that has more
        than the max number of words, where the sentence in the text starts;
        where it ends. If all sentences have the same number or few than max,
        empty list returned

        Args:
            max (int): max number of words allowed per sentence

        Raises:
            ValueError: max is a non-positive integer (i.e. less than 1)

        Returns:
            long_sentences (list): a list of maps. Each item has three entries
                sentence (str): sentence that has more than max words
                start (int): index where the sentence starts in the text
                end (int): index where the sentence ends in the text
                index (int): index of sentence in sentence list
        '''

        long_sentences = []
        start_pos = 0

        for sentence in self.sentences:
            if self.more_than(sentence, max):
                start, end = ta.find_start_end(sentence, self.text, start_pos)
                item = {
                        'sentence':sentence,
                        'start': start,
                        'end': end,
                        'wordcount': self.count_words(sentence)
                        }
                long_sentences.append(item)
                # Do not start searching for positions at beginning of text;
                # Start from where the last sentence ended:
                # What happens if you have same sentence more than once?!
                start_pos = end + 1

        return long_sentences


    def merge_next(self, index):
        '''Modifies list of sentences such that sentence referenced at index is
        is merged with next sentence in list

        Args:
            index (int): index of primary sentence

        Raises:
            ValueError: trying to combine sentences when sentence list is empty

            IndexError: index is less than zero or greater the number of
                        sentences in the sentence list.

        Returns:
            void: Modifies sentences list: new sentence takes place of sentence
                  at index; sentence at index + 1 removed.
        '''

        # No sentences to merge: do nothing.
        if len(self.sentences) == 0:
            raise ValueError("Merge cannot be performed on an empty sentence list.")

        # Index out of bounds
        if index < 0 or index >= len(self.sentences):
            raise IndexError("Index cannot be less than zero or larger " +
                             "than list")

        # Can't merge the last sentence with anything—don't do anything.
        if index != len(self.sentences) - 1:
            # Merge sentences
            curr = self.sentences[index]
            next = self.sentences[index + 1]

            # OLD CODE
            # self.sentences[index] = " ".join([curr, next])

            # NEW TEST CODE
            self.sentences[index] = curr + next

            # No need for that second sentence anymore
            self.sentences.pop(index + 1)


    def split_sentence(self, index, split_pos):
        '''Cuts a sentnece at specified position; add new sentence to
        sentence list.

        Args:
            index (int): index of sentence being split in sentence list
            split_pos (int): postion where sentence is to be cut

        Raises:
            ValueError: trying to split a sentence when sentence list is empty

            IndexError: index is less than zero or greater the number of
                        sentences in the sentence list; split_pos less than
                        zero or greater than length of sentence

        Return:
            void: Modifies sentences list: first part of cut sentence
            assigned to index; second part part inserted at index + 1
        '''
        # Algorithn
        # 1. Check for errors
        # 2. Get sentence at index; save first and second parts re split pos
        # 3. Check to see whether first part is only white spaces
            # Y - Do nothing, exit
            # N - Go to step 5
        # 4. Check to see whether second part is only white spaces
            # Y - Do nothing, exit
            # N - Go to step 5
        # 5. Replace sentence at index with first part
        # 6. Insert second sentence at position index + 1

        # No sentences to merge: do nothing.
        if len(self.sentences) == 0:
            raise ValueError("Split cannot be performed on an empty sentence list.")

        # Index out of bounds
        if index < 0 or index >= len(self.sentences):
            raise IndexError("Index cannot be less than zero or larger " +
                             "than list")

        # split_pos out of bounds
        sentence = self.sentences[index]

        if split_pos < 0 or split_pos > len(sentence):
            raise IndexError("split_pos cannot be less than zero or larger " +
                             "than sentence length")


        # Get first and second parts of sentence
        first_part = sentence[:split_pos]
        second_part = sentence[split_pos:]

        # DEBUG
        # white space characteres (i.e. not a valid sentence)
        print("sentence", repr(sentence))
        print("first_part:", repr(first_part))
        print("second_part:", repr(second_part))

        # No point in modifying sentence list if one of the parts is just
        firstOk = bool(len(first_part.strip()))
        secondOk = bool(len(second_part.strip()))

        if firstOk and secondOk:
            self.sentences[index] = first_part
            self.sentences.insert(index+1, second_part)



    def generate_LGSentenceList(self, text, sentlist, max):
        '''Return list of LGSentences given a list of string sentences

        Args:
            text (str): text of strings
            sentlist (list): list of sentences parsed from text
            max (int): Max number of words per sentence

        Returns:
            lg_sentlist (LGSentences): list of LGSentences
        '''

        print("***********DEBUGGING GENERATE_LGSENTENCES***************")
        print("=========================================================")
        print("")

        # Empty list of sentences sent as argument
        if not sentlist:
            return []

        lg_sentlist = []
        start_pos = ta.offset(text)

        print(f"\nDEBUG: start_pos = {start_pos}")

        for s in sentlist:

            print(f"\nDEBUG: start_pos = {start_pos}")
            print("\nDEBUG: leguincounter:generate_LGSentenceList, start, end = {}; sentence = {}\n".format(ta.find_start_end(s, text, start_pos), s))

            start, end = ta.find_start_end(s, text, start_pos)

            #New code - modeify start such that you get first position of non-white space character
            start += ta.offset(s)
            print(f"\nDEBUG: (start, end), offset accounted = {(start, end)}")


            print(f"DEBUG: leguincounter:generate_LGSentenceList, slice = {text[start:end]}\n")

            isOver = self.more_than(s, max)

            # Old code No strip
            # lg_sent = LeGuinnSentence(s, start=start, end=end, isOver=isOver)

            # New code - sentences stripped
            s = s.strip()
            lg_sent = LeGuinnSentence(s, start=start, end=end, isOver=isOver)

            lg_sentlist.append(lg_sent)

            # OLD CODE
            # start_pos = end + 1
            #NEW fix
            start_pos = end

        # Copy white-space characters before a sentence
        lg_sentlist = self.__whitespace_before(lg_sentlist, text)

        return lg_sentlist

# -------------------------PRIVATE--------------------------------------------

    def __whitespace_before(self, lg_sentlist, text):
        '''Return list of LeGuinnSentences such that any white-space characters
        before each sentence are saved

        Args:
            lg_sentlist (LeGuinnSentence []): A complete list of sentences
                                              in a text
            text (str): text from which whitespace characters will be copied

        Return:
            lg_sentlist (LeGuinnSentence []): An updated list with white-space
                                              preceding a sentence saved
        '''

        print(f"*******DEBUGGING __whitespace before*********")
        print(f"==============================================")

        # The index where you think the a sentence starts at in the text
        expected_start = 0

        for i in range(len(lg_sentlist)):

            # See whether there is a gap between the first character in LGSent-
            # ence and the next LGSentence. Gaps (should) imply whitespaces.
            highlight_start = lg_sentlist[i].start
            diff = highlight_start - expected_start

            print(tw.dedent(f'''
                expected_start = {expected_start}
                sentlist[i].start/highlight_start = {highlight_start}
                diff = {diff}
                sentlist[i].end = {lg_sentlist[i].end}
            '''))

            # If difference is more than just a space, copy the whitespace
            # string. We'll need it for highlighting the text in the presentat-
            # layer.
            if diff:
                lg_sentlist[i].whitespace = text[expected_start:highlight_start]
                # Bug in HTML rendering means newlines don't show up as they
                # would in the console. Adding an extra newline character
                # seems to fix this. (Code should probably not be in the
                # in the domain layer)
                print(f"DEBUG: whitepace characters before sentence {i} = {repr(lg_sentlist[i].whitespace)}, length = {len(lg_sentlist[i].whitespace)}")

                # OLD CODE
                # if lg_sentlist[i].whitespace.count('\n') == 1:
                #     lg_sentlist[i].whitespace = re.sub(r'[\n]', r'\n\n',
                #                                        lg_sentlist[i].whitespace)

                # Add an extra newline so highlighted text renders properly
                # This code should be in app.py (UI concern)
                if '\n' in lg_sentlist[i].whitespace:
                    lg_sentlist[i].whitespace = '\n' + lg_sentlist[i].whitespace

            #Reset exprected start
            # OLD
            # expected_start = lg_sentlist[i].end + 1

            #NEW
            expected_start = lg_sentlist[i].end


            print(f"DEBUG: whitepace characters for sentence {i} = {repr(lg_sentlist[i].whitespace)}")
            print(f"DEBUG: content of sentence {i} = {lg_sentlist[i].content}")

        print(f"*******END __whitespace before*********")
        print(f"==============================================")

        return lg_sentlist





# ---------------------MAIN------------

def modify_text(text, start, stop):
    '''Modifies text between start and stop indices, inclusive. Returns string
    object referencing modified text'''

    before = text[0:start]
    after = text[stop+1:len(text)+1]
    mod = text[start:stop+1]

    #Make the change! In this case, make text uppercase
    mod = mod.upper()

    return before + mod + after


if __name__ == "__main__":
    text = '''
    This is a sample text. Do you like it? I hope so.
    We're having so much trouble getting this program finished. Bye for now!!
    '''

    lg_counter = LeGuinnCounter(tw.dedent(text))
    print(lg_counter.sentences)

    print("#####")
    lg_sentlist = lg_counter.generate_LGSentenceList(text, lg_counter.sentences, 4)
    for s in lg_sentlist:
        print(s)
    print("#####")

    sentences = lg_counter.sentences

    print(lg_counter.more_than(sentences[0],3))

    max = 4
    long_sentences = lg_counter.sentences_more_than(max)

    for item in long_sentences:
        print(item)

    # modify text -> to be implemented in JS
    for item in long_sentences:
        text = modify_text(text, item['start'], item['end'])

    print("")
    print(tw.dedent(text))
    print("")

    lg_counter.merge_next(0)
    lg_counter.merge_next(0)
    lg_counter.merge_next(0)
    lg_counter.merge_next(0)
    lg_counter.merge_next(0)
    lg_counter.merge_next(0)
    lg_counter.merge_next(0)
    lg_counter.merge_next(0)
