from flask import Flask
from flask import render_template
from flask import request

from leguinncounter import LeGuinnCounter

app = Flask(__name__)

"""
def not_none(input):
    if input == None:
        return False
    else:
        return True

def is_empty(input):
    '''Check whether user entered anything into form field'''
    if input == None or len(input) == 0:
        return True
    else:
        return False


def is_integer(input):
    '''Check whether user entered an integer. Don't rely on form to check!!'''
    try:
        int(input)

        if isinstance(input, float):
            return False

        return True
    except ValueError:
        return False

def is_between(num, lbound=1, ubound=999):
    '''Ensure integer is between the bounds'''
    if num >= lbound and num <= ubound:
        return True
    else:
        return False
"""


@app.route("/leguinncounter", methods=['POST', 'GET'])
def index():

    if request.method == 'GET':

        # render text box to enter text
        print(request.method)
        return render_template("form.html")
        #return render_template("form.html", prob_num=prob_num, prob_descr=prob_descr)

    elif request.method == 'POST':
        print(request.method)

        input_text = request.form['input_text']
        print(input_text)

        lg = LeGuinnCounter(input_text)
        sentences = lg.sentences

        long_sentences = lg.sentences_more_than(max=4)

        return render_template("results.html", input_text=input_text, sentences = sentences, long_sentences = long_sentences)

        # get passed data: text, max number
        # process text
            # create lg object
            # find out which sentences are more than Max
            # render output return list of maps






        '''

        input = request.form['var']

        if is_empty(input.strip()):
            err = "No input entered."
            return render_template("error.html", err=err)

        #take out this block if input need not be an integer
        if is_integer(input) == False:
            err = "Input is not an integer."
            return render_template("error.html", err=err)

        num = int(input)
        status = prob.check_input(num)

        if status[0] == False:
            err = status[1]
            return render_template("error.html", err=err)

        prob.set_input(num)
        answer = prob.compute_solution()

        return render_template("answer.html", answer=answer)

        '''

    else:
        #server will return a 405 error code if other methods specified
        #Note that head request will work as it only returns blank data
        #Head request exectutes this conditional, even though the error
        #page is technically not returned (weird?)
        err = "Not a GET or POST request; HEAD request likely made: " + request.method
        return render_template("error.html", err=err)



if __name__ == "__main__":
    app.run()
