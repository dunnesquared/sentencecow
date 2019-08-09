// To do:
// Make enableSubmit more responsive - doesn't disable button if just detelete all contents but don't click down later


const WORD_MAX = 150;
let textarea = document.querySelector("textarea");

// Ensure that user can't submit an empty textarea to web script on first load
textarea.addEventListener("load", enableSubmit());



function sayHello(){
  alert("Hello World Pizza!!")
  return true;
}


function countWords(text){
  let words = text.match(/\S+/g);
  return words ? words.length : 0;
}




function checkWordCount(){
  //Get input text
  let text = "";
  let numWords = 0;

  try{
    text = document.getElementsByName("input_text")[0].value; //have to specify index as there is more than element by that name
    //console.log(text); //NOT WORKING! Giving undefined! try using id instead

    //Get number of words in text
    numWords = countWords(text);
    console.log("numWords =  " + numWords);
  }
  catch(err){
    console.log(err.message);
  }

  //See whether number of words is greater than WORD_MAX
  //True -> show alert; deactivate submit button
  //False -> carry on
  if (numWords > WORD_MAX){
    let count_button = document.getElementById('count');
    //count_button.disabled = true;
    alert("Your text is over " + WORD_MAX + " words long.");
  }else{
    alert("Looks good!");
  }
}



function check(){
  //Get input text
  let text = "";
  let numWords = 0;

  try{
    text = document.getElementsByName("input_text")[0].value; //have to specify index as there is more than element by that name
    //console.log(text); //NOT WORKING! Giving undefined! try using id instead

    //Get number of words in text
    numWords = countWords(text);
    console.log("numWords =  " + numWords);
  }
  catch(err){
    console.log(err.message);
  }

  //See whether number of words is greater than WORD_MAX
  //True -> show alert; deactivate submit button
  //False -> carry on
  if (numWords > WORD_MAX){
    let count_button = document.getElementById('count');
    //count_button.disabled = true;
    alert("Your text is over " + WORD_MAX + " words long.");
  }else{
    alert("Looks good!");
  }
}



/**
 *
 *
 *
*/
function updateWordCount(){
    let text = "";
    let numWords = 0;

    try{
      text = document.getElementsByName("input_text")[0].value; //have to specify index as there is more than element by that name
      //console.log(text); //NOT WORKING! Giving undefined! try using id instead

      //Get number of words in text
      numWords = countWords(text);
      console.log("numWords =  " + numWords);

      document.getElementById('word-count').innerHTML = numWords;

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

  //console.log("IN enableSubmit");


  if (countWords(text)){
    console.log("ENABLED!!");
    //countButton.disabled = false;
  }else{
    console.log("DISABLED!!");
    //countButton.disabled = true;
  }
}
