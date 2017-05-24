/*
 Joel Gruselius | 2015-09

 (Google Apps script)

 Script for listing sheet names where a string is found.
 Used to list all sheets (of a defined format) where a user ID
 is present along with a valid date.

 The refresh function must be used to work around Google's
 caching of return values of custom functions.
*/

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++80

/**
 * @OnlyCurrentDoc
 */

var EDITORS = [];
var MAX_ROWS = 100;

function onInstall() {
  onOpen();
}

/* Add a menu with custom functions */
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu("Licenses")
    .addItem("Refresh now", "refreshLastUpdate")
    .addItem("Search","searchPrompt")
    .addItem("Add method", "addMethodDialog")
    .addItem("Remove method", "removeMethodDialog")
    .addItem("Show incomplete entries", "getIncomplete")
    .addItem("Show instructions", "showHelpPanel")
      .addToUi();
  copyAndTranspose();
}

function showHelpPanel() {
  var html = "<title>Instructions</title> <style> div {padding: 1.2em; font-family: Helvetica, Arial; font-size: 0.7em; } li {margin-bottom: 4px; } </style> <div> <h3>To issue licences</h3> <ol> <li>Locate the sheet for the instrument or method in question</li> <li>Make sure any previous licenses for the user has been revoked (see below) by searching (CTRL+F or &#8984;+F)</li> <li>Add the username of the licensee on a new row, this is the scilifelab email account username of format first.lastname</li> <li>Add the username of the person who has trained the licensee</li> <li>Sign the instrument responsible signature column to attest that the user has been trained</li> <li>Sign the QA manager signature column</li> <li>Add an issue date</li> </ol> <h3>To revoke license</h3> <ol> <li>Add a revoke date to the revoke date column</li> <li>Sign the revoke date signature column</li> </ol> <h3>To add an instrument or method</h3> <ol> <li>Select <b>Licenses &rsaquo; Add method</b> from the menu bar and enter the method name in the dialog window. The name must be unique.</li> </ol> <h3>To list licenses for an instrument or method</h3> <ol type=\"a\"> <li>View the <b>All Licenses</b> sheet for a list of all users with licenses for each instrument with user names in rows</li> <li>View the <b>All Licenses (T)</b> for the same as above but with user names in columns (use <b>Licenses &rsaquo; Refresh now</b> to update)</li> </ol> <h3>To list licenses for a particular user</h3> <ol> <li>Select <b>Licenses &rsaquo; Search</b> from the menu bar and enter the user in the dialog window. Use the format <code>firstname.lastname</code></li> </ol> <h3>To withdraw an instrument or method</h3> A new document version needs to be written and validated. </font></div>";
  SpreadsheetApp.getUi().showSidebar(HtmlService.createHtmlOutput(html).setTitle("Instructions"));
}

/* Some sheets, e.g. instructions, should be excluded in many operations */
function isMethod(sheet) {
  var name = sheet.getName();
  return !(name.search("All Licenses") >= 0 || name.search("Instructions") >= 0 || name.search("Search") >= 0);
}

/* Check if the logged in user is an editor */
function isEditor() {
  var user = Session.getActiveUser().getEmail();
  return EDITORS.indexOf(user) >= 0;
}

/* Indicate that the spreadsheet has been changed since last refresh */
function onEdit(e) {
  var range = e.source.getRangeByName("Search user!refreshDate");
  var refreshDate = new Date(range.getValue().toString());
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
    var t0 = new Date();
    var result = getLicenses(query, null, "\n");
    var delta = new Date() - t0;
    ui.alert("Search result for "+query, result, ui.ButtonSet.OK);
  }
}

/* Update the refresh date text and methos lists */
function refreshLastUpdate() {
  var range = SpreadsheetApp.getActiveSpreadsheet()
    .getRangeByName("Search user!refreshDate");
  range.setValue(new Date());
  range.setBackground("white");
  range = SpreadsheetApp.getActiveSpreadsheet()
    .getRangeByName("searchResult");
  range.setFormula('=IF(REGEXMATCH($A$3,"^\w+\.\w+$"),getLicenses($A$3,$B$1),"Enter a valid user name")');
  updateMethodList();
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

/* Set the columns of the overview sheet to match the list of
 * method sheets
 */
function updateMethodList() {
  var sheet = SpreadsheetApp.getActive().getSheetByName("All Licenses");
  var sheetList = SpreadsheetApp.getActive().getSheets();
  var nameList = [];
  for(var i in sheetList) {
    var s = sheetList[i];
    if(isMethod(s)) {
      nameList.push(s.getName());
    }
  }
  var n = sheet.getMaxColumns();
  var range = sheet.getRange(1, 1, 1, n);
  range.clearContent();
  var d = n - nameList.length;
  // Delete or add columns as neccessary:
  if(d > 0) {
    sheet.deleteColumns(nameList.length+1, d);
  } else if(d < 0) {
    sheet.insertColumnsAfter(n, -d);
    // Copy format to the added columns:
    for(var i=1; i<=(-d); i++) {
      range = sheet.getRange(1, n);
      var newCol = sheet.getRange(1, n+i);
      range.copyTo(newCol);
      range = range.offset(1, 0);
      newCol = newCol.offset(1, 0);
      range.copyTo(newCol);
    }
  }
  range = sheet.getRange(1, 1, 1, nameList.length);
  range.setValues([nameList]);
}

/**
 * Return a comma-separated string of all the sheet names where
 * the specified userName string was found together with a valid
 * issue date. Search only sheets with string "Username" in cell A1.
 *
 * @param {string} userName The string to search for.
 * @param {object} dummyVar To work around return value caching.
 * @param {string} sep Separator between hits in result string.
 * @customfunction
 */
function getLicenses(userName, dummyVar, sep) {
  if(typeof sep === "undefined") var sep = ",";
  // Column in sheet with user ID, QA manager signature
  // and issue/revoke dates starting from 0:
  var USER_COL = 0;
  var SIGN_COL = 3;
  var ISSUE_COL = 4;
  var REVOKE_COL = 5;
  var maxCol = Math.max(USER_COL,SIGN_COL,ISSUE_COL,REVOKE_COL) + 1;

  var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();
  var licenseList = [];

  for(var i in sheets) {
    var sheet = sheets[i];
    var data  = sheet.getSheetValues(1, 1, 1, 1);
    if(data[0][0] === "Username") {
      data = sheet.getSheetValues(2, 1, sheet.getLastRow(), maxCol);
      for(var j in data) {
        var userId = data[j][USER_COL].toString();
        if(userId === userName) {
          var error = null;
          var sign = data[j][SIGN_COL].toString().trim();
          var issueDate = new Date(data[j][ISSUE_COL].toString());
          var revokeDate = data[j][REVOKE_COL].toString();
          if(!sign) {
            error = "MISSING SIGNATURE";
          } else if(!issueDate || !isFinite(issueDate)) {
            error = "DATE ERROR";
          } else if(!!revokeDate) {
            revokeDate = new Date(revokeDate);
            if(!isFinite(revokeDate)) {
              error = "DATE ERROR";
            }
          }
          if(error) {
            licenseList.push(error + "__" + sheet.getName());
          } else if(issueDate > revokeDate) {
            licenseList.push(sheet.getName());
            break;
          }
        }
      }
    }
  }
  return licenseList.length ? licenseList.join(sep) : "No valid entries found for "+userName;
}

/* Prompt for a method name and add if unique and user as permissions */
function addMethodDialog() {
  var ui = SpreadsheetApp.getUi();
  var response;
  if(!isEditor()) {
    response = "You do not have the permission to add methods.";
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
  var HEADER = ["Username", "Trainer", "Responsible signature",
      "QA manager signature", "Issue date", "Revoke date", "Revoke signature"];
  var row = ss.getSheetByName("All Licenses").getRange("A1:1").getValues()[0];
  if(ss.getSheetByName(name) !== null || row.indexOf(name) > -1) {
    return false;
  } else {
    var sheet = ss.insertSheet(name, ss.getNumSheets()+1);
    var range = sheet.getRange("A1:G1");
    range.setValues([HEADER]);
    range = sheet.getRange("E2:F").setNumberFormat("yyyy-MM-dd");
    trimSheet(sheet);
    protectSheet(sheet);
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

function removeMethodDialog() {
  var ui = SpreadsheetApp.getUi();
  var ss = SpreadsheetApp.getActive();
  var sheet = ss.getActiveSheet();
  var name = sheet.getName();
  if(!isEditor()) {
    ui.alert("You do not have the permission to remove methods.", ui.ButtonSet.OK);
  } else {
    if(!isMethod(sheet)) {
      ui.alert("You cannot remove " + name, ui.ButtonSet.OK);
    } else {
      var response = ui.alert("Remove method",
                             "Do you want to remove " + name + "?",
                             ui.ButtonSet.OK_CANCEL);
      if(response === ui.Button.OK) {
        ss.deleteSheet(sheet);
        sheet = ss.getSheetByName("All Licenses");
        var vals = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues();
        var col = vals[0].indexOf(name);
        sheet.deleteColumn(col+1);
        refreshLastUpdate();
        ui.alert("Removal successful", name + " was removed.", ui.ButtonSet.OK);
      }
    }
  }
}

function protectSheet(sheet) {
  var reset = (function(range) {
    var p = range.protect();
    p.removeEditors(p.getEditors());
    p.addEditors(EDITORS);
    return p;
  });
  var range = sheet.getRange(1, 1, 1, sheet.getMaxColumns());
  reset(range).setDescription("Protected header");
  range = sheet.getRange(2, 4, sheet.getMaxRows(), 2);
  reset(range).setDescription("Protected columns");
  Logger.log("Added editors " + EDITORS.join(", ") + " to " + sheet.getName());
}

function resetProtections() {
  var ss = SpreadsheetApp.getActive();
  var sheets = ss.getSheets();
  for(var i in sheets) {
    var s = sheets[i];
    if(!isMethod(s)) {
      Logger.log("Skipping " + s.getName());
    } else {
      var protections = s.getProtections(SpreadsheetApp.ProtectionType.RANGE);
      for(var i in protections) {
        protections[i].remove();
      }
      protectSheet(s);
    }
  }
}

/**
 * Use this to update the WIP spreadsheet with data from the
 * current, in use spreadsheet (paste the correct ID on the 1st line):
 */
function updateData() {
  var id = null;
  var ssOld = SpreadsheetApp.openById(id);
  var ssNew = SpreadsheetApp.getActive();
  if(ssOld) {
    var sheetsOld = ssOld.getSheets();
    var sheetsNew = ssNew.getSheets();
    for(var i in sheetsOld) {
      var name = sheetsOld[i].getName();
      if(!isMethod(sheetsOld[i])) {
        Logger.log("Skipping " + name);
      } else {
        var newSheet = ssNew.getSheetByName(name);
        while(newSheet === null) {
          Logger.log(name + " was not found in new, creating a new method...");
          addMethod(name);
          newSheet = ssNew.getSheetByName(name);
        }
        Logger.log("Found " + name + " in both, copying data...");
        newSheet.getDataRange().clearContent();
        var rangeOld = sheetsOld[i].getDataRange().offset(1, 0);
        var rangeNew = newSheet.getRange(2,1,rangeOld.getNumRows(),rangeOld.getNumColumns());
        rangeNew.setValues(rangeOld.getValues());
        rangeNew = newSheet.getRange(1,1, 1, 7);
        rangeNew.setValues([["Username", "Trainer", "Responsible signature",
                             "QA manager signature", "Issue date", "Revoke date", "Revoke signature"]]);
      }
    }
  } else {
    Logger.log("Spreadsheet with ID="+id+" could not be opened.");
  }
}

function getIncomplete() {
  // Column in sheet with user ID, QA manager signature
  // and issue/revoke dates starting from 0:
  var COLS = {
    USER: 0,
    TR_SIGN: 1,
    RE_SIGN: 2,
    QA_SIGN: 3,
    ISSUE_DATE: 4,
    REVOKE_DATE: 5,
    REVOKE_SIGN: 6
  };
  var maxCol = 1;
  for(var c in COLS) {
    if(COLS[c] >= maxCol) maxCol = COLS[c]+1;
  }

  var sheets = SpreadsheetApp.getActive().getSheets();
  var licenseList = [];
  var errors = [];
  for(var i in sheets) {
    var sheet = sheets[i];
    var data  = sheet.getSheetValues(1, 1, 1, 1);
    if(data[0][COLS.USER] === "Username") {
      var sheetName = sheet.getName();
      data = sheet.getSheetValues(2, 1, sheet.getLastRow(), maxCol);
      for(var j in data) {
        var row = data[j];
        var userId = row[COLS.USER];
        if(userId) {
          if(!row[COLS.TR_SIGN]) errors.push(sheetName + ": Trainer signature missing for " + userId);
          if(!row[COLS.RE_SIGN]) errors.push(sheetName + ": Responsible signature missing for " + userId);
          if(!row[COLS.QA_SIGN]) errors.push(sheetName + ": QA manager signature missing for " + userId);
          if(!row[COLS.ISSUE_DATE]) errors.push(sheetName + ": Issue date missing for " + userId);
          if(row[COLS.REVOKE_DATE].toString() && !row[COLS.REVOKE_SIGN]) errors.push(sheetName + ": Revoke signature missing for " + userId);
          if(row[COLS.REVOKE_SIGN] && !row[COLS.REVOKE_DATE].toString()) errors.push(sheetName + ": Revoke date missing for " + userId);
        }
      }
    }
  }
  var result = errors.length ? errors.join("\n") : "No errors found.";
  var ui = SpreadsheetApp.getUi();
  ui.alert("Missing info scan results", result, ui.ButtonSet.OK);
}

// Remove unused cols and rows so we don't reach Spreadsheet's limit so quickly:
function trimSheet(sheet) {
  var lastCol = sheet.getLastColumn();
  var maxCol = sheet.getMaxColumns();
  var maxRow = sheet.getMaxRows();
  if(maxCol > lastCol) {
    sheet.deleteColumns(lastCol+1, maxCol-lastCol);
  }
  if(maxRow > 100) {
    sheet.deleteRows(101, maxRow-100);
  }
}

function trimSheets() {
  var ss = SpreadsheetApp.getActive();
  var sheets = ss.getSheets();
  for(var i in sheets) {
    var s = sheets[i];
    if(!isMethod(s)) {
      Logger.log("Skipping " + s.getName());
    } else {
      trimSheet(s);
    }
  }
}
