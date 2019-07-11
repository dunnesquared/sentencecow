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


app = Flask(__name__)

@app.route("/leguinncounter", methods=['POST', 'GET'])
def index():
    '''Returns web pages that allow users to see whether their texts satisfy
       the criterion that their sentences have fewer or the same user-set
       number of words.
      '''

    if request.method == 'GET':
        # Render main page of web app
        return render_template("form.html")

    elif request.method == 'POST':
        # User requests to merge a sentence with the one following it.
        if 'merge_list' in request.form:

            #Get everything we'll need to merge sentences and send data back
            index, max, input_text, sent_list = request.form['merge_list'].split('::')

            # LeGuinnCounter expects integers, not strings for these values
            index = int(index)
            max = int(max)

            #TEMPORARY CODE - you need to handle this situation better
            #Strip text of any leading whitespace
            input_text = input_text.lstrip()

            # Initialize domain object
            lg = LeGuinnCounter(input_text)

            # We can't use sentence list generated when we create a LeGuinn-
            # Counter object: regardless, how many times we merge sentences
            # that parsing will always be the same (and so undo the parsing).
            # Thus, it's important we use the sentences from our last merge.
            # and replace the sentences in our object with them. Not the best
            # design; will fix in later iteration
            sentences = sent_list.split('||')
            lg.sentences = sentences

            # Merge sentence at current index with the one following it
            lg.merge_next(index)

            # So we can send back sentence list to user
            sentences = lg.sentences

            # Get list of LG_sentences so we can do highlighing more easily
            lg_sentlist = lg.generate_LGSentenceList(input_text, sentences, max)

            # Create a tuples list that you can send to the template; also
            # want to decouple the domain stuff from the controller/ui stuff
            highlight_data = [ (l.start, l.end, l.isOver) for l in lg_sentlist]


        # First parsing of text!
        else:

            #Get everything we'll need to get the sentences from a text
            input_text = request.form['input_text']
            max = int(request.form['max'])

            #TEMPORARY CODE - you need to handle this situation better
            #Strip text of any leading whitespace
            input_text = input_text.lstrip()

            # Initialize domain object
            lg = LeGuinnCounter(input_text)

            # So we can send back sentence list to user
            sentences = lg.sentences

            # Get list of LG_sentences so we can do highlighing more easily
            lg_sentlist =lg.generate_LGSentenceList(input_text, sentences, max)

            # Create a tuples list that you can send to the template; also
            # want to decouple the domain stuff from the controller/ui stuff
            highlight_data = [ (l.start, l.end, l.isOver) for l in lg_sentlist]

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



if __name__ == "__main__":
    app.run()
