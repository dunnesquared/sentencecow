from nose.tools import *
from leguinncounter import LeGuinnCounter
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
    lg = LeGuinnCounter(text)
    expected = True
    assert_equal(isinstance(lg, LeGuinnCounter), expected)

    # Check contents of attribute text
    expected = "Blah! Blah, blah."
    assert_equal(lg.text, expected)

    # Check contents of attribute sentences
    expected = ["Blah!", " Blah, blah."]
    assert_equal(lg.sentences, expected)

    # Pass invalid Argument
    text = None
    assert_raises(TypeError, LeGuinnCounter, text)

    # Pass empty string ""
    text = ""
    expected = ("", [])
    lg = LeGuinnCounter(text)
    assert_equal((lg.text, lg.sentences), expected)

    # Pass empty string  "   \n\t  \r\n  "
    text = "   \n\t  \r\n  "
    expected = expected = ("   \n\t  \r\n  ", [])
    lg = LeGuinnCounter(text)
    assert_equal((lg.text, lg.sentences), expected)



def test_parse():
    '''Test Cases:
        # Pass valid argument
        # Pass invalid argument
    '''

    # Pass valid argument
    text = "Blah! Blah, blah."
    lg = LeGuinnCounter(text)
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
    lg = LeGuinnCounter(text)
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
    lg = LeGuinnCounter(text)
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
    lg = LeGuinnCounter(text)
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
    lg = LeGuinnCounter(text)
    before = len(lg.sentences)
    lg.merge_next(0)
    after = len(lg.sentences)
    assert_equal(before, after)


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
