/*
 Joel Gruselius 2014.05
 
 (Google Apps script)

 This script searches the folder given by the key below for all filenames
 containing the strings in the cells defined in the 'monitor' range. Strings
 not matching the format 'J.Doe_14_01' are ignored.
 The names of all new matching files are emailed to the user running the script.
 Use a time trigger to run e.g. every hour.
*/

var FOLDER_ID = "0B_062T6cLrjbM2IwZWI5MDctMTZkYi00N2JiLThmZTEtZDJiN2IxNDI4ZDFm";

function run() {
  try {
    var updates = filterNew(getFiles());
    if(updates.length > 0) {
      ScriptDb.getMyDb().saveBatch(updates, false);
      var names = updates.map(function(x) {
        return "<a href=\"" + x.url + "\">" + x.name + "</a> (" + x.created + ")";
      });
      var body = "The following monitored files have been added to \"" +
                 DocsList.getFolderById(FOLDER_ID).getName() +
                 "\":\n\n" +
                 names.join("\n");
      MailApp.sendEmail({
        to: Session.getActiveUser().getEmail(),
        name: "Google Drive folder monitor",
        noReply: true,
        subject:"Folder monitor update",
        htmlBody: body
      });
    }
  } catch(e) {
    MailApp.sendEmail("joel.gruselius@scilifelab.se", "Google Apps script error", e.message);
  }
}

function notInDb(file) {
  return ScriptDb.getMyDb().query(file).getSize() < 1;
}

function getMonitored() {
  var values = SpreadsheetApp.getActive().getRangeByName("monitor").getValues();
  var nameList = [];
  for(var i in values) {
    var name = values[i][0];
    if(name.match(/[A-Z]\.[A-Za-z]+_\d\d_\d\d/)) nameList.push(name);
  }
  return nameList;
}

function getFiles() {
  var folder = {};
  folder.obj = DocsList.getFolderById(FOLDER_ID);
  folder.files = folder.obj.getFiles();
  var monList = getMonitored();
  folder.monitored = folder.files.filter(function(x) {
    var match = x.getName().match(/[A-Z]\.[A-Za-z]+_\d\d_\d\d/);
    return !!match && monList.indexOf(match[0]) > -1;
  });
  var files = folder.monitored.map(function(x) { 
    return {"name":x.getName(), "id":x.getId(), "created":x.getDateCreated().toLocaleString(),
            "url":x.getUrl(), "folder":FOLDER_ID, "type":"file"};
  });
  Logger.log(files);
  return files;
}

function filterNew(files) {
  return files.filter(notInDb);
}

function deleteAll() {
  var db = ScriptDb.getMyDb();
  while (true) {
    var result = db.query({});
    if (result.getSize() == 0) {
      break;
    }
    while (result.hasNext()) {
      db.remove(result.next());
    }
  }
}

function initialize() {
  var hourTrigger = ScriptApp.newTrigger("run").timeBased().everyHours(1).create();
  SpreadsheetApp.getActive().toast("Hourly trigger set, ID: " + hourTrigger.getUniqueId(), "Install");
}

function deactivate() {
  var triggers = ScriptApp.getProjectTriggers();
  for(var i in triggers) ScriptApp.deleteTrigger(triggers[i]);
  deleteAll();
  SpreadsheetApp.getActive().toast("Database cleared and triggers removed", "Uninstall");
}

function onOpen() {
  SpreadsheetApp.getActive().addMenu("Monitor",
    [{name:"Install",functionName:"initialize"},
     {name:"Uninstall",functionName:"deactivate"},
     {name:"Run now",functionName:"run"}]);
}
