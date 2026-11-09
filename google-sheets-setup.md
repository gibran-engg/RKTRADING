# Send website enquiries to Google Sheets

The enquiry forms (the quick quote on the home page and the full form on the Contact page) post to a Google Apps Script web app, which appends each enquiry as a row in a Google Sheet. Until you set the URL (step 3), both forms run in **demo mode**: they validate and show the success screen, but send nothing. In demo mode the browser console (F12 → Console) shows exactly what would have been sent.

## 1. Create the sheet and script

1. Create a new Google Sheet and type these headers in **row 1** (one per column, A to L). The script reads them, so the order is up to you and you can rename or add columns later (see the table below):

   | A | B | C | D | E | F | G | H | I | J | K | L |
   | - | - | - | - | - | - | - | - | - | - | - | - |
   | NAME | BUSINESS EMAIL | COMPANY | COUNTRY | PH/WA NUMBER | ENQUIRY TYPE | PRODUCT INTEREST | QUANTITY | REQUIREMENT | LANGUAGE | PAGE | TIMESTAMP |

   `TIMESTAMP` is optional but useful: it records when each enquiry arrived. Without it the sheet has no date.
2. Open **Extensions → Apps Script**, delete the sample code and paste this:

```js
// Which tab to write to. '' = the first tab (put the headers in row 1 of that tab).
const SHEET_NAME = ''

// Row-1 header text (any capitalisation) -> the field the website sends. Edit the left side to rename a column.
const COLUMNS = {
  'NAME': 'name',
  'BUSINESS EMAIL': 'email',
  'COMPANY': 'company',
  'COUNTRY': 'country',
  'PH/WA NUMBER': 'phone',
  'ENQUIRY TYPE': 'type',
  'PRODUCT INTEREST': 'interest',
  'QUANTITY': 'quantity',
  'REQUIREMENT': 'message',
  'LANGUAGE': 'language',
  'PAGE': 'page',
  'TIMESTAMP': 'timestamp'
}

// Stops text such as "=IMPORTXML(...)" from being run as a formula inside your sheet.
const safe = v => (/^[=+\-@]/.test(v) ? "'" + v : v)

function doPost(e) {
  const lock = LockService.getScriptLock()
  lock.waitLock(10000) // two enquiries at the same moment must not overwrite each other
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet()
    const sheet = SHEET_NAME ? ss.getSheetByName(SHEET_NAME) : ss.getSheets()[0]
    const p = e.parameter || {}
    const headers = sheet.getRange(1, 1, 1, Math.max(sheet.getLastColumn(), 1)).getValues()[0]
    const row = headers.map(h => {
      const key = COLUMNS[String(h).trim().toUpperCase()]
      if (key === 'timestamp') return new Date()
      return key ? safe(String(p[key] || '')) : ''
    })
    sheet.appendRow(row)
  } finally {
    lock.releaseLock()
  }
  return ContentService.createTextOutput('ok')
}
```

3. Click **Save**.

## 2. Publish it

1. **Deploy → New deployment → Select type: Web app**.
2. Set **Execute as: Me** and **Who has access: Anyone**.
3. Click **Deploy**, approve the permissions, and copy the **Web app URL** (it ends in `/exec`).

If you change the script later, use **Deploy → Manage deployments → Edit → New version** so the URL keeps working.

## 3. Connect the website

Open `assets/js/config.js` and paste the URL:

```js
window.RK_CONFIG = {
  enquiryEndpoint: 'https://script.google.com/macros/s/XXXXXXXX/exec',
  requestTimeoutMs: 20000
};
```

Save and reload the page. The note under the Submit button changes from "Demo mode…" to "We use your details only to respond to your enquiry." No build step or restart is needed.

**Test it:** send one enquiry from the Contact page and check that a new row appears under your headers. If a column stays empty, its header text does not match a key in `COLUMNS` (capitalisation does not matter, spelling does).

To go back to demo mode, set `enquiryEndpoint` back to `''`.

## Field reference

Sheet column by field: NAME = `name`, BUSINESS EMAIL = `email`, COMPANY = `company`, COUNTRY = `country`, PH/WA NUMBER = `phone`, ENQUIRY TYPE = `type`, PRODUCT INTEREST = `interest`, QUANTITY = `quantity`, REQUIREMENT = `message`, LANGUAGE = `language`, PAGE = `page`.

| Field      | Form control                        | Notes                                              |
| ---------- | ----------------------------------- | -------------------------------------------------- |
| `name`     | Name                                | required                                           |
| `email`    | Business email                      | required, format checked                           |
| `company`  | Company                             | optional (full form only)                          |
| `country`  | Country                             | required                                           |
| `phone`    | Phone / WhatsApp                    | optional                                           |
| `type`     | Enquiry type                        | `Request a quote` for the home quick-quote form    |
| `interest` | Product interest                    | one of the ten product lines, or `Other / not sure`; pre-filled by "Request a quote" links |
| `quantity` | Quantity / volume                   | optional (full form only)                          |
| `message`  | Tell us about your requirement      | pre-filled with the product name when empty        |
| `language` | (automatic)                         | `en`, `zh` or `ar`: the language the visitor was reading. Use it to reply in their language |
| `page`     | (automatic)                         | URL the enquiry was sent from                      |

Values are always saved in **English**, even when the visitor used the Chinese or Arabic site, so filters and automations in the sheet stay simple.

If you add a field to a form, give the input a `name`, add that name to `FIELDS` in `assets/js/main.js`, add a column with a header for it in the sheet, and add that header to `COLUMNS` in the Apps Script.

## Connecting n8n

n8n has a Google Sheets trigger ("On row added"). Use the `language` column to choose the language of the automatic email or WhatsApp reply, and `interest` to route the enquiry to the right person or template.

## Notes

- The browser cannot read Apps Script's reply (it sends no CORS headers), so the form shows "Enquiry received" once the request has left the browser. Check your sheet after the first test enquiry to confirm it arrived.
- If the request fails (offline, blocked, or no answer within `requestTimeoutMs`), the visitor sees an error and their typing is kept so they can retry.
- The URL in `config.js` is visible to anyone who views the page source. That is normal for an Apps Script web app: the script above can only append rows.
- The form has a hidden honeypot field to filter simple bots. For heavier spam you can add a CAPTCHA later.
- Nobody is notified when a row is added. To get an email for each enquiry, add `MailApp.sendEmail('you@yourdomain.com', 'New enquiry', JSON.stringify(e.parameter, null, 2))` inside `doPost`.
