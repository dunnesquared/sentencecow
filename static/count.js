// To do:
// Understand regex below
// Make text typing in box faster
// Ensure word max has entry filled before disabling submit
// Wrap three oninput functions into a single function
// cross browser testing

// Max number of inputted words allowed
const WORD_MAX = 150;

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
    console.log(err.message);
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
      console.log(err.message);
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

  //console.log("IN enableSubmit");
  if (countWords(text) && !maxBlank) {
    //console.log("ENABLED!!");
    countButton.disabled = false;
  }else{
    //console.log("DISABLED!!");
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
