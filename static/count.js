// To do:
// Cross browser testing
// Documentation at top of module

// Max number of words allowed in textarea
// Fetch from html file--originally from app.py: the one place to set max val
const WORD_MAX = parseInt(document.getElementsByName('max')[0].max);
const CHAR_MAX = parseInt(document.getElementsByName('input_text')[0].getAttribute('data-charmax'));

//const CHAR_MAX = parseInt(document.getElementsByName('input_text')[0].maxLength);

// DEBUG
console.log("CHAR_MAX = ", CHAR_MAX);

// Regular expression containing oft-used punctuation marks and symbols
const PUNC_REGEX = /[!"#$%&'()*+,-./:;<=>?@[\\\]^_`{|}~]/g;

// Regular expression containing less-used punctuation marks
const MOREPUNC_REGEX = /[․‥…‼⁇⁈⁉‟❝❞＂〝〞‛‘’❛❜]/g;


// In case the bizzare happens...
try{
  if (WORD_MAX < 1){
    let s = `
    Error in count.js:
    WORD_MAX = ${WORD_MAX}
    Value outside acceptable range.
    WORD_MAX must be an
    integer > 0.
    `
   throw new RangeError(s);
 }else if(!Number.isInteger(WORD_MAX)){
   let s = `
   Error in count.js:
   WORD_MAX = ${WORD_MAX}
   Bad type.
   WORD_MAX must be an integer.
   `
  throw new TypeError(s);

 }
}
catch(err){
  disableInputs();
  displayError(err);
}


// On loadig page...
// Ensure that user can't submit an empty textarea to web script
// Ensure that we count the words on the page
// let textarea = document.querySelector("textarea");
// textarea.addEventListener("load", enableSubmit());
// textarea.addEventListener("load", updateWordCount());


/**
 * Display error messages on console and form page
*/
function displayError(err){
  console.error(err.name + err.message);
  let errTag = document.getElementsByClassName('error')[0];
  errTag.color = 'red';
  errTag.innerHTML =  '\n' + err.name + err.message;
}


/**
 * Ensure user can't proceed with form if exception thrown
*/
function disableInputs(){
  document.querySelector("textarea").readOnly = true;
  document.getElementsByName("max")[0].readOnly = true;
  document.getElementById('count').disabled = true;
  document.getElementById('reset_button').disabled = true;
}


/**
 * Return number of words in a string.
*/
function countWords(text){
  // Edit text so we over-count or undercount words in text`
  // En dashes are used to denote durations, e.g. WWII was from 1939–1945
  // Em dashes are used to separate clauses. The words touching an em-dash are
  // distinct (unlike a hyphen that creates one word out of usually two)

  text = text.replace(/—/g, ' '); // em dash
  text = text.replace(/–/g, ' '); // en dashes

  // Remove all punctuation and sybols from text.
  // Something like '? ! % ^' should not register as four separate words,
  // but as zero words.
  text = text.replace(PUNC_REGEX, '');
  text = text.replace (MOREPUNC_REGEX, '');

  // Get words from text
  // arrayStrings = s.match(/regex/modifier);
  // \S+ Find string of at least one character with no whitespace characters
  // g  Find all matching strings, not just the first one found
  // match: return all strings that match regex
  let words = text.match(/\S+/g);

  return words ? words.length : 0;
}



/**
 * Refresh output that indicates number of words currently in textarea
 * If text over max allowed, don't allow the user to send the form!
*/
function updateWordCount(){
    let text = "";
    let numWords = 0;
    let numChars = 0;
    let msg = "";

    console.log("updateWordCount button: ", document.getElementById('count').disabled);
    try{

      // Count words
      text = document.getElementsByName("input_text")[0].value;
      numWords = countWords(text);
      numChars = text.length;
      let wordCount = document.getElementById('word-count');
      let charCount = document.getElementById('char-count');
      let wordCountOver = document.getElementById('wordcount-over');
      let charCountOver = document.getElementById('charcount-over');
      let count_button = document.getElementById('count');

      // If text over max, make sure users know about it and don't let them
      // send the form
      if (numWords > WORD_MAX){
        // Disable submit

        count_button.disabled = true;


        msg = "← Too many words!"

        // Change colour of word count to indicate user has gone over max
        wordCountOver.innerHTML = msg;
        //wordCountOver.style.color = 'Crimson';
        //wordCountOver.style.fontWeight = '900';

      }else{
        wordCountOver.innerHTML = "";
      }

      if (numChars > CHAR_MAX){
        // Disable submit
        count_button.disabled = true;


        msg = "← Too many characters!"

        // Change colour of word count to indicate user has gone over max
        charCountOver.innerHTML = msg;
        //charCountOver.style.color = 'Crimson';
        //charCountOver.style.fontWeight = '900';

      }else{
        charCountOver.innerHTML = "";
      }


      wordCount.innerHTML = numWords;
      charCount.innerHTML = numChars;

    }
    catch(err){
      disableInputs();
      displayError(err);
    }
}

/*
function updateWordCount(){
    let text = "";
    let numWords = 0;
    let msg = "";

    try{

      // Count words
      text = document.getElementsByName("input_text")[0].value;
      numWords = countWords(text);
      wordCount = document.getElementById('word-count');

      // If text over max, make sure users know about it and don't let them
      // send the form
      if (numWords > WORD_MAX){

        // Disable submit
        let count_button = document.getElementById('count');
        count_button.disabled = true;

        // Change colour of word count to indicate user has gone over max
        document.getElementById('word-count').style.color = 'Crimson';
        document.getElementById('word-count').style.fontWeight = '900';

      }else{
        // Word count okay. Reset it back to blacl.
        document.getElementById('word-count').style.color = 'black';
        document.getElementById('word-count').style.fontWeight = '400';
      }

      // Handle singular and plural case for word count display
      msg = numWords;

      if (numWords == 1){
        msg +=  ' word' + `       (${text.length} character(s))`
      }else{
        msg += ' words' + `        (${text.length} character(s))`
      }

      wordCount.innerHTML = msg;
    }
    catch(err){
      disableInputs();
      displayError(err);
    }
}
*/

/**
 * Enable submit button if text in textarea;
 * Disable submit button if textarea empty.
*/
function enableSubmit(){
  let countButton = document.getElementById('count');
  const text = document.getElementsByName("input_text")[0].value;
  const max = document.getElementsByName("max")[0].value;
  const numWords = countWords(text)
  const numChars = text.length

  // DEBUG statements
  console.log("Max = " + max);
  console.log(typeof(max));
  console.log(max === '');
  console.log("enableSubmit button: ", document.getElementById('count').disabled);

  wordOk = numWords > 0 && numWords <= WORD_MAX
  charOk = numChars > 0 && numChars <= CHAR_MAX
  maxBlank = max === ''

  if (wordOk && !maxBlank && charOk) {
    countButton.disabled = false; // enable!
  }else{
    countButton.disabled = true; // disable!
  }
}

/**
 * Reset all form elements to initial states
*/
function resetAll(){
  // Clear form to default values
  document.getElementById("lgcform").reset();

  // It's possible, though hopefully unlikely, that the Jinja template rendered
  // an "you're over the word count max" error message. If this JS script is
  // is doing its job, that shouldn't happen
  // That said, if it does, you'll want to erase the error message when
  // the user presses the reset button.
  let appMsg = document.getElementsByClassName("over")[0];

  // Check to see whether the appMSg was rendered in the first place. If so,
  // clear it!
  if (typeof appMsg !== 'undefined'){
    appMsg.innerHTML = "";
  }

  // Handle whatever reset didn't
  enableSubmit();
  updateWordCount();

  // Put back placeholder text
  const textarea = document.querySelector("textarea");
  textarea.placeholder = "Write your text here..."
}


/**
 * Check and update other parts of form vis-a-vis current state. functions
 * delays updating the form with the current word count in order to so the
 * update function runs every time a key is pressed. This should hopefully
 * avoid any typing-lag on older or busy machines.
*/

let timeout;

function refresh(){
  enableSubmit();

  // Tell users what's happening so they don't freak out
  // Need to switch back to black in case word count is over the max
  //document.getElementById('word-count').style.color = 'black';
  //document.getElementById('word-count').style.fontWeight = '400';
  document.getElementById('word-count').innerHTML = 'Processing...';
  document.getElementById('char-count').innerHTML = 'Processing...';
  document.getElementById('wordcount-over').innerHTML = '';
  document.getElementById('charcount-over').innerHTML = '';

  // Kill the last timeout. If we're typing at normal speed, there's no
  // benefit to every single invocation of updateWordCount when a key is pressed.
  // Only the last one matters (i.e. when the user stops typing.)
  clearTimeout(timeout);
  timeout = setTimeout(updateWordCount, 500); //500 milliseconds
}

// EVENT HANDLERS
try{
  // On loadig page...
  // Ensure that user can't submit an empty textarea to web script
  // Ensure that we count the words on the page
  const textarea = document.querySelector("textarea");
  textarea.addEventListener("DOMContentLoaded", enableSubmit);
  textarea.addEventListener("DOMContentLoaded", updateWordCount);
  textarea.addEventListener("input", refresh);
  textarea.addEventListener("focus", function () {
                            this.placeholder = this.placeholder ='';});

  const maxBoxTextArea = document.getElementsByName("max")[0];
  maxBoxTextArea.addEventListener("input", enableSubmit);

  const resetButton = document.getElementById('reset_button');
  resetButton.addEventListener("click", resetAll);

}catch(err){
  console.error(err.name + err.message);
}
