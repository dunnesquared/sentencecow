

function chooseSentence(){
	let sel = document.getElementById('sel_split');
	let i = sel.selectedIndex;

  const options = sel.options;
  let myTextArea = document.getElementById('sentencetextarea');

  //display sentence in textarea
  myTextArea.innerHTML = options[i].value;

  //DEBUG
  let isSame = myTextArea.innerHTML === options[i].value;
  console.log("isSame = ", isSame);
  console.log("myTextArea.innerHTML", JSON.stringify(myTextArea.innerHTML));
  console.log("options[i].value", JSON.stringify(options[i].value));

  //save index, and full sentence
  const inputIndexElem = document.getElementById('sent_index');
  //const inputFullSentElem = document.getElementById('full_sent');
  inputIndexElem.value = i;
  //inputFullSentElem.value = options[i].value;

}

/*
function selectText(){
	//Get the active Element
  const activeTextArea = document.activeElement;

  let selection = ""

   //Check that the element is the textarea, if not do nothing
  if (activeTextArea.id === 'sentencetextarea'){
      //Get the substring representing the highlighted text
     let start = activeTextArea.selectionStart;
     let end = activeTextArea.selectionEnd;
     selection = activeTextArea.value.substring(start, end);

     //DEBUG
     console.log("start: ",  start);
     console.log("end: ",  end);

    //output substring
    let outputArea = document.getElementById('output_area');
    outputArea.innerHTML = selection;

    // Save to input element
    const inputSubSent = document.getElementById('sub_sent');
    inputSubSent.value = selection;

  }

}
*/
function splitText(){
  //Get the active Element
  const activeTextArea = document.activeElement;

  let selection = ""

   //Check that the element is the textarea, if not do nothing
  if (activeTextArea.id === 'sentencetextarea'){
      //Get the substring representing the highlighted text
     let start = activeTextArea.selectionStart;
     let end = activeTextArea.selectionEnd;
     let text = activeTextArea.value;
     //output substring
     let outputArea = document.getElementById('output_area');


     //DEBUG
     console.log("start: ",  start);
     console.log("end: ",  end);

     //cursor the same
     if(start === end){
       //get the first and secondParts
       const firstPart = text.slice(0, start);
       const secondPart = text.slice(start, text.length);

       //display them to user
       outputArea.innerHTML = "Part 1 →" + firstPart + "\n" + "Part 2 →" + secondPart;

       //Save caret position, i.e. where text will be split
       const inputSplitPos = document.getElementById('split_pos');
       inputSplitPos.value = start;

			 //Save first and last parts of split sentence
			 const inputFirstPart = document.getElementById('first_part');
			 const inputSecondPart = document.getElementById('second_part');
			 inputFirstPart.value = firstPart;
			 inputSecondPart.value = secondPart;

     }
  }

  //DEBUG
  printSavedValues();

}


// Save index, full sentence.
function printSavedValues(){
	const index = document.getElementById('sent_index').value;
  const first = document.getElementById('first_part').value;
  const second = document.getElementById('second_part').value;
  const splitPos = document.getElementById('split_pos').value;

  const savedValues = `index = ${index}\nfirst = ${first}\nsecond = ${second}\nsplitPos = ${splitPos}`

  const savedValTextArea = document.getElementById('saved');
  savedValTextArea.innerHTML = savedValues;

}


//CHOOSING
//const button = document.getElementById('btn');
//button.addEventListener('click', chooseSentence);

//using both these seems to get the behaviour I want
try{

  const optionList = document.getElementById('sel_split');
  optionList.addEventListener('focus', chooseSentence);
  optionList.addEventListener('change', chooseSentence);

  //SELECTING
  //Have textArea listen for an event to indicate text has been selected
  const textArea = document.getElementById('sentencetextarea');
  //textArea.addEventListener('mouseup', selectText, false);
  textArea.addEventListener('mouseup', splitText, false);

  //SENDING DATA
  const splitButton = document.getElementById('split');
  splitButton.addEventListener('click', printSavedValues);

}catch(err){
  console.error(err.name + err.message);
}
