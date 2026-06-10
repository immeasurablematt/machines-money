/**
 * Machines & Money digest webhook.
 *
 * Receives the daily scanner digest from GitHub Actions and saves it as a
 * Google Doc in Drive. Deploy this from script.google.com while signed in as
 * the account that should own the docs (baggetta@gmail.com).
 *
 * One-time setup (see docs/news-insights-scanner/production-setup.md):
 * 1. Replace FOLDER_ID below with the ID of the Drive folder where digests
 *    should land (the long string at the end of the folder's URL).
 * 2. Replace SHARED_TOKEN below with a long random string. Store the same
 *    value in the GitHub repo secret DIGEST_WEBHOOK_TOKEN.
 * 3. In the Apps Script editor, click the + next to "Services" and add
 *    "Drive API" (this enables Markdown-to-Doc conversion). If this step is
 *    skipped the digest still arrives, just as plain text.
 * 4. Deploy > New deployment > Web app, with "Execute as: Me" and
 *    "Who has access: Anyone". Copy the web app URL into the GitHub repo
 *    secret DIGEST_WEBHOOK_URL.
 */

var FOLDER_ID = 'PASTE_DRIVE_FOLDER_ID_HERE';
var SHARED_TOKEN = 'PASTE_A_LONG_RANDOM_TOKEN_HERE';

function doGet() {
  return ContentService.createTextOutput(
    'Machines & Money digest webhook is live.'
  );
}

function doPost(e) {
  var payload;
  try {
    payload = JSON.parse(e.postData.contents);
  } catch (err) {
    return jsonResponse_({ ok: false, error: 'invalid JSON body' });
  }
  if (!payload.token || payload.token !== SHARED_TOKEN) {
    return jsonResponse_({ ok: false, error: 'bad token' });
  }
  if (!payload.markdown) {
    return jsonResponse_({ ok: false, error: 'missing markdown' });
  }

  var title =
    payload.title ||
    'Machines & Money News Digest ' + new Date().toISOString().slice(0, 10);
  var docUrl;
  try {
    docUrl = createDocFromMarkdown_(title, payload.markdown);
  } catch (err) {
    // Drive advanced service not enabled or conversion failed; deliver the
    // digest as a plain-text Doc rather than dropping it.
    docUrl = createPlainTextDoc_(title, payload.markdown);
  }
  return jsonResponse_({ ok: true, doc_url: docUrl });
}

function createDocFromMarkdown_(title, markdown) {
  var blob = Utilities.newBlob(markdown, 'text/markdown', title + '.md');
  var file = Drive.Files.create(
    {
      name: title,
      mimeType: 'application/vnd.google-apps.document',
      parents: [FOLDER_ID],
    },
    blob
  );
  return 'https://docs.google.com/document/d/' + file.id + '/edit';
}

function createPlainTextDoc_(title, markdown) {
  var doc = DocumentApp.create(title);
  doc.getBody().setText(markdown);
  doc.saveAndClose();
  var file = DriveApp.getFileById(doc.getId());
  file.moveTo(DriveApp.getFolderById(FOLDER_ID));
  return doc.getUrl();
}

function jsonResponse_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(
    ContentService.MimeType.JSON
  );
}
