"""Module that supports sentence extraction, analysis and modification.

This module provides classes to support the extraction, analysis and
modification of sentences in a text. While it heavily uses and extends
the functionality defined in module 'textanalysis', it adds unique features
such as merging and splitting sentences. These last provide solutions to the
cases where 'textanalysis' parses a text incorrectly (read module
documentation for more details).

Two classes provide the functionality of this module: LeGuinSentence
and LeGuinCounter. Both classes were not developed in isolation of
the needs of the presentation layer of the greater app to which it belongs,
but with them strongly in mind. While separation of concerns is mostly achieved
in these classes, there is some unwanted HTML UI accomodation in
LeGuinCounter's sole private method. _whitespace_before. Any future
improvements to this module should include shifting this code out of this class
into the presentation layer.

The classes here get the job done, but their design could've been a lot better
with more forethought. Improve it as you will, but be warned: some of this
code is delicate and the result of extensive testing and debugging. Proceed
cautiously...
"""


from textanalysis import textanalysis as ta


class LeGuinSentence:
    """A class used to store metadata about a sentence within a text.

    Metadata can be useful for various applications. One application is to
    support the highlighting of a sentence in a text.

    Attributes:
        content (str): the content of the sentence itself.
        start (int): index where sentence starts in a text.
        end (int): index where sentence ends in a text.
        is_over (bool): whether sentence is over defined word max
        whitespace (str): leadning whitespace before a sentence
    """

    def __init__(self, content="", start=0, end=0, is_over=False):
        """Inits LeGuinSentence class."""
        self.content = content
        self.start = start
        self.end = end
        self.is_over = is_over
        self.whitespace = ""

    def __str__(self):
        """Prints values of a LeGuinnSentence class object."""

        return f'''
                    content: {self.content}
                    start: {self.start}
                    end : {self.end}
                    is_over: {self.is_over}
                '''


class LeGuinCounter:
    """A class that extracts, analyzes and modifies sentences in a text.

    Attributes:
        text (str): original text
        sentences (list <str>): list of sentences from parsed text. Note that
                                sentences include any leading whitespace
                                attached to them.
    """

    def __init__(self, text):
        """Inits LeGuinCounter indirectly via parse method.

        Args:
            text (str): original text
        """
        self.parse(text)

    def parse(self, text):
        """Parse sentences from a text and store in list.

        Args:
            text (str): text to be parsed

        Returns:
            sentences (list <str>): list of sentences from parsed text
        """

        # Save text for future processing
        self.text = text
        self.sentences = ta.get_sentences(text)

        return self.sentences

    def count_words(self, sentence):
        """Counts the number of words in a sentence

        Args:
            sentence (str): string in which words are to be counted.

        Returns:
            (int): number of words in text,
        """

        return len(ta.get_words(sentence))

    def more_than(self, sentence, word_max=20):
        """Returns whether sentence has more than max words.

        Args:
            sentence (str): sentence whose words are to be counted.
            word_max (int): max number of words allowed per sentence.
                            If no max, is specified the default is 20 words.

        Raises:
            ValueError: max is a non-positive integer (i.e. less than 1).

        Returns:
            (bool): True if sentence has more than max words; False if not.
        """

        if word_max < 1:
            raise ValueError("Max must be a number >= 1.")

        num_words = self.count_words(sentence)

        if num_words > word_max:
            return True

        return False

    def sentences_more_than(self, word_max=20):
        """Gets information about sentences that have more than the
        passed max number of words.

        If all sentences are below or equal to the maximum, an empty list
        is returned. Otherwise, the method returns a list of maps where
        each entry contains a sentence that is over the defined maximum
        amount of words, along with metadata about that sentence.

        Each entry map contains the following data:
            sentence (str): sentence that has more than max words.
            start (int): index where the sentence starts in self.text.
            end (int): index where the sentence ends in the self.text.
            word_count (int): number of words in a sentence.

        Args:
            word_max (int): max number of words allowed per sentence.

        Raises:
            ValueError: word_max is a non-positive integer (i.e. less than 1).

        Returns:
            long_sentences (list <map>): a list of maps of sentences over
                                         the passed word maximum; empty if
                                         sentences are not over.
        """

        long_sentences = []

        start_pos = 0 # Where to begin analysis of text

        for sentence in self.sentences:

            if self.more_than(sentence, word_max):

                # Find where sentence starts and ends in a text
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
                # what happens if you have same sentence more than once?!

                start_pos = end + 1

        return long_sentences

    def merge_next(self, index):
        """Modifies list of sentences such that sentence referenced at index is
        is merged with next sentence in list.

        Args:
            index (int): index of leading sentence in merge.

        Raises:
            ValueError: trying to combine sentences when sentence list is
                        empty.

            IndexError: index is less than zero or greater the number of
                        sentences in the sentence list.
        """

        # No sentences to merge: do nothing.
        if len(self.sentences) == 0:
            raise ValueError("Merge cannot be performed on an empty " +
                             "sentence list.")

        # Index out of bounds
        if index < 0 or index >= len(self.sentences):
            raise IndexError("Index cannot be less than zero or larger " +
                             "than list")

        # Can't merge the last sentence with anything, so don't do anything.
        if index != len(self.sentences) - 1:

            # Merge sentences
            curr = self.sentences[index]
            next_sentence = self.sentences[index + 1]
            self.sentences[index] = curr + next_sentence

            # No need for that second sentence anymore
            self.sentences.pop(index + 1)

    def split_sentence(self, i, sub):
        """Cuts a sentence at end where substring sub ends; adds new sentence
        to sentence list.

        Args:
            i (int): index of sentence in sentence list to be split.
            sub (str): substring to be matched in sentences[i].

        Raises:
            ValueError: trying to split a sentence when sentence list is empty.

            IndexError: index is less than zero or greater the number of
                        sentences in the sentence list.
        """

        # No sentences to split; shouldn't be splitting here
        if len(self.sentences) == 0:
            raise ValueError("Split cannot be performed on an empty " +
                             "sentence list.")

        # Index out of bounds
        if i < 0 or i >= len(self.sentences):
            raise IndexError("Index cannot be less than zero or larger " +
                             "than list")

        # Do nothing if the substring is empty or has only
        # whitespace characters
        if len(sub.strip()) == 0:
            return

        sentence = self.sentences[i]

        # Because of newline characters given as CRLF in HTML/Windows and LF in
        # UNIX and JS normalizes CRLF to LF (I think), finding the substring i
        # in the above sentence will likely fail any where you have a newline
        # space in your text. Easiest just to find non-white space characters
        sub = sub.strip()

        # Get first and second parts of sentence
        _, end = ta.find_start_end(sub, sentence)
        first_part = sentence[0:end]
        second_part = sentence[end:]

        # No point in modifying sentence list if one of the parts is empty.
        first_ok = bool(len(first_part.strip()))
        second_ok = bool(len(second_part.strip()))

        if first_ok and second_ok:
            self.sentences[i] = first_part
            self.sentences.insert(i+1, second_part)

    def generate_LGSentenceList(self, text, sentlist, word_max):
        """Converts list of string sentences into a list of LeGuinSentence
           objects.

        Args:
            text (str): text from sentences originally parsed.
            sentlist (list <str>): list of sentences parsed from text
            word_max (int): Max number of words per sentence

        Returns:
            lg_sentlist (list <LGSentence>): list of LeGuinSentence objects.
                                             [] returned if sentlist empty.
        """

        # Empty list of sentences sent as argument
        if not sentlist:
            return []

        lg_sentlist = []

        # Start scan at first non whitespace char
        start_pos = ta.offset(text)

        for s in sentlist:
            # Gather data about each sentence

            # Find where sentence starts and ends in text
            start, end = ta.find_start_end(s, text, start_pos)

            # Sentences in sentlist include whitespace characters.
            # Modify start such that you get first position of non-whitespace
            # character
            start += ta.offset(s)

            is_over = self.more_than(s, word_max)

            # Unlike class attribute, only non whitespace contents written to
            # a LeGuinSentence object
            s = s.strip()

            lg_sent = LeGuinSentence(s, start=start, end=end, is_over=is_over)
            lg_sentlist.append(lg_sent)

            # Continue text analysis at end of just-processed sentence
            start_pos = end

        # Copy whitespace characters before each sentence
        lg_sentlist = self.__whitespace_before(lg_sentlist, text)

        return lg_sentlist

    def __whitespace_before(self, lg_sentlist, text):
        """Returns list of LeGuinSentences such that any whitespace characters
           before a sentence in a text are saved to its corresponding
           LeGuinSentence object.

           This functionality is necessary to support 'highlighting' of text
           in presentation layer.

        Args:
            lg_sentlist (list <LeGuinSentence>): A list of sentences in text
                                                 along with metadata.

            text (str): text from which whitespace characters will be copied.

        Returns:
            lg_sentlist (list <LeGuinSentence>): An updated list with
                                                 leading whitespace characters
                                                 of a sentence saved.
        """

        # Index where you expect a sentence shoud start in a text. Right now,
        # at the beginngin (i.e. no offset)
        expected_start = 0

        for i in range(len(lg_sentlist)):

            # See whether there is a gap between where a sentence actually
            # starts in a text and where you expect it to.
            # Gaps (should) imply whitespaces.
            highlight_start = lg_sentlist[i].start
            diff = highlight_start - expected_start

            # If difference is more than just a space, copy the whitespace
            # string. We'll need it for highlighting the text in the presentat-
            # layer.
            if diff:
                lg_sentlist[i].whitespace = text[expected_start:highlight_start]

                # Bug(?) in HTML rendering means newlines don't show up as they
                # would in the console. Adding an extra newline character
                # seems to fix this. Admittedly, this code should probably not
                # be in this class, but in a class that is more concerned with
                # the UI.

                # Add an extra newline so highlighted text renders properly
                if '\n' in lg_sentlist[i].whitespace:
                    lg_sentlist[i].whitespace = '\n' + lg_sentlist[i].whitespace

            # Reset expected start so next sentence can be processed
            expected_start = lg_sentlist[i].end

        return lg_sentlist


# ----------------------------------MAIN---------------------------------------


if __name__ == "__main__":
    pass
