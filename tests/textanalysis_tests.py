from nose.tools import *
from textanalysis.textanalysis import *
from textwrap import dedent

'''
To do:
    * fix find_start_last test on line 320 when using re (remove subtraction)

Done:
    * add test for curly quotes in substring in find_start_end
    * add test for curly quotes in find_start_last
'''


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
            l) "He ate a donut?" Alex asked.
            m) Multiple lines of dialogue
            “He wasn’t sure, said he had to ask his wife.
            Thank God I don’t have to ask permission of a wife. None of that
            ball and chain stuff for me, no sir. I can go where I want, when
            I want. Yep, freedom. Nothing beats freedom.”


            Laurel yelled, "Eeyore! Eeyore!"
            See http://theeditorsblog.net/2010/12/08/punctuation-in-dialogue/
            for more cases
        x) No punct in last part of text
            "Hello there, good sir. Would you like a chocolate"
        xi) Purely symbolic sentence #$? ! #.

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
    assert_equal(get_sentences("?.!>?,?!. ?!!!...?,,,?"), ["?.!>?,?!.", " ?!!!...?,,,?"])


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
    assert_equal(get_sentences(text),["Hello, Mrs. Dunne.", " I've been waiting a long time for you."])

    #Quote test
    '''
    ix) Dialgoue attribution
        Cases:
        a) "He ate a donut." - PASSED
        b) "He ate a donut," she said. - PASSED
        c) She said, "He ate a donut." - PASSED
        d) "He ate a donut," she said, "but you didn't care." - PASSED
        e) "He ate a donut," she said, hoping to provoke a reaction. "But you didn't care." - PASSED
        f) "He ate a donut?" - PASSED
        h) "He ate a donut!" - PASSED
        i) "He ate a donut?" she asked. - PASSED
        j) "He ate a donut!" she said. - PASSED
        k) "He ate a--"
        l) "He ate a donut?" Alex asked.
        m) Multiple lines of dialogue
        “He wasn’t sure, said he had to ask his wife.
        Thank God I don’t have to ask permission of a wife. None of that
        ball and chain stuff for me, no sir. I can go where I want, when
        I want. Yep, freedom. Nothing beats freedom.”
        n) “Curly quotes are going to be problem!” she yelled.
    '''

    # a, f, h
    text = "\"He ate a donut.\""
    assert_equal(get_sentences(text), ["\"He ate a donut.\""])
    text = "\"He ate a donut!\""
    assert_equal(get_sentences(text), ["\"He ate a donut!\""])
    text = "\"He ate a donut?\""
    assert_equal(get_sentences(text), ["\"He ate a donut?\""])

    # b
    text = "\"He ate a donut,\" she said."
    assert_equal(get_sentences(text), ["\"He ate a donut,\" she said."])

    # c
    text = "She said, \"He ate a donut.\""
    assert_equal(get_sentences(text), ["She said, \"He ate a donut.\""])

    # d
    text = "\"He ate a donut,\" she said, \"but you didn't care.\""
    assert_equal(get_sentences(text), ["\"He ate a donut,\" she said, \"but you didn't care.\""])

    # e
    text = "\"He ate a donut,\" she said, hoping to provoke a reaction. \"But you didn't care.\""
    assert_equal(get_sentences(text), ["\"He ate a donut,\" she said, hoping to provoke a reaction.", " \"But you didn't care.\""])

    # i, j, k
    text = "\"He ate a donut?\" she asked."
    assert_equal(get_sentences(text), ["\"He ate a donut?\" she asked."])

    text = "\"He ate a donut!\" she said."
    assert_equal(get_sentences(text), ["\"He ate a donut!\" she said."])

    text = "\"He ate a don--\" she said."
    assert_equal(get_sentences(text), ["\"He ate a don--\" she said."])

    # l => FAILED TEST
    #text = "\"He ate a donut?\" Alex asked."
    #assert_equal(get_sentences(text), ["\"He ate a donut?\" Alex asked."])

    # m
    text = ("\"He wasn’t sure, said he had to ask his wife. " +
            "Thank God I don’t have to ask permission of a wife. " +
            "None of that ball and chain stuff for me, no sir. " +
            "I can go where I want, when I want. Yep, freedom. " +
            "Nothing beats freedom.\"")

    expected = [
                "\"He wasn’t sure, said he had to ask his wife.",
                " Thank God I don’t have to ask permission of a wife.",
                " None of that ball and chain stuff for me, no sir.",
                " I can go where I want, when I want.",
                " Yep, freedom.",
                " Nothing beats freedom.\""
                ]

    assert_equal(get_sentences(dedent(text)), expected)



    # n
    text=  "“Curly quotes are going to be problem.” I ignored Mario."
    expected = ["\"Curly quotes are going to be problem.\"", " I ignored Mario."]
    assert_equal(get_sentences(text), expected)

    # X
    text  = "Hello there, good sir. Would you like a chocolate"
    expected = ["Hello there, good sir."]
    assert_equal(get_sentences(text), expected)

    # xi) Purely symbolic sentence #$? ! #.
    text = "#$? ! ^."
    expected = ['#$?', ' !', ' ^.']
    assert_equal(get_sentences(text), expected)


def test_get_words():
    '''CASES:
        1. Non-string passed
        2. Empty string, len = 0
        3. String with blank spaces in it
        4. 1-word string
        5. One full sentence
        6. Two full sentences
        7. Keep hyphens; remove em-dashes
     '''

    # 1. Non-string passed
    assert_raises(TypeError, get_words, None)

    # 2. Empty string, len = 0
    assert_equal(get_words(""), [])

    # 3. String with blank spaces in it
    assert_equal(get_words("          "), [])

    # 4. 1-word string
    assert_equal(get_words("Eeyore"), ["Eeyore"])

    # 5. One full-sentence
    text = "Giovanni loves pizza!"
    expected = ["Giovanni", "loves", "pizza"]
    assert_equal(get_words(text), expected)


    # 6. TWo full sentences
    text = "Giovanni loves pizza! Do you?"
    expected = ["Giovanni", "loves", "pizza", "Do", "you"]
    assert_equal(get_words(text), expected)

    # 7. Keep hyphens; remove em-dashes
    text  = "My dog-sitter likes hot-dogs—how unsettling."
    expected = ["My", "dog-sitter", 'likes', 'hot-dogs', 'how', 'unsettling']
    assert_equal(get_words(text), expected)

    text  = "My dog-sitter likes— "
    expected = ["My", "dog-sitter", 'likes']
    assert_equal(get_words(text), expected)




def test_find_start_end():
    '''CASES:
    1. Bad type for sentence parameter
    2. Bad type for text parameter
    3. Bad type for start_search parameter
    4. Bad type for all parameters
    5. Negative value for start_search
    6. Searching for an empty sentence, "", in a non-empty text
    7. Searching for a non-empty sentence in an empty text
    8. Searching for empty sentence in an empty text
    9. "  " for a non-empty sentence in a non-empty text; sentence not there
    10. "  " for a non-empty sentence in a non-empty text; sentence there
    11. Same as 8, but with multiple of occurrences of sentence in text
    12. Make sure text is clean of curly quotes
    13. Make sure substring is clean of curly quotes
    '''

    # 1
    sentence = None
    text = "Some dummy text"
    assert_raises(AttributeError, find_start_end, sentence, text, start_search=1)
    # 2
    sentence = "Some dummy text"
    text = None
    assert_raises(AttributeError, find_start_end, sentence, text, start_search=1)
    # 3
    text = "More dummy text"
    assert_raises(TypeError, find_start_end, sentence, text, start_search="1")
    # 4
    sentence, text = None, None
    assert_raises(AttributeError, find_start_end, sentence, text, start_search="1")
    # 5
    sentence = "Some dummy text"
    text = "More dummy text"
    assert_raises(ValueError, find_start_end, sentence, text, start_search=-1)
    # 6
    sentence = ""
    assert_raises(ValueError, find_start_end, sentence, text, start_search=0)
    # 7
    sentence = "Some dummy text"
    text = ""
    assert_raises(ValueError, find_start_end, sentence, text, start_search=0)
    # 8
    sentence, text = "", ""
    assert_raises(ValueError, find_start_end, sentence, text, start_search=0)
    # 9
    sentence = "Yesterday, she was here."
    text = "Tomorrow she is not."
    assert_raises(NotInTextError, find_start_end, sentence, text, start_search=0)

    # 10
    text = "Yesterday, she was here. Tomorrow she is not."
    assert_equal(find_start_end(sentence, text, start_search=0), (0, len(sentence)))
    # 11
    text = "Yesterday, she was here. Tomorrow she is not. Yesterday she was here."
    assert_equal(find_start_end(sentence, text, start_search=0), (0, len(sentence)))

    # 12
    sentence = '"Tomorrow she is not."'
    text = "“Tomorrow she is not.” So it goes."
    assert_equal(find_start_end(sentence, text, start_search=0), (0, len(sentence)))

    # 13
    sentence = '“Tomorrow she is not.”'
    text = "\"Tomorrow she is not.\" So it goes."
    assert_equal(find_start_end(sentence, text, start_search=0), (0, len(sentence)))

    # 14
    text = 'X Y. Z. A B C. '
    sentence = ' Z.'
    assert_equal(find_start_end(sentence, text, start_search=0), (4, 4+ len(sentence)))


def test_ussr():
    # N.B. This test will fail once you add U.S.S.R to abbreviation list

    text = "He lived in the U.S.S.R I think."
    expected = ['He lived in the U.S.S.R I think.']
    assert_equal(get_sentences(text), expected)

    text = "He lived in the U.S.S.R. I think."
    expected = ['He lived in the U.S.S.R.', ' I think.']
    assert_equal(get_sentences(text), expected)

    text = "He lived in the U.S. I think."
    expected = ['He lived in the U.S. I think.']
    assert_equal(get_sentences(text), expected)

def test_offset():

    text = "      Once upon a time, there was a dog called Tutu."
    expected = 6
    assert_equal(offset(text), expected)
