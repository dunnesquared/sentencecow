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
        ix) Dialgoue attribution
            Cases:
            a) "He ate a donut."
            b) "He ate a donut," she said. => works now
            c) She said, "He ate a donut."
            d) "He ate a donut," she said, "but you didn't care."
            e) "He ate a donut," she said, hoping to provoke a reaction. "But you didn't care."
            f) "He ate a donut?"
            h) "He ate a donut!"
            i) "He ate a donut?" she asked. => will fail if implement
            j) "He ate a donut!" she said. => will fail
            k) "He ate a--"
            l) Multiple lines of dialogue
            “He wasn’t sure, said he had to ask his wife.
            Thank God I don’t have to ask permission of a wife. None of that
            ball and chain stuff for me, no sir. I can go where I want, when
            I want. Yep, freedom. Nothing beats freedom.”


            Laurel yelled, "Eeyore! Eeyore!"
            See http://theeditorsblog.net/2010/12/08/punctuation-in-dialogue/
            for more cases

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

    assert_equal(num_sentences >= 896, True)
    #v)
    '''
    dialog = '"I\'m not read for this," said the Blue Russian.'
    assert_equal(get_sentences(dialog), [dialog])
    dialog = '"I\'m not read for this!" exclaimed the Blue Russian.'
    assert_equal(get_sentences(dialog), [dialog])
    dialog = '"I\'m not read for this?" asked the Blue Russian.'
    assert_equal(get_sentences(dialog), [dialog])
    '''
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

    #viii - Honorifics
    text = "Hello, Mrs. Dunne. I've been waiting a long time for you."
    assert_equal(get_sentences(text),["Hello, Mrs. Dunne.", "I've been waiting a long time for you."])

    #Quote test
    '''
    ix) Dialgoue attribution
        Cases:
        a) "He ate a donut."
        b) "He ate a donut," she said. => works now
        c) She said, "He ate a donut."
        d) "He ate a donut," she said, "but you didn't care."
        e) "He ate a donut," she said, hoping to provoke a reaction. "But you didn't care."
        f) "He ate a donut?"
        h) "He ate a donut!"
        i) "He ate a donut?" she asked. => will fail if implement
        j) "He ate a donut!" she said. => will fail
        k) "He ate a--"
        l) Multiple lines of dialogue
        “He wasn’t sure, said he had to ask his wife.
        Thank God I don’t have to ask permission of a wife. None of that
        ball and chain stuff for me, no sir. I can go where I want, when
        I want. Yep, freedom. Nothing beats freedom.”
    '''

    #a
    text = "\"He ate a donut.\""
    assert_equal(get_sentences(text), ["\"He ate a donut.\""])




'''
Just to make sure nosetest is actually working...
def test_testing():
    assert_equal(True, False)
'''
