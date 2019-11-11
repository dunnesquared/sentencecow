# Sentence Cow 🐄

Sentence Cow is a Flask-based web application that extracts sentences from a
text and counts the number of words in each sentence, *as best as possible*.
Any string of alphanumeric characters that ends with a terminating punctuation
mark such as . ! ? and the like is considered to be a sentence, regardless of
grammar or syntax.

Sentence Cow doesn't use any NLP algorithms to detect sentences–just a lot
regular expressions and checking.

End-users can use tools to 'split' or 'merge' sentences where the application
fails to extract a sentence in a way that they might expect.

A live demo of the project is available [here][demo].

## Setting up the development environment

> It is highly recommended that you are in a virtual environment before
>doing any of the below.

After cloning the [repository][repo], perhaps the easiest way to get Sentence
Cow's dependencies is to type the following on the console:

```sh
pip install -r requirements.txt
```

This will install everything you need, including the [nose][nose] testing
framework.

To run the tests, simply make sure you are in the project's root folder and
then on the console,

```sh
nosetests
```

Alternatively, you can rely on setup.py to download the latest versions of
the dependencies via

```sh
pip install -e .
```

The testing framework won't be there, however. You'll have to download it
separately:


```sh
pip install nose
```

## Running Sentence Cow

From the project root, type

```sh
python sentencecow/app.py
```

You can then open your favourite browser to *http://localhost:5000/sentencecow*
the program in action.


## Updating `abbreviations.txt`

Sentence Cow relies on a data file to handle sentences that contain
abbreviations that end with a period (e.g. 'Mr.', 'etc.', 'i.e.'). Essentially,
the program will 'skip' any abbreviation listed in `data/abbreviations.txt`.
That is, a listed abbreviation won't be taken as the end of a sentence,
except at the end of a text.

A separate script, `abbrevscrape`,  is used to generate `abbreviations.txt`,
whose repository can be found [here][abbrev]. Please read the instructions
about running the script and editing the text file.

Should you wish to replace `abbreviations.txt` with an updated version,
simply copy the new file to the `data` folder. It's always a good idea to backup
the old abbreviations file in case there's something
wonky with the new one.

## Feedback

Any positive, constructive feedback is welcome. I am a novice programmer
who knows he has many, many things to learn.


<!-- Markdown link & img dfn's -->
[demo]: https://zaxel9.pythonanywhere.com/sentencecow
[repo]: https://github.com/dunnesquared/sentencecow
[nose]: https://nose.readthedocs.io/en/latest/
[abbrev]: https://github.com/dunnesquared/sentencecow
