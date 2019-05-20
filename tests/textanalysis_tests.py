from nose.tools import *
from textanalysis.textanalysis import *


def test_get_sentences():
    '''
    TEST CASES:

    1) No input
        i) Empty string
            a) No space ""
            b) Spaces "    "
        ii) None object
    '''

    assert_equal(get_sentences(""), [])
    assert_equal(get_sentences("   "), [])
    assert_raises(AttributeError, get_sentences, None)

    '''
    TEST CASES:

    2) Bad input
        i) Non-string object, e.g. Integer
        ii) Non-English text with non-standard end-of sentence punctuation
    '''

    assert_raises(AttributeError, get_sentences, 5)

    #Burmese script ends with ||
    burmese_script = "ကျွန်ေတာ် မိုက် လို ခေါ်ပါတယ်။"
    assert_equal(get_sentences(burmese_script), [])
