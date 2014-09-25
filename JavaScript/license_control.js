/* 
 Joel Gruselius | 2014-04-09

 (Google Apps script)

 Script for listing sheet names where a string is found.
 Used to list all sheets (of a defined format) where a user ID
 is present along with a valid date.
 
 The refresh function must be used to work around Google's
 caching of return values of custom functions.
*/

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++80

/* Add a menu with custom functions */
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu("Licenses")
    .addItem("Refresh now", "refreshLastUpdate")
    .addItem("Search","searchPrompt")
      .addToUi();
  copyAndTranspose();
}

/* Indicate that the spreadsheet has been changed since last refresh */
function onEdit() {
  var range = SpreadsheetApp.getActiveSpreadsheet()
    .getRangeByName("refreshDate");
  var refreshDate = new Date(range.getValue());
  if(refreshDate < new Date()) {
    range.setBackgroundRGB(255, 214, 0);
  }
}

/* Prompt for a name to search for and display the results in a dialog box */
function searchPrompt() {
  var ui = SpreadsheetApp.getUi();
  var prompt = ui.prompt("Search for user",
                         "Enter the user name to search for:",
                        ui.ButtonSet.OK_CANCEL);
  var query = prompt.getResponseText();
  if(prompt.getSelectedButton() === ui.Button.OK) {
    var result = getLicenses(query, null) || "No valid entries found";
    ui.alert("Search result for "+query, result, ui.ButtonSet.OK);
  }
}

/* Update the refresh date text and transposed list */
function refreshLastUpdate() {
  var range = SpreadsheetApp.getActiveSpreadsheet()
    .getRangeByName("Search user!refreshDate");
  range.setValue(new Date());
  range.setBackground("white");
  copyAndTranspose();
}

/* Transpose the data in the summary list and copy to another sheet */
function copyAndTranspose() {
  var s = SpreadsheetApp.getActiveSpreadsheet();
  var a = s.getSheetByName("All Licenses").getDataRange().getValues();
  var t = a[0].map(function(col, i) { 
    return a.map(function(row) { 
      return row[i];
    });
  });
  s.getSheetByName("All Licenses (T)").clearContents()
    .getRange(1,1,t.length,t[0].length).setValues(t);
}

/*
 Return a comma-separated string of all the sheet names where
 the specified userName string was found together with a valid 
 issue date. Search only sheets with string "Username" in cell A1:
*/
function getLicenses(userName, dummyVar) {
  // Column in sheet with user ID, QA manager signature
  // and issue/revoke dates:
  var USER_COL   = 1;
  var SIGN_COL   = 4;
  var ISSUE_COL  = 5;
  var REVOKE_COL = 6;
  
  var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();
  var licenseList = [];
  
  for(var i in sheets) {
    var sheet = sheets[i];
    var data  = sheet.getRange(1, 1).getValues();
    if(data[0][0] === "Username") {
      data = sheet.getRange(2, 1, sheet.getLastRow(), sheet.getLastColumn())
        .getValues();
      for(var j in data) {
        var userId = data[j][USER_COL-1];
        var sign = data[j][SIGN_COL-1];
        var issueDate = new Date(data[j][ISSUE_COL-1]);
        var revokeDate = new Date(data[j][REVOKE_COL-1]);
        var valid = (userId === userName) && sign && isFinite(issueDate)
          && (!isFinite(revokeDate) || issueDate > revokeDate);
        if(valid) {
          licenseList.push(sheet.getName());
          break;
        }
      }
    }
  }
  return licenseList.join();
}