# -*- coding: utf-8 -*-
"""Flask script that handles requests to parse sentences in a text and more.

The following CGI script is the main server-side component that handles
user requests to extract, analyze and modify sentences in a text.

This script facilitates interaction between the domain and the UI
layers. The domain layer consists of the leguincounter and textanalysis
modules; Jinja2 HTML templates and JavaScript handlers make up the UI layer.

Domain-level objects are not passed to the UI templates to lower coupling
between the two. Any needed data from the former are converted into standard
Python objects such as lists, maps and tuples.

Sessions are not used in this script to maintain state. Instead, for operations
such as merging and splitting text, all initla data is re-POSTed along with any
changes that need to be processed.
"""

import traceback as tb
from flask import Flask, make_response
from flask import render_template
from flask import request
from leguincounter import LeGuinCounter
import textanalysis as ta

app = Flask(__name__)

# Server-side restriction on word-count in case client-side script disabled
# Set WORD_MAX to 26000 if running test on metamorphis_kafka.txt
WORD_MAX = 300
CHAR_MAX = WORD_MAX * 10


def _is_over(text, word_max, char_max):
    """Checks whether 'text' contains more words or characters than given
    max allowed.

    N.B. It may seem useless to pass maximums as arguments rather than directly
    access them via the globals above. The reason for it was to make
    testing of _is_over easier: changing the global maximums from the
    test script for testing purpose was not possible.

    Args:
        text (str): String in which words are to be counted.
        word_max (int): Maximum number of words allowed from user input.
        word_max (int): Maximum characters of words allowed from user input.

    Returns:
        True: number of words in text is greater than word_max or char_max.
        False: number of words in text is NOT greater than word_max or
               char_max.
    """
    word_over = len(ta.get_words(text)) > word_max

    char_over = len(text) > char_max

    return word_over or char_over


def _is_over_err_msg(input_text):
    """Returns form page with an error message stating that input text has too
    many words and/or characters.

    Args:
        input_text (str): text entered by user.

    Return:
        (template): data that will be used to render webpage on client-side.

    """
    msg = f'''Text exceeds {WORD_MAX} words or
                 {CHAR_MAX} characters:
                 {len(ta.get_words(input_text))} words;
                 {len(input_text)} characters.'''

    return render_template("form.html", msg=msg,
                           input_text=input_text,
                           max=WORD_MAX,
                           is_over=True)


def _max_err_msg():
    """Returns form page with an error message stating that max is not a
    natural number.

    Returns:
        (response): data that will be used to render webpage on client-side.

    """
    err = "Bad input: 'max' can only be a positive whole number."
    stack_trace = tb.format_exc()
    # Add security policy
    response = make_response(render_template("error.html",
                                             err=err,
                                             stack_trace=stack_trace))
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


def _unknown_post_err_msg():
    """Returns page with an error message stating that some other POST action
    besides Count, Merge or Split was requested.

    Returns:
        (response): data that will be used to render webpage on client-side.
    """
    err = "submit_button neither Count, Merge nor Split!"
    stack_trace = "Not an exception!"

    # Add security policy
    response = make_response(render_template("error.html",
                                             err=err,
                                             stack_trace=stack_trace))
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


def _not_get_post_err_msg():
    """Returns page with an error message stating that some other request
    besides GET or POST was made.

    Returns:
        (response): data that will be used to render webpage on client-side.
    """

    err = ("Not a GET or POST request; HEAD request likely made: " +
           request.method)

    response = make_response(render_template("error.html", err=err))
    response.headers['Content-Security-Policy'] = "default-src 'self'"

    return response


def _misc_err_msg(exception):
    """Returns page with an error message stating that cause of error was due
    to various other things that could've gone wrong.

    Args:
        exception: Exception obj of varying type.

    Returns:
        (template): data that will be used to render webpage on client-side.
    """
    err = str(exception)
    stack_trace = tb.format_exc()

    response = make_response(render_template("error.html",
                                             err=err,
                                             stack_trace=stack_trace))
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


@app.errorhandler(400)
def bad_request(error):
    """Returns web page with description and stack trace of exception invoked
    by an HTTP Bad Request Error (400)

    Args:
        Error (exceptions.BadRequest): Error raised by an HTTP Bad
                                       Request Error (400).

    Returns:
        (template): data that will be used to render webpage on client-side.


    """
    err = str(error) + "\n(Input possibly passed NoneType object)"
    stack_trace = tb.format_exc()

    response = make_response(render_template("error.html",
                                             err=err,
                                             stack_trace=stack_trace))
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


@app.route("/sentencecow", methods=['POST', 'GET'])
def process_text():
    """Handles HTTP requests from client-side of app that allows users
    to enter a text and get information about it.

    Raises:
        NotInTextError: A custom exception from the textanalysis module
                        that is raised when a provided sentence cannot be
                        matched with its equivalent in a text.

        ValueError: if the user enters a non-integer value for word-max;
                    also handles various exceptions raised lower down.

        TypeError: handles various exceptions raised lower down.

        IndexError: handles various exceptions raised lower down.

        MemoryError: handles exceptions raised in textanalysis if text
                     exceeds developer-defined memory constraint.

    Returns:
        response (flask.Response): object to data back to a specified
                                   Jinja template that will then be used
                                   for rendering on the client side.
    """

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

        if request.method == 'POST':

            # Request to parse text made from form.html
            if request.form['submit_button'] == 'Count':

                # Get everything we'll need to parse the sentences from a text
                input_text = request.form['input_text']

                # Check that word_max has been respected
                if _is_over(input_text, WORD_MAX, CHAR_MAX):
                    return _is_over_err_msg(input_text)

                # LeGuinCounter expects an integer
                try:
                    word_max = int(request.form['max'])
                except ValueError:
                    return _max_err_msg()

                # Trailing whitespaces are superfluous
                input_text = input_text.rstrip()

                # Parse text
                lgcounter = LeGuinCounter(input_text)

            # Request to merge a sentence with the one following it.
            # Made from results.html
            elif request.form['submit_button'] == 'Merge':

                # Get everything we'll need to merge sentences
                # and need to send data back to results.html
                input_text = request.form['input_text']
                word_max = request.form['max']
                sent_list = request.form.getlist('sent_list[]')

                # pos of first sentence in merge
                index = int(request.form['index'])

                # LeGuinCounter expects an integer
                try:
                    word_max = int(word_max)
                except ValueError:
                    return _max_err_msg()

                # Trailing whitespaces are superfluous
                input_text = input_text.rstrip()

                # Parse text
                lgcounter = LeGuinCounter(input_text)

                # The parsing above generates a sentence list based on the
                # original text sent via form.html. However, if users have made
                # merges or splits since then, they will not appear: only the
                # results of the first parsing will.

                # To keep track of any previous merges/splits made on the text,
                # a modified sent_list is passed with every POST request.
                # This requires, however, overriding the LeGuinCounter's
                # sent_list. Admittedly, not the best design, but it works.
                lgcounter.sentences = sent_list

                # Merge sentence at current index with the one following it
                lgcounter.merge_next(index)

            # Request to split a sentence in two parts
            # Made from results.html
            elif request.form['submit_button'] == 'Split':

                # Position of sentence to be split in sent_list
                index = int(request.form['sentindex'])

                # First segment of split sentence
                first_part = request.form['firstpart']

                # The rest of the data that needs to be POSTed on every change
                input_text = request.form['input_text']
                word_max = request.form['max']
                sent_list = request.form.getlist('sent_list[]')

                # LeGuinCounter expects an integer
                try:
                    word_max = int(word_max)
                except ValueError:
                    return _max_err_msg()

                # Trailing white spaces are suprefluous
                input_text = input_text.rstrip()

                # Parse text
                lgcounter = LeGuinCounter(input_text)

                # Read comments under 'Merge'
                lgcounter.sentences = sent_list

                # Divide sentence at 'index' in to two with first having to
                # match the argument 'first_part'
                lgcounter.split_sentence(index, first_part)

            else:
                return _unknown_post_err_msg()

            # Get list of LeGuinSentence objects to facilitate the highlighting
            # of parsed text in the UI layer
            lg_sentlist = lgcounter.generate_LGSentenceList(input_text,
                                                            lgcounter.sentences,
                                                            word_max)

            # Want to keep lgcounter classes, which are domain-level,
            # decoupled from HTML/JS code which is UI level
            highlight_data = [(l.start, l.end, l.is_over, l.whitespace)
                              for l in lg_sentlist]

            # Useful when printing a table that describes each sentence
            sentences = [{'content': s, 'wordcount': lgcounter.count_words(s)}
                         for s in lgcounter.sentences]

            # Get number of words in original and parsed texts
            # If they're not equal, then it's likely the last part of the
            # original text got lobbed off because it was missing a terminating
            # punctuation mark or was split in the middle of a word.
            wordcounts = {
                'original': len(ta.get_words(input_text)),
                'parsed': sum(sentence['wordcount'] for sentence in sentences)
            }

            # Add security policy
            response = make_response(render_template("results.html",
                                                     input_text=input_text,
                                                     sentences=sentences,
                                                     max=word_max,
                                                     highlight_data=highlight_data,
                                                     wordcounts=wordcounts))

            response.headers['Content-Security-Policy'] = "default-src 'self'"
            return response


        # Server will return a 405 error code if GET or POST not made.
        # Note that HEAD request will work as it only returns blank data
        # HEAD request executes this conditional, even though the error
        # page is technically not returned (Why??)
        return _not_get_post_err_msg()


    except (ta.NotInTextError, ValueError, TypeError, IndexError,
            MemoryError) as exception:

        return _misc_err_msg(exception)


if __name__ == "__main__":
    app.run()
