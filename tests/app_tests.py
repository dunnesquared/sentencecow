from nose.tools import *
from app import *

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

def test_first_parse():
    # TEST CASES
    # No input
    # Whitespace input
    # Non-valid sentence input
    # Very, very large input
    # Very, very, large max
    # Negative max
    # Non-integer max

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

    # Very, very large input
    fin = open("./tests/metamorphosis_kafka.txt")
    input_text = fin.read()
    max = '25'
    data = {"input_text" : input_text, 'max' : max}
    rv = web.post(resource_name, follow_redirects=True, data=data)
    assert_in(b'Highlighted Text', rv.data)
