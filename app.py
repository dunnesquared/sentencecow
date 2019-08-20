"""APP.PY

To Do:

    * use different separator ("||")
    * clean up code
    * document
    * bug - when trying to merge blank text
    * handle exceptions from model modules/classes
    * need to send sentences when sending over whole lg object
    * results.html: clean up code
    * redesign LeGuinnCounter class to better handle merging (class-leve methods)
    * the indent in first paragraph screwing up the highlighting

Done:
    * show word count for every sentence
    * add max to value returned by merge_list

"""

from flask import Flask
from flask import render_template
from flask import request

from leguinncounter import LeGuinnCounter
from textanalysis import textanalysis as ta

import traceback as tb

app = Flask(__name__)

# Server-side restriction on word-count in case client-side script disabled
WORD_MAX = 300
CHAR_MAX = WORD_MAX * 20


def _is_over(text, word_max, char_max):
    '''Return whether 'text' contains more words or character
       than given max allowed.

    Args:
        text (str): String in which words are to be counted
        max (int): Maximum number of words allowed from user input

    Return
        True: number of words in text is greater than WORD_MAX
        False: number of words in text is NOT greater than WORD_MAX
    '''
    word_over = True if len(ta.get_words(text)) > word_max else False
    char_over = True if len(text) > char_max else False

    print(len(ta.get_words(text)))
    print(True if len(ta.get_words(text)) > word_max else False)
    print(f"word over = {word_over}\nchar_over = {char_over}")
    return word_over or char_over

    # return True if len(ta.get_words(text)) > WORD_MAX else False


@app.errorhandler(400)
def bad_request(error):
    '''Return web page with description and stack trace of Bad Request Error.'''
    err = str(error) + "\n(Input possibly passed NoneType object)"
    stack_trace = tb.format_exc()
    return render_template("error.html", err=err, stack_trace=stack_trace)


@app.route("/leguinncounter", methods=['POST', 'GET'])
def index():
    '''Return web pages that allow users to see whether their texts satisfy
       the criterion that their sentences have fewer or the same user-set
       number of words.
      '''

    try:
        if request.method == 'GET':
            # Render main page of web app
            return render_template("form.html", max=WORD_MAX, char_max=CHAR_MAX)

        elif request.method == 'POST':

            # User requests to merge a sentence with the one following it.
            if request.form['submit_button'] == 'Merge':

                #Get everything we'll need to merge sentences and send data back
                input_text = request.form['input_text']
                max = request.form['max']
                sent_list = request.form.getlist('sent_list[]')
                index = request.form['index']

                # LeGuinnCounter expects integers, not strings for these values
                try:
                    max = int(max)
                except ValueError as e:
                    err = "Max can only be an integer"
                    stack_trace = tb.format_exc()
                    return render_template("error.html", err=err,
                                            stack_trace=stack_trace)

                index = int(index)

                # Trailing white spaces are suprefluous
                input_text = input_text.rstrip()

                # Initialize domain object
                lg = LeGuinnCounter(input_text)

                # We can't use sentence list generated when we create a LeGuinn-
                # Counter object: regardless, how many times we merge sentences
                # that parsing will always be the same (and so undo the parsing).
                # Thus, it's important we use the sentences from our last merge.
                # and replace the sentences in our object with them. Not the best
                # design; will fix in later iteration
                lg.sentences = sent_list

                # Merge sentence at current index with the one following it
                lg.merge_next(index)

                # Get list of LG_sentences so we can do highlighing more easily
                lg_sentlist = lg.generate_LGSentenceList(input_text, lg.sentences, max)

                # Create a tuples list that you can send to the template; also
                # want to decouple the domain stuff from the controller/ui stuff
                highlight_data = [ (l.start, l.end, l.isOver, l.whitespace) for l in lg_sentlist]

                # So we can send back sentence list to user
                # sentences = lg.sentences
                sentences = [{'content': s, 'wordcount': lg.count_words(s)} for s in lg.sentences]

            # First parsing of text!
            elif request.form['submit_button'] == 'Count':
                # Get everything we'll need to get the sentences from a text
                # Check that word_max has been respected
                input_text = request.form['input_text']

                if _is_over(input_text, WORD_MAX, CHAR_MAX):
                    msg = f'''Text exceeds {WORD_MAX} words or
                             {CHAR_MAX} characters:
                             {len(ta.get_words(input_text))} words;
                             {len(input_text)} characters.'''

                    return render_template("form.html", msg=msg,
                                            input_text=input_text,
                                            max=WORD_MAX,
                                            is_over=True)

                # LeGuinnCounter expects integers, not strings for these values
                try:
                    max = int(request.form['max'])
                except ValueError as e:
                    err = "Bad input: 'max' can only be a positive whole number."
                    stack_trace = tb.format_exc()
                    return render_template("error.html", err=err,
                                            stack_trace=stack_trace)

                # Trailing white spaces are suprefluous
                input_text = input_text.rstrip()

                # Initialize domain object
                lg = LeGuinnCounter(input_text)

                # Get list of LG_sentences so we can do highlighing more easily
                lg_sentlist = lg.generate_LGSentenceList(input_text, lg.sentences, max)

                # Create a tuples list that you can send to the template; also
                # want to decouple the domain stuff from the controller/ui stuff
                highlight_data = [ (l.start, l.end, l.isOver, l.whitespace) for l in lg_sentlist]

                # So we can send back sentence list to user
                # sentences = lg.sentences
                sentences = [{'content': s, 'wordcount': lg.count_words(s)} for s in lg.sentences]

                # So we can have the word counts of each sentence without
                # having to call wordcount function in template

            else:
                err = "submit_button neither Count nor Merge!"
                stack_trace = "Not an exception!"
                return render_template("error.html", err=err, stack_trace=stack_trace)

            # Get list of sentences that have more words than max
            long_sentences = lg.sentences_more_than(max)

            return render_template("results.html", lgcounter=lg,
                                    input_text=input_text, sentences = sentences,
                                    long_sentences = long_sentences, max = max,
                                    highlight_data = highlight_data)

        else:
            #server will return a 405 error code if other methods specified
            #Note that head request will work as it only returns blank data
            #Head request exectutes this conditional, even though the error
            #page is technically not returned (weird?)
            err = "Not a GET or POST request; HEAD request likely made: " + request.method
            return render_template("error.html", err=err)

    except (ta.NotInTextError, ValueError, TypeError, IndexError, MemoryError) as e:
        err = str(e)
        stack_trace = tb.format_exc()
        return render_template("error.html", err=err, stack_trace=stack_trace)


if __name__ == "__main__":
    app.run()
