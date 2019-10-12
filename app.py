"""APP.PY

To Do:

    * use different separator ("||")
    * clean up code
    * document
    * bug - when trying to merge blank text
    * handle exceptions from model modules/classes
    * need to send sentences when sending over whole lg object
    * results.html: clean up code
    * redesign LeGuinCounter class to better handle merging (class-leve methods)
    * the indent in first paragraph screwing up the highlighting

Done:
    * show word count for every sentence
    * add max to value returned by merge_list

"""

from flask import Flask, make_response
from flask import render_template
from flask import request

from leguincounter import LeGuinCounter
from textanalysis import textanalysis as ta

import traceback as tb

app = Flask(__name__)

# Server-side restriction on word-count in case client-side script disabled
# Set WORD_MAX to 26000 if running test on metamorphis_kafka.txt
WORD_MAX = 300
CHAR_MAX = WORD_MAX * 10


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

    return word_over or char_over

    # return True if len(ta.get_words(text)) > WORD_MAX else False


@app.errorhandler(400)
def bad_request(error):
    '''Return web page with description and stack trace of Bad Request Error.'''
    err = str(error) + "\n(Input possibly passed NoneType object)"
    stack_trace = tb.format_exc()

    response = make_response(render_template("error.html",
                                             err = err,
                                            stack_trace = stack_trace))
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


@app.route("/leguincounter", methods=['POST', 'GET'])
def index():
    '''Return web pages that allow users to see whether their texts satisfy
       the criterion that their sentences have fewer or the same user-set
       number of words.
      '''

    try:
        if request.method == 'GET':
            # Need a response object to add meta security policy tag in the
            # header of the returned page
            response = make_response(render_template("form.html",
                                                      max=WORD_MAX,
                                                      char_max=CHAR_MAX))
            # Set security policy to minimize chances of XSS attack
            # Policy: only trust resources (scripts, stylsheets etc) from
            # this site (default-src)
            response.headers['Content-Security-Policy'] = "default-src 'self'"
            return response


        elif request.method == 'POST':

            # User requests to merge a sentence with the one following it.
            if request.form['submit_button'] == 'Merge':

                #Get everything we'll need to merge sentences and send data back
                input_text = request.form['input_text']
                max = request.form['max']
                sent_list = request.form.getlist('sent_list[]')
                index = request.form['index']

                # LeGuinCounter expects integers, not strings for these values
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
                lg = LeGuinCounter(input_text)

                # We can't use sentence list generated when we create a LeGuin-
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
                highlight_data = [ (l.start, l.end, l.is_over, l.whitespace) for l in lg_sentlist]

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

                # LeGuinCounter expects integers, not strings for these values
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
                lg = LeGuinCounter(input_text)

                # Get list of LG_sentences so we can do highlighing more easily
                lg_sentlist = lg.generate_LGSentenceList(input_text, lg.sentences, max)

                # Create a tuples list that you can send to the template; also
                # want to decouple the domain stuff from the controller/ui stuff
                highlight_data = [ (l.start, l.end, l.is_over, l.whitespace) for l in lg_sentlist]

                # So we can send back sentence list to user
                # sentences = lg.sentences
                sentences = [{'content': s, 'wordcount': lg.count_words(s)} for s in lg.sentences]

                # So we can have the word counts of each sentence without
                # having to call wordcount function in template

            elif request.form['submit_button'] == 'Split':
                # Data pertaining to split the sentence
                # split_pos = request.form['splitposition']
                index = request.form['sentindex']
                first_part = request.form['firstpart']
                #second_part = request.form['secondpart']

                # DEBUG
                # print("SPLIT POS = ", split_pos)
                print("SENT INDEX = ", index)
                print("FIRST PART = ", first_part)
                #print("SECOND PART = ", second_part)


                # The rest
                #Get everything we'll need to merge sentences and send data back
                input_text = request.form['input_text']
                max = request.form['max']
                sent_list = request.form.getlist('sent_list[]')

                # LeGuinCounter expects integers, not strings for these values
                try:
                    max = int(max)
                except ValueError as e:
                    err = "Max can only be an integer"
                    stack_trace = tb.format_exc()
                    return render_template("error.html", err=err,
                                            stack_trace=stack_trace)

                index = int(index)
                # split_pos = int(split_pos)

                # Trailing white spaces are suprefluous
                input_text = input_text.rstrip()

                # Initialize domain object
                lg = LeGuinCounter(input_text)

                # We can't use sentence list generated when we create a LeGuin-
                # Counter object: regardless, how many times we merge sentences
                # that parsing will always be the same (and so undo the parsing).
                # Thus, it's important we use the sentences from our last merge.
                # and replace the sentences in our object with them. Not the best
                # design; will fix in later iteration
                lg.sentences = sent_list

                # Merge sentence at current index with the one following it
                #lg.split_sentence(index, split_pos)
                lg.split_sentence(index, first_part)

                # Get list of LG_sentences so we can do highlighing more easily
                lg_sentlist = lg.generate_LGSentenceList(input_text, lg.sentences, max)

                # Create a tuples list that you can send to the template; also
                # want to decouple the domain stuff from the controller/ui stuff
                highlight_data = [ (l.start, l.end, l.is_over, l.whitespace) for l in lg_sentlist]

                # So we can send back sentence list to user
                # sentences = lg.sentences
                sentences = [{'content': s, 'wordcount': lg.count_words(s)} for s in lg.sentences]



            else:
                err = "submit_button neither Count, Merge nor Split!"
                stack_trace = "Not an exception!"

                # Add security policy
                response = make_response(render_template("error.html",
                                                        err=err,
                                                        stack_trace=stack_trace))
                response.headers['Content-Security-Policy'] = "default-src 'self'"
                return response

                # return render_template("error.html", err=err, stack_trace=stack_trace)


            # Get number of words in original and parsed texts
            # If they're not equal, then it's likely the last part of the
            # original text got lobbed off because it was missing a terminating
            # punctuation mark.
            wordcounts = {
                          'original': len(ta.get_words(input_text)),
                          'parsed': sum(sentence['wordcount'] for sentence in sentences)
                         }

            # Add security policy
            response = make_response(render_template("results.html",
                                        input_text=input_text,
                                        sentences = sentences,
                                        max = max,
                                        highlight_data = highlight_data,
                                        wordcounts = wordcounts))

            response.headers['Content-Security-Policy'] = "default-src 'self'"
            return response

        else:
            #server will return a 405 error code if other methods specified
            #Note that head request will work as it only returns blank data
            #Head request exectutes this conditional, even though the error
            #page is technically not returned (weird?)
            err = "Not a GET or POST request; HEAD request likely made: " + request.method
            response = make_response(render_template("error.html", err=err))
            response.headers['Content-Security-Policy'] = "default-src 'self'"
            return response


    except (ta.NotInTextError, ValueError, TypeError, IndexError, MemoryError) as e:
        err = str(e)
        stack_trace = tb.format_exc()

        response = make_response(render_template("error.html",
                                                  err=err,
                                                  stack_trace = stack_trace))
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response


if __name__ == "__main__":
    app.run()
