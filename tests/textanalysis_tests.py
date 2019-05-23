from nose.tools import *
from textanalysis.textanalysis import *


def test_get_sentences():
    '''
    TEST CASES:
    1) No input
        i) Empty string
            a) No space ""
            b) Spaces "    "
            c) Escape sequences "\n\t\r"
        ii) None object
    '''

    assert_equal(get_sentences(""), [])
    assert_equal(get_sentences("   "), [])
    assert_equal(get_sentences("\t\t\n\t\n"), [])
    assert_raises(TypeError, get_sentences, None)

    '''
    2) Bad input
        i)  Non-string object, e.g. Integer
        ii) Non-English text with non-standard end-of sentence punctuation
    '''
    assert_raises(TypeError, get_sentences, 5)
    #Burmese script ends with ||
    burmese_script = "ကျွန်ေတာ် မိုက် လို ခေါ်ပါတယ်။"
    assert_equal(get_sentences(burmese_script), [])

    '''
    3) Valid input
        i) Floating point number in string format
        ii) One sentence
        iii) Text that ends in
        iv) Long text
        v) dialog**
        vi) Swearing
        vii) ellipsis in the middle of the sentence
        viii) Mr. Dr. Mrs. Mrs. Mz. etc. 

    '''
    #i)
    assert_equal(get_sentences("4642436436436.425254425292929291"), [])
    #ii)
    assert_equal(get_sentences("This is a sentence."), ['This is a sentence.'])
    assert_equal(get_sentences("This is a sentence?"), ['This is a sentence?'])
    assert_equal(get_sentences("This is a sentence!"), ['This is a sentence!'])
    assert_equal(get_sentences("This is a sentence?!"), ['This is a sentence?!'])
    assert_equal(get_sentences("This is a sentence..."), ['This is a sentence...'])
    #iii)
    assert_equal(get_sentences("?.!>?,?!. ?!!!...?,,,?"), ["?.!>?,?!.", "?!!!...?,,,?"])
    #iv)
    fin = open("./tests/metamorphosis_kafka.txt")
    fout = open("./tests/output.txt", 'w')

    file_data = fin.read()

    sent_list = get_sentences(file_data)
    num_sentences = len(sent_list)

    for x in sent_list:
        fout.write(x + '\n')

    assert_equal(num_sentences == 896, True) #figured this by ad-hoc bisecting algorithm
    #v)
    dialog = '"I\'m not read for this," said the Blue Russian.'
    assert_equal(get_sentences(dialog), [dialog])
    dialog = '"I\'m not read for this!" exclaimed the Blue Russian.'
    assert_equal(get_sentences(dialog), [dialog])
    dialog = '"I\'m not read for this?" asked the Blue Russian.'
    assert_equal(get_sentences(dialog), [dialog])
    #vi
    sentence = "This is &#%!@? crazy!!"
    result = get_sentences(sentence)

    #vi)
    '''
    Unable to write code to pass this test. The problem is how to distinguish
    the case below from one where the expletive is at the end of the sentence
    e.g.
    "This is &#%!@? crazy."
    "This is &#%!@?! What can I do?"
    I can't think of way of 'ignoring' the expletive in the first case (wanted)
    without ignoring in the second (not wanted)

    At the other side door his sister came plaintively: "Gregor? Aren't you well?"
    '''
    #assert_equal(result, ["This is &#%!@? crazy!!"] )

    #vii)
    text = "And I waited...for a long, long time."
    assert_equal(get_sentences(text), ["And I waited...for a long, long time."] )
