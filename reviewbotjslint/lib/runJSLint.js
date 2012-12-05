/*
 * Global function that serves as an interface between Review Bot JSLint tool
 * and jslint.js (the latter contains jslint itself).
 * Function does not return anything.
 * If jslint finds no errors in the file input, no output is generated.
 * When an error is found, this function prints to stdout a formatted string
 *  indicating the line number and column number of the error, along with the
 *  detailed error message. i.e.: lineNum:colNum:msg
 * Arguments:
 *  pathToJSLint    - full path to jslint.js, must be generated by caller
 *  fileContent     - entire content of the file to be jslinted as a string
 *  custom_options  - json containing user-specified options to be passed in to
 *                    jslint. E.g.: {'white' : 'True', 'evil' : 'False'...}
 */
function runJSLint(pathToJSLint, fileContent, custom_options) {
    load(pathToJSLint);

    var options = {};

    if (custom_options) {
        options = custom_options;
    }

    var result = JSLINT(fileContent, options);

    if (!result) {
        for (var i = 0; i < JSLINT.errors.length; i++) {
            if (JSLINT.errors[i]) {
                print(JSLINT.errors[i].line + ":" + JSLINT.errors[i].character +
                      ":" + JSLINT.errors[i].reason);
            }
        }
    }
}
