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
    .addItem("Add method", "addMethodDialog")
      .addToUi();
  copyAndTranspose();
}

/* Indicate that the spreadsheet has been changed since last refresh */
function onEdit(e) {
  var range = e.source.getRangeByName("Search user!refreshDate");
  var refreshDate = new Date(range.getValue());
  if(refreshDate < new Date()) {
    range.setBackgroundRGB(255, 214, 0);
  }
  /*
  var html = "<code>" + e.changeType + " at " + e.range.getSheet().getName() + "!" +
    e.range.getA1Notation() + " by " + e.user.getEmail() + " (" +
    refreshDate.toLocaleString() + ")</code>";
  SpreadsheetApp.getUi().showSidebar(HtmlService.createHtmlOutput(html));
  */
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
    var data  = sheet.getSheetValues(1, 1, 1, 1);
    if(data[0][0] === "Username") {
      data = sheet.getSheetValues(2, 1, sheet.getLastRow(), sheet.getLastColumn());
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

/* Prompt for a name to search for and display the results in a dialog box */
function addMethodDialog() {
  var ui = SpreadsheetApp.getUi();
  var response;
  var editors = SpreadsheetApp.getActiveSpreadsheet()
    .getSheetByName("All Licenses").getSheetProtection().getUsers();
  var user = Session.getActiveUser().getEmail();
  if(editors.indexOf(user) < 0) {
    response = "You do not have the permission to add methods."
  } else {
    var prompt = ui.prompt("Add method",
      "Enter the name of the new method:",
      ui.ButtonSet.OK_CANCEL);
    var name = prompt.getResponseText().trim();
    if(prompt.getSelectedButton() === ui.Button.OK) {
      if(addMethod(name)) {
        response = "Successfully added method \"" + name + "\"";
      } else {
        response = "Method could not be created, the name " + name +
          " is already in use";
      }
    }
  }
  ui.alert("Add method", response, ui.ButtonSet.OK);
}

function addMethod(name) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var HEADER = ["Username", "Trainer", "Room responsible signature",
      "QA manager signature", "Issue date", "Revoke date", "Revoke signature"];
  var row = ss.getSheetByName("All Licenses").getRange("A1:1").getValues()[0];
  if(ss.getSheetByName(name) !== null || row.indexOf(name) > -1) {
    return false;
  } else {
    var sheet = ss.insertSheet(name, ss.getNumSheets()+1);
    var range = sheet.getRange("A1:G1");
    range.setValues([HEADER]);
    range = sheet.getRange("E2:F").setNumberFormat("yyyy-MM-dd");
    sheet = ss.getSheetByName("All Licenses");
    range = sheet.getRange(1,sheet.getMaxColumns());
    sheet.insertColumnAfter(sheet.getMaxColumns());
    newCol = sheet.getRange(1,sheet.getMaxColumns());
    range.copyTo(newCol);
    newCol.setValue(name);
    range = range.offset(1, 0);
    newCol = newCol.offset(1, 0);
    range.copyTo(newCol);
    return true;
  }
}
