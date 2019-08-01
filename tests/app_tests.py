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
    # Very, very large input
    # Input_text passed None
    # Max passed None
    # Very, very, large max
    # Negative max
    # Non-integer max
    # Valid, working input

    # No input
    data = {"input_text" : "", 'max' : '4'}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Nothing to process!', rv.data)

    # No input
    input_text = "\n\t\r     \n\n\n\n\t   \t\t\r\r\r\n"
    max = '4'
    data = {"input_text" : input_text, 'max' : max}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Nothing to process!', rv.data)

    # Non-valid sentence input
    input_text = "This is not a sentence Neither is this Why No punctuation"
    max = '4'
    data = {"input_text" : input_text, 'max' : max}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Nothing to process!', rv.data)

    ''' DISABLED TEMPORARILY SO TESTS CAN RUN FASTER
    # Very, very large input
    fin = open("./tests/metamorphosis_kafka.txt")
    input_text = fin.read()
    max = '25'
    data = {"input_text" : input_text, 'max' : max}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Highlighted Text', rv.data)
    '''

    # Input_text passed None
    input_text = None
    data = {"input_text" : input_text, 'max' : max}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Bad Request', rv.data)

    # Very large max
    input_text = "Once upon a time, there was named Tutu. He was nice."
    max = '9999999999'
    data = {"input_text" : input_text, 'max' : max}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Highlighted Text', rv.data)

    # Negative max
    max = '-5'
    data = {"input_text" : input_text, 'max' : max}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Max must be a number &gt;= 1.', rv.data)
    #assert_raises(ValueError, web.post, resource_name, follow_redirects=True, data=data)

    # Non-integer max
    max = "Are you having fun yet?!"
    data = {"input_text" : input_text, 'max' : max}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b"Bad input: &#39;max&#39; can only be a positive whole number.", rv.data)

    max = None
    data = {"input_text" : input_text, 'max' : max}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Bad Request', rv.data)

    # Valid, working input
    input_text = "Once upon a time, there was a dog called Tutu. He was nice. If you met him, you would like him too."
    max = 7
    data = {"input_text" : input_text, 'max' : max}
    rv = web.post(resource_name, follow_redirects=True, data=data)

    expected = b"Once upon a time, there was a dog called Tutu. (# words: 10)"
    assert_in(expected, rv.data)
    expected = b"If you met him, you would like him too. (# words: 9)"
    assert_in(expected, rv.data)




def test_results():
    # Test cases
    # Valid input
    pass
