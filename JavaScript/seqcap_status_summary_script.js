/*
 Joel Gruselius 2012.04

 (Google Apps script)

 ~~Description~
*/

function onEdit(e) {
  // Print (replace) date and user ID of every change:
  var sheet = e.source.getSheetByName("list");
  if(sheet) {
    var range = sheet.getRange("B1");
    range.setValue(new Date());
    range.setBackgroundColor("lightgrey");
    range = sheet.getRange("D1");
    var userId = e.user.getEmail().split("@")[0];
    range.setValue(userId);
    range.setBackgroundColor("lightgrey");
  } else {
    Browser.msgBox("ERROR: Could not find sheet \"list\".");
  }
  // Highlight cells edited in current session by background color:
  range = e.source.getActiveRange();
  range.setBackgroundColor("lightpink");
}

function onOpen(e) {
  // Clear any highlighting from last session:
  var sheets = e.source.getSheets();
  for(var i = 0, n = sheets.length; i < n; i++) {
    var sheet = sheets[i];
    sheet.getRange(1, 1, sheet.getMaxRows(), sheet.getMaxColumns()).setBackgroundColor("white");
  }
}

// string lookFor, string inColumn
function getFromProjectList(lookFor, inColumn) {
  
  // Check query 'lookFor':
  // Whether the matching should ignore case:
  var ignoreCase = true;
  // Determine if 'lookFor' is on project index form ('Pnnn' or nnn):
  // var pattern = (ignoreCase) ? /^(?:P)?(\d{3})$/i : /^(?:P)?(\d{3})$/;
  // Using lazy matching for the 'P'?
  var pattern = /\d{3}$/;
  var match = pattern.exec(lookFor);
  var lookForNumber = (match !== null);
  if(lookForNumber) lookFor = match[0];
  
  if(ignoreCase && typeof lookFor == "string" && !lookForNumber) lookFor = lookFor.toLowerCase();

  // Get the project list sheet:
  var ss = SpreadsheetApp.openById("0Aodhnv9MdaBidFhZT2NKNm0tU2c4Qm5qd0swX0JkUkE");
  var sheet = ss.getSheetByName("Ongoing");
  
  // Get the range to search for 'lookFor':
  var queryColumn = (lookForNumber) ? 2 : 3;
  var range = sheet.getRange(1, queryColumn, sheet.getLastRow(), queryColumn);
  var values = range.getValues();
  // Get the row index of the first cell matching 'lookFor':
  for(var i = 0, n = values.length; i < n; i++) {
    var value = values[i][0];
    if(ignoreCase && !lookForNumber) value = value.toLowerCase();
    if(value == lookFor) { 
      var queryRow = i;
      break;
    }
  }
  // Get the row containing column headers (1st row):
  range = sheet.getRange(1, 1, 1, sheet.getLastColumn());
  values = range.getValues();
  // Get the column index of the cell matching 'inColumn':
  if(ignoreCase) inColumn = inColumn.toLowerCase();
  var lookupColumn;
  for(var i = 0, n = values[0].length; i < n; i++) {
    value = (ignoreCase) ? values[0][i].toLowerCase() : values[0][i];
    if(value == inColumn) { 
      lookupColumn = i;
      break;
    }
  }
  // Get the value of the cell in the resulting row, column.
  // If either 'lookFor' or 'inColumn' wasn't found return an empty string:
  if(typeof queryRow === "undefined" || typeof lookupColumn === "undefined") {
    value = "";
  } else {
    range = sheet.getRange(queryRow+1, lookupColumn+1);
    value = range.getValue();
  }
  return value;
}

function findDocumentation(files, project) {
  var file = null;
  for(var i = 0, n = files.length; i < n; i++) {
    var pid = files[i].getName().match(/([A-Z]\.)?[A-Z]+_\d{2}_\d{2}/gi);
    if(pid && pid[0] === project) {
      file = files[i];
      break;
    }
  }
  if(file) Logger.log(file.getName());
  return file;
}

function makeLinks() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var range = sheet.getRange(1, 1, sheet.getLastRow(), 1);
  var data = range.getValues();
  
  var t0 = new Date();
  var fileList = DocsList.getFilesByType(DocsList.FileType.DOCUMENT);
  Logger.log("Files: "+fileList.length);
  Logger.log("DocsList.get: " + (new Date()-t0)/1000+" s")
  
  for(var i = 0, n = data.length; i < n ; i++) {
    var val = data[i][0];
    var pid = val.match(/([A-Z]\.)?[A-Z]+_\d{2}_\d{2}/gi);
    if(pid) {
      var doc = findDocumentation(fileList, pid[0]);
      if(doc) { 
        data[i][0] = "=HYPERLINK(\"" + doc.getUrl() + "\",\"" + val + "\")";
      }
    }
  }
  //range.setValues(data);
}

function testRegExp(pattern, str) {
  re = new RegExp(pattern);
  var match = re.exec(str);
  var result = (match != null) ? match[match.length-1] + " (" + match.length + ")" : "";
  return result;
}

function trimString(str) {
  return str.replace(/^\s\s*/, "").replace(/\s\s*$/, "");
}