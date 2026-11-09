/*
 * R.K. Trading: one-click builder for the enquiry Google Form
 * ------------------------------------------------------------------
 * Paste this into https://script.google.com (New project), click Run on
 * createRkEnquiryForm, approve the permissions, then open View > Logs
 * (or Execution log). It prints a block to paste into assets/js/config.js.
 *
 * It creates: the Google Form, a linked Google Sheet that collects the
 * responses, and (optionally) an email alert for every new enquiry.
 * Run it ONCE. Running it again creates a second form.
 */

// Optional: put an address here to get an email for each enquiry. Leave '' for none.
const NOTIFY_EMAIL = ''

const FORM_TITLE = 'R.K. Trading website enquiries'

// [key the website sends, question title, required?, long answer?]
// Keep these as plain "short answer" / "paragraph" questions: the website sends free text,
// and a dropdown or multiple-choice question would reject any value that is not an exact option.
const QUESTIONS = [
  ['name', 'Name', true],
  ['email', 'Business email', true],
  ['company', 'Company', false],
  ['country', 'Country', true],
  ['phone', 'Phone / WhatsApp', false],
  ['type', 'Enquiry type', false],
  ['interest', 'Product interest', false],
  ['quantity', 'Quantity / volume', false],
  ['message', 'Requirement', false, true],
  ['language', 'Visitor language', false],
  ['page', 'Page', false]
]

function createRkEnquiryForm() {
  const form = FormApp.create(FORM_TITLE)
  form.setDescription('Enquiries sent from the R.K. Trading website. The website posts straight to these questions, so please do not rename or delete them.')
  form.setCollectEmail(false)
  form.setAllowResponseEdits(false)
  form.setConfirmationMessage('Thank you. We will get back to you shortly.')
  try { form.setRequireLogin(false) } catch (e) { /* only available on Workspace accounts */ }

  const items = {}
  QUESTIONS.forEach(function (q) {
    const item = q[3] ? form.addParagraphTextItem() : form.addTextItem()
    item.setTitle(q[1]).setRequired(!!q[2])
    items[q[0]] = item
  })

  // Collect the answers in a Google Sheet
  const sheet = SpreadsheetApp.create(FORM_TITLE + ' (responses)')
  form.setDestination(FormApp.DestinationType.SPREADSHEET, sheet.getId())

  // Work out each question's entry.NNNN id from a pre-filled link (nothing is submitted).
  let draft = form.createResponse()
  QUESTIONS.forEach(function (q) { draft = draft.withItemResponse(items[q[0]].createResponse(q[0])) })
  const prefilled = draft.toPrefilledUrl()
  const ids = {}
  const re = /[?&](entry\.\d+)=([^&]*)/g
  let m
  while ((m = re.exec(prefilled))) ids[decodeURIComponent(m[2])] = m[1]

  const action = form.getPublishedUrl().replace(/\/viewform.*$/, '/formResponse')

  if (NOTIFY_EMAIL) ScriptApp.newTrigger('notifyNewEnquiry').forForm(form).onFormSubmit().create()

  const lines = QUESTIONS.map(function (q) { return "    " + q[0] + ": '" + (ids[q[0]] || 'NOT FOUND') + "'" })
  const block =
    'googleForm: {\n' +
    "  action: '" + action + "',\n" +
    '  fields: {\n' + lines.join(',\n') + '\n  }\n},'

  Logger.log('Paste this inside window.RK_CONFIG in assets/js/config.js:\n\n' + block)
  Logger.log('Form (edit): ' + form.getEditUrl())
  Logger.log('Responses sheet: ' + sheet.getUrl())
}

// Only used when NOTIFY_EMAIL is set.
function notifyNewEnquiry(e) {
  const body = e.response.getItemResponses().map(function (r) {
    return r.getItem().getTitle() + ': ' + r.getResponse()
  }).join('\n')
  MailApp.sendEmail(NOTIFY_EMAIL, 'New website enquiry', body)
}
