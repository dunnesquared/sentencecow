// To do:
// Cross browser testing
// Documentation at top of module

// Max number of words allowed in textarea
const WORD_MAX = 150;

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


// On loadig page...
// Ensure that user can't submit an empty textarea to web script
// Ensure that we count the words on the page
let textarea = document.querySelector("textarea");
let count_button = document.getElementById('count');
textarea.addEventListener("load", enableSubmit());
textarea.addEventListener("load", updateWordCount());


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
 * Check # of words in string < WORD_MAX
 */
function checkWordCount(){
  let text = "";
  let numWords = 0;

  try{
    text = document.getElementsByName("input_text")[0].value;
    numWords = countWords(text);
    console.log("numWords =  " + numWords);
  }
  catch(err){
    disableInputs();
    displayError(err);
  }

  if (numWords > WORD_MAX){
    let count_button = document.getElementById('count');
    count_button.disabled = true;
    //Change colour of word count to red
    document.getElementById('word-count').style.color = 'red';
  }else{
    // Change text colour back to black
    document.getElementById('word-count').style.color = 'black';
  }
}


/**
 * Refresh output that indicates number of words currently in textarea
*/
function updateWordCount(){
    let text = "";
    let numWords = 0;

    try{
      text = document.getElementsByName("input_text")[0].value;
      numWords = countWords(text);
      console.log("numWords =  " + numWords);
      document.getElementById('word-count').innerHTML = numWords + ` out of ${WORD_MAX}`;
    }
    catch(err){
      disableInputs();
      displayError(err);
    }
}

/**
 * Enable submit button if text in textarea;
 * Disable submit button if textarea empty.
*/
function enableSubmit(){
  let countButton = document.getElementById('count');
  const text = document.getElementsByName("input_text")[0].value;
  const max = document.getElementsByName("max")[0].value;

  console.log("Max = " + max);
  console.log(typeof(max));
  console.log(max === '');
  maxBlank = max === ''

  if (countWords(text) && !maxBlank) {
    countButton.disabled = false;
  }else{
    countButton.disabled = true;
  }
}

/**
 * Reset all form elements to initial states
*/
function resetAll(){
  // Clear form to default values
  document.getElementById("lgcform").reset();

  // Handle whatever reset didn't
  enableSubmit();
  updateWordCount();
  checkWordCount();
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
  document.getElementById('word-count').innerHTML = 'Processing...';

  // Kill the last timeout. If we're typing at normal speed, there's no
  // benefit to every single invocation of updateWordCount when a key is pressed.
  // Only the last one matters (i.e. when the user stops typing.)
  clearTimeout(timeout);
  timeout = setTimeout(updateWordCount, 500); //500 milliseconds

  checkWordCount();
}
