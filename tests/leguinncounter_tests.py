from nose.tools import *
from leguincounter import LeGuinCounter
from random import randint

def test_init():
    '''Test Cases:
        - Returns expected object
        - Check contents of attribute text
        - Check contentes of attribute sentences
        - Pass invalid argument
        - Pass empty string ""
        - Pass empty string "   \n\t  \r\n  "
    '''

    # Returns expected object
    text = "Blah! Blah, blah."
    lg = LeGuinCounter(text)
    expected = True
    assert_equal(isinstance(lg, LeGuinCounter), expected)

    # Check contents of attribute text
    expected = "Blah! Blah, blah."
    assert_equal(lg.text, expected)

    # Check contents of attribute sentences
    expected = ["Blah!", " Blah, blah."]
    assert_equal(lg.sentences, expected)

    # Pass invalid Argument
    text = None
    assert_raises(TypeError, LeGuinCounter, text)

    # Pass empty string ""
    text = ""
    expected = ("", [])
    lg = LeGuinCounter(text)
    assert_equal((lg.text, lg.sentences), expected)

    # Pass empty string  "   \n\t  \r\n  "
    text = "   \n\t  \r\n  "
    expected = expected = ("   \n\t  \r\n  ", [])
    lg = LeGuinCounter(text)
    assert_equal((lg.text, lg.sentences), expected)



def test_parse():
    '''Test Cases:
        # Pass valid argument
        # Pass invalid argument
    '''

    # Pass valid argument
    text = "Blah! Blah, blah."
    lg = LeGuinCounter(text)
    lg.parse(text)
    expected = ["Blah!", " Blah, blah."]
    assert_equal(lg.sentences, expected)

    # Pass invalid argument
    text = None
    assert_raises(TypeError, lg.parse , text)


def test_count_words():
    '''Test Cases:
        - invalid input
        - empty string
        - empty string with spaces
        - non-empty string = 1 word
        - non-empty = random number of words
    '''

    # invalid input
    text = "Blah! Blah, blah."
    lg = LeGuinCounter(text)
    assert_raises(TypeError, lg.count_words, 7)

    # empty string
    text = ""
    lg.parse(text)
    expected = 0
    assert_equal(lg.count_words(text), expected)

    # empty string with spaces
    text = '''


    '''
    lg.parse(text)
    expected = 0
    assert_equal(lg.count_words(text), expected)

    # non-empty string = 1 word
    text = "Eeyore"
    lg.parse(text)
    expected = 1
    assert_equal(lg.count_words(text), expected)

    # random number of words
    val = randint(2, 1000)
    text = "Pizza! " * val
    expected = val
    assert_equal(lg.count_words(text), expected)


def test_morethan():
    '''Test Cases
    # valid sentence, invalid max = less than 1
    # empty sentece, valid max
    # valid input; sentence equal to max
    # valid input; sentence less than max
    # valid input; greater than max
    # bad input types
    # default max
    '''

    # valid sentence, invalid max = less than 1
    text = "My name is Alex. What's yours?"
    lg = LeGuinCounter(text)
    max = 0
    assert_raises(ValueError, lg.more_than, text, max)

    # empty sentece, valid max
    text = ""
    max = 3
    assert_equal(lg.more_than(text, max), False)

    # valid input; sentence equal to max
    text = "My name is Alex. What's yours?"
    max = 6
    assert_equal(lg.more_than(text, max), False)

    # valid input; sentence less than max
    text = "My name is Alex. What's yours?"
    max = 10
    assert_equal(lg.more_than(text, max), False)

    # valid input; sentence less than max
    text = "My name is Alex. What's yours?"
    max = 3
    assert_equal(lg.more_than(text, max), True)

    # bad input types
    assert_raises(TypeError, lg.more_than, 7, "whua?")

    # default max (20 words)
    assert_equal(lg.more_than(text), False)

def test_sentence_morethan():
    '''Test Cases
    # bad max value
    # no sentences over max
    # all sentences over max
    # some sentences over max
    '''

    text = '''
    This is a sample text. Do you like it? I hope so.
    We're having so much trouble getting this program finished. Bye for now!!
    '''

    # bad max value
    lg = LeGuinCounter(text)
    max = 0
    assert_raises(ValueError, lg.sentences_more_than, max)

    # no sentences over max
    max = 100
    expected = []
    assert_equal(lg.sentences_more_than(max), expected)

    # all sentences over max
    max = 1
    actual = len(lg.sentences_more_than(max))
    expected = 5
    assert_equal(actual, expected)

    # some sentences over
    max = 3
    actual = len(lg.sentences_more_than(max))
    expected = 3
    assert_equal(actual, expected)


def test_mergenext():
    '''Text Cases
    # Nothing to merge
    # Out of bounds to index: < 0
    # Out of bounds to index: > len(sentences)
    # Out of bounds index: trying to merge the last element with something else
    # Merging when there is only one sentence in list
    # Merging when there are multiple sentences in list
    # Multiple merges until everything is just one sentence
    '''

    # Nothing to merge
    text = ""
    lg = LeGuinCounter(text)
    before = len(lg.sentences)
    val = 0
    assert_raises(ValueError, lg.merge_next, val)
    #lg.merge_next(0)
    #after = len(lg.sentences)
    #assert_equal(before, after)


    text = '''
    This is a sample text. Do you like it? I hope so.
    We're having so much trouble getting this program finished. Bye for now!!
    '''
    lg.parse(text)

    # Out of bounds to index: < 0
    val = -100
    assert_raises(IndexError, lg.merge_next, val)

    # Out of bounds to index: > len(sentences)
    val = 100
    assert_raises(IndexError, lg.merge_next, val)

    # Out of bounds index: trying to merge the last element with something else
    val = len(lg.sentences) - 1
    before = len(lg.sentences)
    lg.merge_next(val)
    after = len(lg.sentences)
    assert_equal(before, after)

    # Merging when there is only one sentence in list
    text = "This is a single sentence."
    lg.parse(text)
    before = len(lg.sentences)
    lg.merge_next(0)
    after = len(lg.sentences)
    assert_equal(before, after)

    # Merging when there are multiple sentences in list
    text = '''
    This is a sample text. Do you like it? I hope so.
    We're having so much trouble getting this program finished. Bye for now!!
    '''
    lg.parse(text)
    lg.merge_next(1)
    expected = 4
    actual = len(lg.sentences)
    assert_equal(actual, expected)

    # Multiple merges until sentences can be merged no more!
    for n in range(10):
        lg.merge_next(0)

    expected = 1
    actual = len(lg.sentences)
    assert_equal(actual, expected)


# def test_split_sentence():
#     # 1. Normal case, minimal white spacing
#     # Check first sentence
#     # Check second sentence
#     # Check list size
#
#     # Setup
#     text = "This is a sentence with a footnote.[1] Crazy!"
#     split_pos = 38
#     i = 0
#     lg = LeGuinCounter(text)
#     lg.split_sentence(i, split_pos)
#
#
#     # Check first sentence
#     expected = 'This is a sentence with a footnote.[1]'
#     result = lg.sentences[i]
#     assert_equal(result, expected)
#
#     # Check second sentence
#     expected = ' Crazy!'
#     result = lg.sentences[i+1]
#     assert_equal(result, expected)
#
#     # Check size of list
#     expected = 2
#     result = len(lg.sentences)
#     assert_equal(result, expected)
#
#     # 2. Normal case, complicated whitespacing
#     text = '''This is a sentence with a footnote.[1] Crazy! It's followed by another.[2] And another.[3] This sentence is free.
# Just insane.
# Here's one last sentence with a footnote.[3]
# This sentence is on a separate line, but still atttached to the previous sentence.'''
#
#     # Check size BEFORE split
#     lg.parse(text)
#     expected = 4
#     result = len(lg.sentences)
#     assert_equal(result, expected)
#
#     # Split sentence 0 at split_pos = 38
#     split_pos = 38
#     i = 0
#     lg.split_sentence(i, split_pos)
#
#     # Test whether split worked: check sentences and list size
#     # Check first sentence
#     expected = 'This is a sentence with a footnote.[1]'
#     result = lg.sentences[i]
#     assert_equal(result, expected)
#
#     # Check second sentence
#     expected = ' Crazy!'
#     result = lg.sentences[i+1]
#     assert_equal(result, expected)
#
#     # Check size of list
#     expected = 5
#     result = len(lg.sentences)
#     assert_equal(result, expected)
#
#     # Test splitting the last sentence (4) at split pos 45
#     i = 4
#     split_pos = 45
#     lg.split_sentence(i, split_pos)
#
#     # Check first sentence
#     expected = "\nHere's one last sentence with a footnote.[3]"
#     result = lg.sentences[i]
#     assert_equal(result, expected)
#
#     # Check second sentence
#     expected = '''
# This sentence is on a separate line, but still atttached to the previous sentence.'''
#     result = lg.sentences[i+1]
#     assert_equal(result, expected)
#
#     # Check size of list
#     expected = 6
#     result = len(lg.sentences)
#     assert_equal(result, expected)
#
#
#     #Test error conditions
#
#     # Sentence index out of bounds
#     i = -1
#     split_pos = 5
#     assert_raises(IndexError, lg.split_sentence, i, split_pos)
#
#     i = 1000
#     assert_raises(IndexError, lg.split_sentence, i, split_pos)
#
#
#     # split pos out of bounds
#     i = 5
#     split_pos = -5
#     assert_raises(IndexError, lg.split_sentence, i, split_pos)
#
#     split_pos = 1000
#     assert_raises(IndexError, lg.split_sentence, i, split_pos)
#
#
#     # No sentences
#     lg.sentences = []
#     i = 0
#     split_pos = 3
#     assert_raises(ValueError, lg.split_sentence, i, split_pos)
#
#
#     # Test: multiple splits
#     text = "0.1.2.3.4."
#     lg.parse(text)
#
#     #Check size BEFORE split
#     expected = 1
#     result = len(lg.sentences)
#     assert_equal(result, expected)
#
#     # Do multiple splits
#     split_pos = 2
#     for i in range(0, 4):
#         lg.split_sentence(i, split_pos)
#
#     expected = 5
#     result = len(lg.sentences)
#     assert_equal(result, expected)
#
#     expected = ["0.", "1.",  "2.",  "3.",  "4."]
#     result = lg.sentences
#     assert_equal(result, expected)
#
#     # Split when there's nothing to split
#     text = "1."
#     lg.parse(text)
#     i, split_pos = 0, 1
#     lg.split_sentence(i, split_pos)
#     lg.split_sentence(i, 0) # split again
#
#     # Check sentence list length
#     expected = ['1', '.']
#     result = lg.sentences
#     assert_equal(result, expected)
#
#
#     # Split with blank characters
#     text = "\n\t\r\n123!\n\t\r\n"
#     lg.parse(text)
#     i = 0
#     split_pos = 4
#     lg.split_sentence(i, split_pos)
#
#     # Check sentence list length
#     expected = 1
#     result = len(lg.sentences)
#     assert_equal(result, expected)
#
#     # N.B. offset in textanalysis ignores leading white spaces of first sentence
#     # Trailing whitespaces discarded since sentence only take to terminating
#     # character
#     expected = "123!"
#     result = lg.sentences[i]
#     assert_equal(result, expected)
#
#     # Split at end of sentence
#     text = "Pizza!"
#     lg.parse(text)
#     i, split_pos = 0, 6
#     lg.split_sentence(i, split_pos)
#
#     expected = 1
#     result = len(lg.sentences)
#     assert_equal(result, expected)
#
#     expected = "Pizza!"
#     result = lg.sentences[i]
#     assert_equal(result, expected)


def test_split_sentence():
    # 1. Normal case, minimal white spacing
    # Check first sentence
    # Check second sentence
    # Check list size

    # Setup
    text = "This is a sentence with a footnote.[1] Crazy!"
    i = 0
    sub = "This is a sentence with a footnote.[1]"
    lg = LeGuinCounter(text)
    lg.split_sentence(i, sub)

    # Check first sentence
    expected = 'This is a sentence with a footnote.[1]'
    result = lg.sentences[i]
    assert_equal(result, expected)

    # Check second sentence
    expected = ' Crazy!'
    result = lg.sentences[i+1]
    assert_equal(result, expected)

    # Check size of list
    expected = 2
    result = len(lg.sentences)
    assert_equal(result, expected)

    # 2. Normal case, complicated whitespacing
    text = '''This is a sentence with a footnote.[1] Crazy! It's followed by another.[2] And another.[3] This sentence is free.
Just insane.
Here's one last sentence with a footnote.[3]
This sentence is on a separate line, but still atttached to the previous sentence.'''

    # Check size BEFORE split
    lg.parse(text)
    expected = 4
    result = len(lg.sentences)
    assert_equal(result, expected)

    # Split sentence 0 at split_pos = 38
    sub = 'This is a sentence with a footnote.[1]'
    i = 0
    lg.split_sentence(i, sub)

    # Test whether split worked: check sentences and list size
    # Check first sentence
    expected = 'This is a sentence with a footnote.[1]'
    result = lg.sentences[i]
    assert_equal(result, expected)

    # Check second sentence
    expected = ' Crazy!'
    result = lg.sentences[i+1]
    assert_equal(result, expected)

    # Check size of list
    expected = 5
    result = len(lg.sentences)
    assert_equal(result, expected)

    # Test splitting the last sentence (4) at split pos 45
    i = 4
    sub = "Here's one last sentence with a footnote.[3]"
    lg.split_sentence(i, sub)

    # Check first sentence
    expected = "\nHere's one last sentence with a footnote.[3]"
    result = lg.sentences[i]
    assert_equal(result, expected)

    # Check second sentence
    expected = '''
This sentence is on a separate line, but still atttached to the previous sentence.'''
    result = lg.sentences[i+1]
    assert_equal(result, expected)

    # Check size of list
    expected = 6
    result = len(lg.sentences)
    assert_equal(result, expected)


    #Test error conditions

    # Sentence index out of bounds
    i = -1
    sub= "Hello."
    assert_raises(IndexError, lg.split_sentence, i, sub)

    i = 1000
    assert_raises(IndexError, lg.split_sentence, i, sub)

    # No sentences
    lg.sentences = []
    i = 0
    sub = "Hello"
    assert_raises(ValueError, lg.split_sentence, i, sub)

    #Substring empty
    text = "This is a sentence with a footnote.[1] Crazy!"
    lg.parse("This is a sentence with a footnote.[1] Crazy!")
    i = 0
    sub = ""
    expected = ["This is a sentence with a footnote.[1] Crazy!"]
    result = lg.sentences
    assert_equal(result, expected)


    #Substring white characters only
    lg.sentences = []
    i = 0
    sub = " \n \r\t \n"
    assert_raises(ValueError, lg.split_sentence, i, sub)



    # Test: multiple splits
    text = "0.1.2.3.4."
    lg.parse(text)

    #Check size BEFORE split
    expected = 1
    result = len(lg.sentences)
    assert_equal(result, expected)

    # Do multiple splits
    lg.split_sentence(0, "0.")
    lg.split_sentence(1, "1.")
    lg.split_sentence(2, "2.")
    lg.split_sentence(3, "3.")

    expected = 5
    result = len(lg.sentences)
    assert_equal(result, expected)

    expected = ["0.", "1.",  "2.",  "3.",  "4."]
    result = lg.sentences
    assert_equal(result, expected)

    # Split when there's nothing to split
    lg.split_sentence(2, "2.")
    expected = ["0.", "1.",  "2.",  "3.",  "4."]
    result = lg.sentences
    assert_equal(result, expected)

    #Split again and again
    lg.split_sentence(2, "2")
    lg.split_sentence(2, "2")
    expected = ["0.", "1.",  "2", ".", "3.",  "4."]
    result = lg.sentences
    assert_equal(result, expected)

    # Split with blank characters
    text = "You!\n\t\r\n123!\n\t\r\n"
    lg.parse(text)
    i = 1
    sub = "123!"
    lg.split_sentence(i, sub)

    # Check sentence list length
    expected = 2
    result = len(lg.sentences)
    assert_equal(result, expected)

    expected = ["You!", "\n\t\r\n123!"]
    result = lg.sentences
    assert_equal(result, expected)

#
