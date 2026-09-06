/**
 * Code.gs — V2
 * Pillai & Sons — Careers form backend
 *
 * Columns match the Google Form "JOB APPLICATION FOR 20 CITIES" exactly.
 * Receives POSTs from careers.html, saves any attached resume to Drive,
 * and appends one row per application to the Google Sheet.
 *
 * SETUP — see README-CAREERS.md
 *   1. Open your sheet:
 *      https://docs.google.com/spreadsheets/d/1X7oDATxdpm1nnzK_jc7Su0k718QEk2wfKMnn7s0cWEU/edit
 *   2. Extensions > Apps Script
 *   3. Delete anything there, paste this whole file, Save
 *   4. Run > setupSheet   (creates the header row; authorise when asked)
 *   5. Deploy > New deployment > Web app
 *        Execute as:       Me
 *        Who has access:   Anyone
 *      Copy the /exec URL into careers.html
 */

var SHEET_ID     = '1X7oDATxdpm1nnzK_jc7Su0k718QEk2wfKMnn7s0cWEU';
var SHEET_NAME   = 'Applications';
var RESUME_FOLDER = 'Pillai & Sons — Resumes';   // created automatically in your Drive

/* Column order. First value = sheet header, second = form field name.
   These mirror the Google Form questions, in the same order. */
var COLUMNS = [
  ['Timestamp',                                       'submittedAt'],
  ['For Which Position you want to apply for Job?',   'position'],
  ['Name',                                            'name'],
  ['Mobile Number',                                   'mobile'],
  ['Age',                                             'age'],
  ['Education Qualification?',                        'qualification'],
  ['Do you have Car Driving License?',                'drivingLicense'],
  ['Are you Fresher or Experienced',                  'fresherOrExperienced'],
  ['Do you have experience in Car/Bike Sales or Service?', 'carBikeExperience'],
  ['In which City you want Job?',                     'jobCity'],
  ['Your Current living city/Town?',                  'currentCity'],
  ['Present Company Name',                            'presentCompany'],
  ['Current Monthly Takehome Salary?',                'currentSalary'],
  ['Expected Monthly Takehome Salary?',               'expectedSalary'],
  ['Resume',                                          'resumeUrl']
];

/**
 * Run this once from the editor to create the sheet and header row.
 */
function setupSheet() {
  var sheet = getSheet_();
  var headers = COLUMNS.map(function (c) { return c[0]; });

  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length)
       .setFontWeight('bold')
       .setBackground('#D5232B')
       .setFontColor('#FFFFFF');
  sheet.setFrozenRows(1);
  sheet.autoResizeColumns(1, headers.length);

  Logger.log('Sheet ready with ' + headers.length + ' columns.');
}

function getSheet_() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) sheet = ss.insertSheet(SHEET_NAME);
  return sheet;
}

/**
 * Finds (or creates) the Drive folder that holds uploaded resumes.
 */
function getResumeFolder_() {
  var it = DriveApp.getFoldersByName(RESUME_FOLDER);
  return it.hasNext() ? it.next() : DriveApp.createFolder(RESUME_FOLDER);
}

/**
 * Saves a base64 resume to Drive and returns a shareable link.
 */
function saveResume_(params) {
  if (!params.resumeData) return '';
  try {
    var bytes = Utilities.base64Decode(params.resumeData);
    var safeName = (params.name || 'Applicant').replace(/[^\w\s-]/g, '').trim();
    var original = params.resumeName || 'resume';
    var ext = original.indexOf('.') > -1 ? original.split('.').pop() : 'pdf';
    var fileName = safeName + ' - ' + (params.mobile || '') + '.' + ext;

    var blob = Utilities.newBlob(bytes, params.resumeType || 'application/octet-stream', fileName);
    var file = getResumeFolder_().createFile(blob);
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    return file.getUrl();
  } catch (err) {
    return 'Upload failed: ' + String(err);
  }
}

/**
 * Handles the form POST.
 */
function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(30000);   // stop two submissions writing the same row

    var params = (e && e.parameter) ? e.parameter : {};
    var sheet  = getSheet_();

    // Create headers if someone forgot to run setupSheet
    if (sheet.getLastRow() === 0) setupSheet();

    var resumeUrl = saveResume_(params);

    var row = COLUMNS.map(function (c) {
      var key = c[1];
      if (key === 'submittedAt') return params.submittedAt || new Date();
      if (key === 'resumeUrl')   return resumeUrl;
      return params[key] || '';
    });

    sheet.appendRow(row);

    return json_({ result: 'success', row: sheet.getLastRow() });

  } catch (err) {
    return json_({ result: 'error', message: String(err) });
  } finally {
    try { lock.releaseLock(); } catch (ignore) {}
  }
}

/**
 * Lets you open the /exec URL in a browser to confirm it deployed.
 */
function doGet() {
  return json_({
    result: 'ok',
    message: 'Pillai & Sons careers endpoint is live. Submit via POST.'
  });
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
