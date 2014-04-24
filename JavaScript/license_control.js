/* 
 Joel Gruselius | 2014-04-09

 (Google Apps script)

 Script for listing sheet names where a string is found.
 Used to list all sheets (of a defined format) where a user ID
 is present along with a valid date.
 
 The refresh function must be used to work around Google's
 caching of return values of custom functions.
*/

/* Add menu entry for refresh function */
function onOpen() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  var entries = [{name: "Refresh now", functionName: "refreshLastUpdate"}];
  sheet.addMenu("Refresh", entries);
}

/* Indicate that the spreadsheet has been changed since last refresh */
function onEdit() {
  var range = SpreadsheetApp.getActiveSpreadsheet().getRangeByName("refreshDate");
  var refreshDate = new Date(range.getValue());
  if(refreshDate < new Date()) {
    range.setBackgroundRGB(255, 214, 0);
  }
}

/* Update the refresh date text */
function refreshLastUpdate() {
  var range = SpreadsheetApp.getActiveSpreadsheet().getRangeByName("refreshDate");
  range.setValue(new Date());
  range.setBackground("white");
}

/*
 Return a comma-separated string of all the sheet names where
 the specified userName string was found together with a valid 
 issue date. Search only sheets with string "Username" in cell A1:
*/
function getLicenses(userName, dummyVar) {
  // Column in sheet with user ID and issue/revoke dates:
  var USER_COL   = 1;
  var ISSUE_COL  = 2;
  var REVOKE_COL = 6;
  
  var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();
  var licenseList = [];
  
  for(var i in sheets) {
    var sheet = sheets[i];
    var data  = sheet.getRange(1, 1).getValues();
    if(data[0][0] === "Username") {
      data = sheet.getRange(2, 1, sheet.getLastRow(), sheet.getLastColumn()).getValues();
      for(var j in data) {
        var userId     = data[j][USER_COL-1];
        var issueDate  = new Date(data[j][ISSUE_COL-1]);
        var revokeDate = new Date(data[j][REVOKE_COL-1]);
        var valid      = (userId === userName && isFinite(issueDate) && !isFinite(revokeDate));
        if(valid) {
          licenseList.push(sheet.getName());
          break;
        }
      }
    }
  }
  return licenseList.join();
}