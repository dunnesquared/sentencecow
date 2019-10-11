{ // Use ECMA6 block scope to prevent namespace conflicts with other JS files
  // possible loading in same page

  /**
  * Reset split-part display and split-part values
  * if new sentence selected
  */
  function resetValues(){
     /*
     Algorithm :
     1. Get ref to area where split parts displayed; get their values
     2. Clear output area; set splits parts to ""
     */
     const outputArea = document.getElementById('output_area');
     let firstPart = document.getElementById('first_part').value;
     let secondPart = document.getElementById('second_part').value;

     outputArea.innerHTML = "";
     firstPart = "";
     secondPart = "";

     console.log("VALUES RESET!!");

     // Make sure not split submission happens until user has actually chosen
     // a split point
     const splitButton = document.getElementById('split');
     splitButton.disabled = true;
  }



  function chooseSentence(){
  	// Clear output areas and form values every time a new sentence has been
  	// selected
  	resetValues();

  	let sel = document.getElementById('sel_split');

  	let i = sel.selectedIndex;

    //DEBUG
    console.log("Selected Index = ", i);

    const options = sel.options;
    let myTextArea = document.getElementById('sentencetextarea');

    // Display sentence in textarea
    // Leading/trailing spaces are't necessary and just make the text weird to
    // look at
    myTextArea.innerHTML = options[i].value.trim();

    //DEBUG
    let isSame = myTextArea.innerHTML === options[i].value;
    console.log("isSame = ", isSame);
    console.log("myTextArea.innerHTML", JSON.stringify(myTextArea.innerHTML));
    console.log("options[i].value", JSON.stringify(options[i].value));

    //save index, and full sentence
    const inputIndexElem = document.getElementById('sent_index');
    //const inputFullSentElem = document.getElementById('full_sent');

    // Careful here: the value saved is the index that will be used
    // to access the sentence from sentences list in the web script
    // Because the way the option list is presented in results.html
    // with a 'placeholder' first option, i needs to be decremented by 1.
    inputIndexElem.value = i - 1;
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

  	//Only makes sense to do a split if there's something in the field
  	if (activeTextArea.value.trim().length === 0){
  		return;
  	}

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
         let firstPart = text.slice(0, start);
         let secondPart = text.slice(start, text.length);

  			 // Get rid of leading/trailing whitespaces. Not necessary
  			 firstPart = firstPart.trim();
  			 secondPart = secondPart.trim();

         // Display parts to user so long as they're not empty or full of
  			 // whitepace characters; no point in saving them either.
  			 if (firstPart.length !== 0 && secondPart.length !== 0){
  				 outputArea.style.fontStyle = "normal";

           //outputArea.innerHTML = "1) " + firstPart + "\n\n" + "2) " + secondPart;
           outputArea.innerHTML = "PART 1\n------\n" + firstPart + "\n\n" +
                                  "PART 2\n------\n" + secondPart;

  			}else{
  				outputArea.style.fontStyle = "italic";
  				outputArea.innerHTML = "Nothing to split. Please pick a split point " +
                                  "within the sentence, not on its edges."
  			}

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
    //printSavedValues();

  }


  // // Save index, full sentence.
  // function printSavedValues(){
  // 	const index = document.getElementById('sent_index').value;
  //   const first = document.getElementById('first_part').value;
  //   const second = document.getElementById('second_part').value;
  //   const splitPos = document.getElementById('split_pos').value;
  //
  //   const savedValues = `index = ${index}\nfirst = ${first}\nsecond = ${second}\nsplitPos = ${splitPos}`
  //
  //   const savedValTextArea = document.getElementById('saved');
  //   savedValTextArea.innerHTML = savedValues;
  //
  // }

  /**
  * Only allow split only if textarea is not empty
  * and neither split is purely whitespace characters
  */
  function enableSplit(){
  	/*
  	Algoithm
  	1. Access contents of textarea; handle to splitButoon
  	2. If empty, do not enable Split, exit. If not, go to 3
  	3. Get contents of first and second split
  	4. Check to see whether either one of the parts is empty (caret not pointed)
  	   or has only whitespace characters. If yes, do not enable Split; exit. If
  		 no, go to step 5.
  	 5. Enable submit
  	*/
  	const splitButton = document.getElementById('split');
  	const textArea = document.getElementById('sentencetextarea');

  	if (textArea.value != ""){
  		let firstPart = document.getElementById('first_part').value;
  		let secondPart = document.getElementById('second_part').value;

  		// Remove leading, trailing whitespaces
  		firstPart = firstPart.trim();
  		secondPart = secondPart.trim();

  		if (firstPart.length !== 0 && secondPart.length !== 0){
  			splitButton.disabled = false;
  		}else{
  			splitButton.disabled = true;
  		}
  	}else{
  		splitButton.disabled = true;
  	}
  }

  //CHOOSING
  //const button = document.getElementById('btn');
  //button.addEventListener('click', chooseSentence);

  //using both these seems to get the behaviour I want
  try{

    const optionList = document.getElementById('sel_split');
    //optionList.addEventListener('focus', chooseSentence);
    optionList.addEventListener('change', chooseSentence);


    //SELECTING
    //Have textArea listen for an event to indicate text has been selected
    const textArea = document.getElementById('sentencetextarea');
    //textArea.addEventListener('mouseup', selectText, false);
    textArea.addEventListener('mouseup', splitText, false);
  	textArea.addEventListener('mouseup', enableSplit, false);

    //SENDING DATA
    const splitButton = document.getElementById('split');
    splitButton.addEventListener('click', printSavedValues);

  }catch(err){
    console.error(err.name + err.message);
  }

}
