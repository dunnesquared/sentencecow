/**
 * @file Iniitalizes and manages form with which user will submit text.
 */

// WARNING: The code in this script file is NOT backwards-compatible with
// older browsers that do not support ES6/ECMAScript 2015. As such, this
// JS features for this program will likely not work in
// Safari: version < 10
// Chrome: version < 51
// Firefox: version < 54
// Source: https://www.w3schools.com/js/js_versions.asp

{ // Use ES6 block scope to prevent namespace conflicts with other JS files
  // possible loading in same page

  // N.B. The following globals were originally declared as consts. However,
  // Safari seems to have trouble accessing these variables if that's the case.
  // Changed declaration to var for compatibility.

  //============================ GLOBALS ======================================

  /**
   * @global
   * Max number of words allowed in text area.
   * Fetch from html file--originally from app.py: the one place where
   * maximum should be set.
   */
  var WORD_MAX = parseInt(document.getElementsByName('max')[0].max);

  /**
   * @global
   * Max number of characters allowed in text area.
   * Fetch from html file--originally from app.py: the one place where
   * maximum should be set.
   */
  var CHAR_MAX = parseInt(
      document.getElementsByName('input_text')[0].getAttribute('data-charmax'));

  /**
   * @global
   * Regular expression containing oft-used punctuation marks and symbols.
   */
  var PUNC_REGEX = /[!"#$%&'()*+,-./:;<=>?@[\\\]^_`{|}~]/g;

  /**
   * @global
   * Regular expression containing less-used punctuation marks.
   */
  var MOREPUNC_REGEX =
      /[․‥…‼⁇⁈⁉‟❝❞＂〝〞‛‘’❛❜]/g;

  /**
   * @global
   * Used in function refreshForm below.
   * ID value of timer returned by setTimeout() method
   */
  var TIMEOUT;

  //============================= MAIN ========================================

  // In case the word or character maxima are set to types or values in
  // app.py that will cause exceptions later on.
  try {
    let errorMessage = '';

    if (WORD_MAX < 1) {
      errorMessage = `
      Error in count.js:
      WORD_MAX = ${WORD_MAX}
      Value outside acceptable range.
      WORD_MAX must be an
      integer > 0.
      `;
      throw new RangeError(errorMessage);
    }

    if (!Number.isInteger(WORD_MAX)) {
      errorMessage = `
     Error in count.js:
     WORD_MAX = ${WORD_MAX}
     Bad type.
     WORD_MAX must be an integer.
     `;
      throw new TypeError(errorMessage);
    }
  } catch (err) {
    disableInputs();
    displayError(err);
  }

  // Bind event handler functions to events on loading of page.
  try {

    const textarea = document.querySelector("textarea");

    // Ensure that user can't submit an empty textarea to web script.
    textarea.addEventListener("DOMContentLoaded", enableSubmit);

    // Ensure that we count the words on the page.
    textarea.addEventListener("DOMContentLoaded", updateCounts);

    // Do both of the above as the user types text.
    textarea.addEventListener("input", refreshForm);

    // Erase placeholder text 'Write your text here' when user sets focus to
    // text area.
    textarea.addEventListener("focus", function() { this.placeholder = ''; });

    const maxBoxTextArea = document.getElementsByName("max")[0];

    // Ensure that user can't submit if max box is empty.
    maxBoxTextArea.addEventListener("input", enableSubmit);

    // Reset form when 'Reset' button clicked.
    const resetButton = document.getElementById('reset_button');
    resetButton.addEventListener("click", resetAll);

    // Need this code to handle to refresh the word counts in the event
    // the user hits the Back button from the Results page.
    window.addEventListener('pageshow', function(event) {
      // Page loading from cache.
      if (event.persisted) {
        console.log("Page was loaded from cache");
      } else {
        // I expected the page to be cached, but it's not. As soon as
        // you go back to the original form page, it makes a GET request.The
        // text inputted by the user is clearly cached though. Oh well...
        console.log("Page not loaded from cache");

        // Refresh counts and check submit button again!
        enableSubmit();
        updateCounts();
      }
    });

  } catch (err) {
    console.error(err.name + err.message);
  }

  //============================ FUNCTIONS ====================================

  /**
   * Displays error message on console and form.html page.
   * @param {string} err - The error message to display.
   */
  function displayError(err) {
    let errTag = document.getElementsByClassName('error')[0];
    errTag.color = 'red';
    errTag.innerHTML = '\n' + err.name + err.message;
  }

  /**
   * Ensures user can't proceed with entering data on form if exception thrown.
   */
  function disableInputs() {
    document.querySelector("textarea").readOnly = true;
    document.getElementsByName("max")[0].readOnly = true;
    document.getElementById('count').disabled = true;
    document.getElementById('reset_button').disabled = true;
  }

  /**
   * Returns number of words in a string.
   * @param {string} text - text inputtted by user for later parsing.
   * @returns {number} Number of words in text.
   */
  function countWords(text) {
    // Remove dashes so we don't over-count or under-count words in text.
    // En dashes are used to denote durations, e.g. WWII was from 1939–1945.
    // Em dashes are used to separate clauses. The words touching an em-dash
    // are distinct (unlike a hyphen that creates one word out of usually two).
    text = text.replace(/—/g, ' '); // em dash
    text = text.replace(/–/g, ' '); // en dashes

    // Remove all punctuation and symbols from text.
    // Something like '? ! % ^' should not register as four separate words,
    // but as zero words.
    text = text.replace(PUNC_REGEX, '');
    text = text.replace(MOREPUNC_REGEX, '');

    // Get words from text.
    // Regex pattern:
    // \S+: Find string of at least one character with no whitespace characters.
    // g: Find all matching strings, not just the first one found.
    // match: return all strings that match regex.
    let words = text.match(/\S+/g);

    // null returned by match above if text is empty; avoid a
    // NullPointerException by returning 0 in this case.
    return words ? words.length : 0;
  }

  /**
   * Refreshes output that indicates number of words and characters currently in
   * text area. If text is over either max, the function prevents the user from
   * submitting the form.
   */
  function updateCounts() {
    // Initial values
    let text = "";
    let numWords = 0;
    let numChars = 0;
    let countMessage = "";

    try {
      // Count words and characters
      text = document.getElementsByName("input_text")[0].value;
      numWords = countWords(text);
      numChars = text.length;

      // Fetch elements where updated counts will be displayed
      let wordCountArea = document.getElementById('word-count');
      let charCountArea = document.getElementById('char-count');
      let wordCountOverArea = document.getElementById('wordcount-over');
      let charCountOverArea = document.getElementById('charcount-over');
      let count_button = document.getElementById('count');

      // If text over either max, make sure users know about it and don't let
      // them send the form.
      if (numWords > WORD_MAX) {
        count_button.disabled = true;
        countMessage = "← Too many words!";
        wordCountOverArea.innerHTML = countMessage;
      } else {
        wordCountOverArea.innerHTML = "";
      }

      if (numChars > CHAR_MAX) {
        count_button.disabled = true;
        countMessage = "← Too many characters!";
        charCountOverArea.innerHTML = countMessage;
      } else {
        charCountOverArea.innerHTML = "";
      }

      // Update display of word and character counts.
      wordCountArea.innerHTML = numWords;
      charCountArea.innerHTML = numChars;

    } catch (err) {
      disableInputs();
      displayError(err);
    }
  }

  /**
   * Enables or disables the 'Count' button depending on the state of the
   * form. The submit button is only enabled if the user has entered text
   * whose word and character counts are equal to or below their respective
   * maxima. Also, the number-of-words-per-sentence text field must contain a
   * value. If any of these conditions are not met, the submit button is
   * disabled.
   */
  function enableSubmit() {

    // Verify number of words and characters is good
    const text = document.getElementsByName("input_text")[0].value;
    const numWords = countWords(text);
    const numChars = text.length;
    const wordOk = numWords > 0 && numWords <= WORD_MAX;
    const charOk = numChars > 0 && numChars <= CHAR_MAX;

    // Ensure user actually entered a sentence max
    const max = document.getElementsByName("max")[0].value;
    const maxBlank = max === '';

    // Check counts and max text area!
    let countButton = document.getElementById('count');

    if (wordOk && !maxBlank && charOk) {
      countButton.disabled = false; // enable!
    } else {
      countButton.disabled = true; // disable!
    }
  }

  /**
   * Resets all form elements to initial states: empty text area; disabled
   * submit button.
   */
  function resetAll() {
    // Clear the text area.
    document.getElementById("lgcform").reset();

    // It's possible, though hopefully unlikely, that the Jinja template
    // rendered a "You're over the word count max" error message. If this JS
    // script is doing its job, that shouldn't happen. That said, if it does,
    // you'll want to erase the error message when the user presses the reset
    // button.
    let serverMessage = document.getElementsByClassName("over")[0];

    // Check to see whether the serverMessage was rendered in the first place.
    // If so, clear it!
    if (typeof serverMessage !== 'undefined') {
      serverMessage.innerHTML = "";
    }

    // Disable the 'Count' button; clear the character counts.
    enableSubmit();
    updateCounts();

    // Put back placeholder text.
    const textarea = document.querySelector("textarea");
    textarea.placeholder = "Write your text here...";
  }

  /**
   * Updates form elements as the user types. Word and character counts
   * are refreshed in real-time, as well as the 'Count' button's state, which
   * which clearly depends on these counts.
   * To avoid typing-lag on old or busy machines, the function does not refresh
   * the counts with every keystroke. While refreshForm is executed on every
   * keystroke, the function upCounts is not: it is only executed after
   * a specified delay (e.g. 500 milliseconds), and no sooner than that.
   */
  function refreshForm() {

    // Should the 'Count' button be enabled or disabled?
    enableSubmit();

    // Tell users why the word counts have disappeared with every keystroke.
    document.getElementById('word-count').innerHTML = 'Processing...';
    document.getElementById('char-count').innerHTML = 'Processing...';
    document.getElementById('wordcount-over').innerHTML = '';
    document.getElementById('charcount-over').innerHTML = '';

    // Stop updateCounts from executing too soon. If we're typing at normal
    // speed, there's no benefit to every single invocation of updateCounts
    // when a key is pressed. Only the last one matters (i.e. when the user
    // stops typing).
    clearTimeout(TIMEOUT);

    // Call updateCounts only after 500 milliseconds have passed.
    TIMEOUT = setTimeout(updateCounts, 500);
  }
}
