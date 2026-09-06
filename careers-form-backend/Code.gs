/**
 * Code.gs — V3
 * Pillai & Sons — Careers form backend
 *
 * Handles three actions:
 *   apply  -> writes the application row, returns its row number
 *   resume -> saves ONE file to Drive and appends the link to that row
 *   (GET)  -> health check you can open in a browser
 *
 * Files are sent one request per file, so a big attachment can never blow up
 * the main submission. If a file fails, the application row is still saved.
 *
 * SETUP
 *   1. Sheet > Extensions > Apps Script
 *   2. Delete everything, paste this file, Save
 *   3. Run > setupSheet  (authorise when asked)
 *   4. Deploy > New deployment > Web app
 *        Execute as:     Me
 *        Who has access: Anyone          <-- must be "Anyone"
 *   5. Copy the /exec URL into careers.html
 *
 * AFTER ANY EDIT HERE: Deploy > Manage deployments > pencil >
 * Version: New version > Deploy.  Otherwise your change is not live.
 */

var SHEET_ID      = '1X7oDATxdpm1nnzK_jc7Su0k718QEk2wfKMnn7s0cWEU';
var SHEET_NAME    = 'Applications';
var RESUME_FOLDER = 'Pillai & Sons — Resumes';

var COLUMNS = [
  ['Timestamp',                                            'submittedAt'],
  ['For Which Position you want to apply for Job?',        'position'],
  ['Name',                                                 'name'],
  ['Mobile Number',                                        'mobile'],
  ['Age',                                                  'age'],
  ['Education Qualification?',                             'qualification'],
  ['Do you have Car Driving License?',                     'drivingLicense'],
  ['Are you Fresher or Experienced',                       'fresherOrExperienced'],
  ['Do you have experience in Car/Bike Sales or Service?', 'carBikeExperience'],
  ['In which City you want Job?',                          'jobCity'],
  ['Your Current living city/Town?',                       'currentCity'],
  ['Present Company Name',                                 'presentCompany'],
  ['Current Monthly Takehome Salary?',                     'currentSalary'],
  ['Expected Monthly Takehome Salary?',                    'expectedSalary'],
  ['Resume',                                               'resumeUrl']
];

var RESUME_COL = COLUMNS.length;   // last column

/* ------------------------------------------------------------------ */

function setupSheet() {
  var sheet = getSheet_();
  var headers = COLUMNS.map(function (c) { return c[0]; });
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length)
       .setFontWeight('bold').setBackground('#D5232B').setFontColor('#FFFFFF');
  sheet.setFrozenRows(1);
  sheet.autoResizeColumns(1, headers.length);
  Logger.log('Sheet ready: ' + headers.length + ' columns.');
}

function getSheet_() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  return ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
}

function getResumeFolder_() {
  var it = DriveApp.getFoldersByName(RESUME_FOLDER);
  return it.hasNext() ? it.next() : DriveApp.createFolder(RESUME_FOLDER);
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o))
                       .setMimeType(ContentService.MimeType.JSON);
}

/* ------------------------------------------------------------------ */

function doGet() {
  return json_({ result: 'ok', message: 'Careers endpoint live. Submit via POST.' });
}

function doPost(e) {
  try {
    var p = (e && e.parameter) ? e.parameter : {};
    var action = p.action || 'apply';
    if (action === 'resume') return handleResume_(p);
    return handleApply_(p);
  } catch (err) {
    return json_({ result: 'error', message: String(err && err.message || err) });
  }
}

/* --- 1. the application row --- */
function handleApply_(p) {
  var lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    var sheet = getSheet_();
    if (sheet.getLastRow() === 0) setupSheet();

    var row = COLUMNS.map(function (c) {
      var key = c[1];
      if (key === 'submittedAt') return p.submittedAt || new Date();
      if (key === 'resumeUrl')   return '';
      return p[key] || '';
    });

    sheet.appendRow(row);
    return json_({ result: 'success', row: sheet.getLastRow() });
  } finally {
    try { lock.releaseLock(); } catch (ignore) {}
  }
}

/* --- 2. one attachment --- */
function handleResume_(p) {
  if (!p.fileData) return json_({ result: 'error', message: 'No file data received.' });

  var rowIndex = parseInt(p.row, 10);
  if (!rowIndex || rowIndex < 2) {
    return json_({ result: 'error', message: 'Bad row reference.' });
  }

  var bytes = Utilities.base64Decode(p.fileData);
  var who   = String(p.applicant || 'Applicant').replace(/[^\w\s.-]/g, '').trim() || 'Applicant';
  var orig  = String(p.fileName || 'resume');
  var ext   = orig.indexOf('.') > -1 ? orig.split('.').pop() : 'pdf';
  var idx   = p.fileIndex ? (' (' + p.fileIndex + ')') : '';
  var name  = who + ' - ' + (p.mobile || '') + idx + '.' + ext;

  var blob = Utilities.newBlob(bytes, p.fileType || 'application/octet-stream', name);
  var file = getResumeFolder_().createFile(blob);
  file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
  var url = file.getUrl();

  var lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    var sheet = getSheet_();
    var cell  = sheet.getRange(rowIndex, RESUME_COL);
    var prev  = cell.getValue();
    cell.setValue(prev ? (prev + '\n' + url) : url);
  } finally {
    try { lock.releaseLock(); } catch (ignore) {}
  }

  return json_({ result: 'success', url: url });
}
