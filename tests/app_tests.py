from nose.tools import *
from app import *
from flask import request
from leguinncounter import LeGuinnCounter

app.config['TESTING'] = True
web = app.test_client()

# !!!Change this to correct web server name in your app!!!
resource_name = '/leguinncounter'

'''
What to test for:
    #The following pre-merge and post-merge
        # No input
        # Whitespace input
        # Non-valid sentence input
        # Very, very large input

    #To test in merge only
        # Merge with no input
        # Merge where there is only one sentence
        # Merge several times when merege is no longer possible.
'''

def test_status_codes():
    # -----------GENERAL APP TESTS: No changes required----------------
    # Make sure GET works
    # Should return 200
    # rv = web.get('/', follow_redirects=True)
    # assert_equal(rv.status_code, 200)

    # Make sure GET works
    # should return 200 okay status_code
    rv = web.get(resource_name, follow_redirects=True)
    assert_equal(rv.status_code, 200)

    # Request other than GET and POST: e.g. trace, put
    rv = web.trace(resource_name, follow_redirects=True)
    assert_equal(rv.status_code, 405)

    rv = web.put(resource_name, follow_redirects=True)
    assert_equal(rv.status_code, 405)

    rv = web.delete(resource_name, follow_redirects=True)
    assert_equal(rv.status_code, 405)

    # Head request just returns header, aka no content
    rv = web.head(resource_name, follow_redirects=True)
    assert_in(b"", rv.data)

def test_form():
    # TEST CASES
    # No input
    # Whitespace input
    # Non-valid sentence input
    # Very, very large input - see last test function below
    # Input_text passed None
    # Max passed None
    # Very, very, large max
    # Negative max
    # Non-integer max
    # Valid, working input

    button = 'Count'

    # No input
    data = {"input_text" : "", 'max' : '4', 'submit_button': button}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Nothing to process!', rv.data)

    # No input
    input_text = "\n\t\r     \n\n\n\n\t   \t\t\r\r\r\n"
    max = '4'
    data = {"input_text" : input_text, 'max' : max, 'submit_button': button}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Nothing to process!', rv.data)

    # Non-valid sentence input
    input_text = "This is not a sentence Neither is this Why No punctuation"
    max = '4'
    data = {"input_text" : input_text, 'max' : max, 'submit_button': button}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Nothing to process!', rv.data)

    # Input_text passed None
    input_text = None
    data = {"input_text" : input_text, 'max' : max, 'submit_button': button}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Bad Request', rv.data)

    # Very large max
    input_text = "Once upon a time, there was named Tutu. He was nice."
    max = '9999999999'
    data = {"input_text" : input_text, 'max' : max, 'submit_button': button}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Parsed Text', rv.data)

    # Negative max
    max = '-5'
    data = {"input_text" : input_text, 'max' : max, 'submit_button': button}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Max must be a number &gt;= 1.', rv.data)
    #assert_raises(ValueError, web.post, resource_name, follow_redirects=True, data=data)

    # Non-integer max
    max = "Are you having fun yet?!"
    data = {"input_text" : input_text, 'max' : max, 'submit_button': button}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b"Bad input: &#39;max&#39; can only be a positive whole number.", rv.data)

    max = None
    data = {"input_text" : input_text, 'max' : max, 'submit_button': button}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Bad Request', rv.data)

    # Valid, working input
    input_text = "Once upon a time, there was a dog called Tutu. He was nice. If you met him, you would like him too."
    max = 7
    data = {"input_text" : input_text, 'max' : max, 'submit_button': button}
    rv = web.post(resource_name, follow_redirects=True, data=data)

    expected = b"Once upon a time, there was a dog called Tutu. (# words: 10)"
    assert_in(expected, rv.data)
    expected = b"If you met him, you would like him too. (# words: 9)"
    assert_in(expected, rv.data)


def test_results():
    # Test cases

    # Valid input - Normal merge
    button = 'Merge'
    input_text = "Once upon a time, there was a dog called Tutu. He was nice. If you met him, you would like him too."
    max = 7
    index = 1
    sentences = LeGuinnCounter(input_text).sentences
    data = {"input_text" : input_text, 'max' : max, 'index': index, 'sent_list[]': sentences, 'submit_button': button}
    expected = b"He was nice. If you met him, you would like him too. (# words: 12)"
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(expected, rv.data)

    # Valid input except bad index - out of bounds
    data['index'] = 3
    expected = b"IndexError"
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(expected, rv.data)
    data['index'] = -4
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(expected, rv.data)

    # Merge with no sentences
    input_text = ''
    index = 0
    sentences = LeGuinnCounter(input_text).sentences
    data = {"input_text" : input_text, 'max' : max, 'index': index, 'sent_list[]': sentences, 'submit_button': button}
    expected = b"Merge cannot be performed on an empty sentence list."
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(expected, rv.data)

    # Try mergeing when there is only one sentence
    input_text = "Once upon a time, there was a dog called Tutu."
    max = 7
    index = 0
    sentences = LeGuinnCounter(input_text).sentences
    data = {"input_text" : input_text, 'max' : max, 'index': index, 'sent_list[]': sentences, 'submit_button': button}
    expected = b"Once upon a time, there was a dog called Tutu. (# words: 10)"

    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(expected, rv.data)


    # Merging with None-types

    #Initial state
    def setup():
        input_text = "Once upon a time, there was a dog called Tutu. He was nice. If you met him, you would like him too."
        max = 7; index = 0; sentences = LeGuinnCounter(input_text).sentences
        return {
                "input_text" : input_text,
                'max' : max,
                'index': index,
                'sent_list[]': sentences,
                'submit_button': button
                }

    # Max = None
    data = setup()
    data['max'] = None
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Bad Request', rv.data)

    # index is None
    data = setup()
    data['index'] = None
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Bad Request', rv.data)

    # sent_list -- This should not happen!
    data = setup()
    data['sent_list[]'] = None
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Merge cannot be performed on an empty sentence list.', rv.data)

    # submit_button is None
    data = setup()
    data['submit_button'] = None
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Bad Request', rv.data)

    # input_text is None
    data = setup()
    data['input_text'] = None
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Bad Request', rv.data)

    # BAD DATA

    # Index passed non-integer type
    data = setup()
    data['index'] = 'r'
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'ValueError', rv.data)

    # Max - negative value
    data = setup()
    data['max'] = -5
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'ValueError', rv.data)
    # Max - letter
    data['max'] = 'go'
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'ValueError', rv.data)

    # submit_button - bad name
    data = setup()
    data['submit_button'] = "CRAZYTOWN!!"
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'submit_button neither Count, Merge nor Split!', rv.data)

    # sent_list doesn't match original text
    data = setup()
    data['sent_list[]'] = ['A.', ' B.' , ' C.']
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'NotInTextError', rv.data)

    # input_text doesn't match sent_list
    data = setup()
    data['input_text'] = "A. B. C."
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'NotInTextError', rv.data)


    # Merging with last sentence
    # NB This may fail in future as users shouldn't have the option of merging
    # with the last sentence in the text
    data = setup()
    data['index'] = len(data['sent_list[]']) - 1
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'If you met him, you would like him too.', rv.data)

    # See whether word counts for original and parsed texts work
    button = 'Count'

    data = setup()
    data['input_text'] = data['input_text'][:-1] # take away period at end
    data['sent_list[]'] = LeGuinnCounter(data['input_text']).sentences
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'13 words', rv.data)

    data = setup()
    data['input_text'] = ""# take away period at end
    data['sent_list[]'] = LeGuinnCounter(data['input_text']).sentences
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Nothing to process', rv.data)




def test_wordchar_max():

    from app import _is_over
    from app import WORD_MAX, CHAR_MAX

    # Test number of words
    # Over
    n = WORD_MAX + 1
    text = 'Giovanni ' * n
    print(len(text))
    expected = True
    assert_equal(_is_over(text, WORD_MAX, CHAR_MAX), expected)

    # Under
    n = WORD_MAX - 1
    text = 'Giovanni ' * n
    expected = False
    assert_equal(_is_over(text, WORD_MAX, CHAR_MAX), expected)

    # Equal
    n = WORD_MAX
    text = 'Giovanni ' * n
    expected = False
    assert_equal(_is_over(text, WORD_MAX, CHAR_MAX), expected)

    # Test number of characters
    # over
    n = CHAR_MAX + 1
    text = 'P' * n
    expected = True
    assert_equal(_is_over(text, WORD_MAX, CHAR_MAX), expected)

    # Under
    n = CHAR_MAX - 1
    text = 'P' * n
    expected = False
    assert_equal(_is_over(text, WORD_MAX, CHAR_MAX), expected)

    # Equal
    n = CHAR_MAX
    text = 'P' * n
    expected = False
    assert_equal(_is_over(text, WORD_MAX, CHAR_MAX), expected)






# DISABLED TEMPORARILY SO TESTS CAN RUN FASTER
# def test_longtext():
#     # Very, very large input
#     fin = open("./tests/metamorphosis_kafka.txt")
#     button = 'Count'
#     input_text = fin.read()
#     max = '25'
#     data = {"input_text" : input_text, 'max' : max, 'submit_button' : button}
#     rv = web.post(resource_name, follow_redirects=True, data=data)
#     assert_in(b'Highlighted Text', rv.data)
