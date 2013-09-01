function trimString(str) {
  return str.replace(/^\s\s*/, "").replace(/\s\s*$/, "");
}

function rangeToArray(sheet, fromRow, fromColumn, toRow, toColumn) {
	return sheet.getRange(fromRow, fromColumn,
		toRow-fromRow+1, toColumn-fromRow+1).getValues();
}

function spreadsheetLookup(spreadSheetId, sheetName, queryColumn, queryValue,
	returnColumn) {
	// Open the spreadsheet (should throw an exception if not found):
	var ss = SpreadsheetApp.openById(spreadSheetId);
	// Find the correct sheet:
	var sheet = ss.getSheetByName(sheetName);
	if(sheet === null) { throw "MissingSheetException"; }
	// If 'queryColumn' is a string, assume it is the header of the column
	// to search for 'queryValue', otherwise assume it is the column index:
	var arr;
	var lookUpColumn;
	if(typeof queryColumn === "string") {
		arr = rangeToArray(sheet, 1, 1, 1, sheet.getLastColumn());
		for(var i = 0, n = arr[0].length; i < n; i++) {
			if(arr[0][i] == queryColumn) {
				lookUpColumn = i;
				break;
			}
		}
	} else {
		lookUpColumn = queryColumn - 1;
	}
	if(typeof lookUpColumn === "undefined") { throw "MissingHeaderValueException"; }
	// Find the row with 'sampleId':
	var lookUpRow;
	arr = rangeToArray(sheet, 1, lookUpColumn+1, sheet.getLastRow(), lookUpColumn+1);
	for(var i = 0, n = arr.length; i < n; i++) {
		if(arr[i][0] == sampleId) {
			lookUpRow = i;
			break;
		}
	}
	if(typeof lookUpRow === "undefined") { throw "MissingSampleIdValueException"; }
	// If 'returnColumn' is a string, assume it is the header of the column
	// where the value to return resides, otherwise assume it is the column index:
	var column;
	if(typeof returnColumn === "string") {
		arr = rangeToArray(sheet, 1, 1, 1, sheet.getLastColumn());
		for(var i = 0, n = arr[0].length; i < n; i++) {
			if(arr[0][i] == returnColumn) {
				column = i;
				break;
			}
		}
	} else {
		column = returnColumn - 1;
	}
	range = sheet.getRange(lookUpRow+1, column+1, 1, 1);
	var value = range.getValue();
	return value;
}