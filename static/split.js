/**
 * @file Provides functionality to allow a string to be split into to two pars.
 */

// WARNING: The code in this script file is NOT backwards-compatible with
// older browsers that do not support ES6/ECMAScript 2015. As such, this
// JS features for this program will likely not work in
// Safari: version < 10
// Chrome: version < 51
// Firefox: version < 54
// Source: https://www.w3schools.com/js/js_versions.asp

{ // Use EC6 block scope to prevent namespace conflicts with other JS files
  // possible loading in same page

  //============================= MAIN ========================================

  // Bind event handler functions to events on loading of page.
  try {

    // Display sentence in text area once user has selected one.
    const optionList = document.getElementById('sel_split');
    optionList.addEventListener('change', chooseSentence);

    // Check whether split can at happen in place chosen by user; if so, do it.
    const textArea = document.getElementById('sentencetextarea');
    textArea.addEventListener('mouseup', splitText, false);
    textArea.addEventListener('mouseup', enableSplit, false);

    // For debugging purposes only; comment out the printSavedValues below
    // to debug.
    // const splitButton = document.getElementById('split');
    // splitButton.addEventListener('click', printSavedValues);

  } catch (err) {
    console.error(err.name + err.message);
  }

  //============================ FUNCTIONS ====================================

  /**
   * Resets text area and parts' areas when new sentence selected; prevents
   * user from submitting the Split form.
   */
  function resetValues() {
    // Text area where selected sentence displayed.
    const outputArea = document.getElementById('output_area');

    // Elements where the two parts of a split sentence are shown.
    let firstPart = document.getElementById('first_part').value;
    let secondPart = document.getElementById('second_part').value;

    // Clear elements of any pre-existing text.
    outputArea.innerHTML = "";
    firstPart = "";
    secondPart = "";

    // Ensure split submission doesn't happen until user has actually chosen
    // a split point.
    const splitButton = document.getElementById('split');
    splitButton.disabled = true;
  }

  /**
   * Displays chosen sentence in text area.
   */
  function chooseSentence() {
    // Clear output areas every time a new sentence has been selected.
    resetValues();

    // Get list of options from sentence drop-down list
    let selectElement = document.getElementById('sel_split');
    const options = selectElement.options;

    // Get drop-down list index of chosen sentence
    let indexOfSentenceToSplit = selectElement.selectedIndex;

    // Display selected sentence in textarea
    // Leading/trailing spaces aren't necessary; make text weird to look at.
    let splitTextArea = document.getElementById('sentencetextarea');
    splitTextArea.innerHTML = options[indexOfSentenceToSplit].value.trim();

    // Save index of chosen sentence from sentence list in input element.
    // Careful here: the saved value is the index that will be used
    // to access the sentence from sentences list in the web script.
    // Because the way the option list is presented in results.html
    // with a 'placeholder' first option, indexOfSentenceToSplit needs to be
    // decremented by 1.
    const inputIndexElem = document.getElementById('sent_index');
    inputIndexElem.value = indexOfSentenceToSplit - 1;
  }

  /**
   * Splits chosen sentence into two parts; displays preview of what split will
   * look like.
   */
  function splitText() {
    // Fetches the element that is clicked on by cursor
    const activeTextArea = document.activeElement;

    // Only makes sense to do a split if there's something in the field.
    if (activeTextArea.value.trim().length === 0) {
      return;
    }

    // let selection = ""

    // Check that the active element is the text area and not some other
    // element.
    if (activeTextArea.id === 'sentencetextarea') {

      // Get the full sentence in the sentence area.
      let text = activeTextArea.value;

      // The selectionStart and selectionEnd methods allow us to get the
      // the positions of the cursor at the beginning and end of a highlighted
      // substring of text.
      let start = activeTextArea.selectionStart;
      let end = activeTextArea.selectionEnd;

      // Area where preview of split parts will be displayed.
      let outputArea = document.getElementById('output_area');

      // We only want to do a split at the position in the sentence where the
      // user clicks. This conditonal expression we only process for that event
      // and ignore whatever else the user might do in the text area.
      if (start === end) {
        // Get the substrings representing the two parts of the split sentence.
        let firstPart = text.slice(0, start);
        let secondPart = text.slice(start, text.length);

        // Get rid of leading/trailing whitespaces. Not necessary.
        firstPart = firstPart.trim();
        secondPart = secondPart.trim();

        // Display parts to user so long as they're not empty or full of
        // whitepace characters; no point in saving them either.
        if (firstPart.length !== 0 && secondPart.length !== 0) {
          outputArea.style.fontStyle = "normal";

          outputArea.innerHTML = "PART 1\n------\n" + firstPart + "\n\n" +
                                 "PART 2\n------\n" + secondPart;

        } else {
          outputArea.style.fontStyle = "italic";
          outputArea.innerHTML =
              "Nothing to split. Please pick a split point " +
              "within the sentence, not on its edges."
        }

        // Save caret position (i.e. where text will be split) so it can be used
        // by the server-side script.
        const inputSplitPosition = document.getElementById('split_pos');
        inputSplitPosition.value = start;

        // Save first and last parts of split sentence for the server-side
        // script.
        const inputFirstPart = document.getElementById('first_part');
        const inputSecondPart = document.getElementById('second_part');
        inputFirstPart.value = firstPart;
        inputSecondPart.value = secondPart;
      }
    }

    // For debugging purposes only.
    // printSavedValues();
  }

  /**
   * Allows split only if textarea is not empty and neither split part is purely
   * whitespace characters.
   */
  function enableSplit() {
    // Fetch submit button and text area where chosen sentence appears.
    const splitButton = document.getElementById('split');
    const textArea = document.getElementById('sentencetextarea');

    // If a sentence has been chosen, then text area won't be empty. Otherwise,
    // it is empty, and the submit button should be greyed out.
    if (textArea.value != "") {

      let firstPart = document.getElementById('first_part').value;
      let secondPart = document.getElementById('second_part').value;

      // Remove leading, trailing whitespaces.
      firstPart = firstPart.trim();
      secondPart = secondPart.trim();

      // Don't let the submit button work if the parts are empty strings!
      if (firstPart.length !== 0 && secondPart.length !== 0) {
        splitButton.disabled = false;
      } else {
        splitButton.disabled = true;
      }
    } else {
      splitButton.disabled = true;
    }
  }

  // // Save index, full sentence.
  // function printSavedValues(){
  // 	const index = document.getElementById('sent_index').value;
  //   const first = document.getElementById('first_part').value;
  //   const second = document.getElementById('second_part').value;
  //   const splitPos = document.getElementById('split_pos').value;
  //
  //   const savedValues = `index = ${index}\nfirst = ${first}\nsecond =
  //   ${second}\nsplitPos = ${splitPos}`
  //
  //   const savedValTextArea = document.getElementById('saved');
  //   savedValTextArea.innerHTML = savedValues;
  //
  // }
}
