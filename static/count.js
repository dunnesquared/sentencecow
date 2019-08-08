//alert("Hello World")

/*
function sayHello(){
  alert("Hello World Pizza!!")
  return true;
}
*/


/**
 * Enables submit button if text in textarea;
 * Disables submit button if textarea empty.
*/
function enableSubmit(){

  let countButton = document.getElementById('count');
  const text = document.getElementsByName("input_text")[0].value;

  if (countWords(text)){
    countButton.disabled = false;
  }else{
    countButton.disabled = true;
  }
}


const WORD_MAX = 150;

function countWords(text){
  let words = text.match(/\S+/g);
  return words ? words.length : 0;
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
