/*
 Joel Gruselius, 2012

 Searches for and returns a value from the preset spreadsheet. Parameters:
 	sampleId (string): Find the row with this string in column 1
 	runId (string): The name of the sheet
 	columnIndex (int): The column number
 I.e. the function will search sheet 'runId' for the row with 'sampleId'
 in column 1 and return the value in column 'columnIndex' of that row.
*/

function demultiplexLookup(sampleId, runId, columnIndex) {
	// Open the spreadsheet (openById should throw an exception if 
	// the spreadsheet with the given ID is not found):
	var fileKey = "0Av062T6cLrjbdDQtZmp5cThiMzEtd25MWDhfaDltSUE";
	var ss = SpreadsheetApp.openById(fileKey);
	// Find the correct sheet:
	var sheet = ss.getSheetByName(runId);
	if(sheet === null) { throw "MissingSheetException"; }
	// Find the column with the 'Sample name' header:
	var range = sheet.getRange(1, 1, 1, sheet.getLastColumn());
	var arr = range.getValues();
	var lookUpColumn;
	for(var i = 0, n = arr[0].length; i < n; i++) {
		if(arr[0][i] == "Sample name") {
			lookUpColumn = i;
			break;
		}
	}
	if(typeof lookUpColumn === "undefined") { throw "MissingHeaderValueException"; }
	// Find the row with 'sampleId':
	var lookUpRow;
	range = sheet.getRange(1, lookUpColumn+1, sheet.getLastRow(), 1);
	arr = range.getValues();
	for(var i = 0, n = arr.length; i < n; i++) {
		if(arr[i][0] == sampleId) {
			lookUpRow = i;
			break;
		}
	}
	if(typeof lookUpRow === "undefined") { throw "MissingSampleIdValueException"; }
	range = sheet.getRange(lookUpRow+1, columnIndex, 1, 1);
	return range.getValue();
}