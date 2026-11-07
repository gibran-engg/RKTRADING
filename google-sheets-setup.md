# Send website enquiries to Google Sheets

The enquiry form posts to a Google Apps Script web app, which appends each enquiry as a row in a Google Sheet. Until you set the URL (step 3), the form runs in **demo mode**: it validates and shows the success screen, but sends nothing. In demo mode the browser console (F12 → Console) shows exactly what would have been sent.

## 1. Create the sheet and script

1. Create a new Google Sheet (any name).
2. Open **Extensions → Apps Script**, delete the sample code and paste this:

```js
const SHEET_NAME = 'Enquiries'
// Must match the field names the website sends (see FIELDS in assets/js/main.js).
const FIELDS = ['name', 'email', 'company', 'country', 'phone', 'type', 'interest', 'quantity', 'message', 'page']

// Stops text such as "=IMPORTXML(...)" from being run as a formula inside your sheet.
const safe = v => (/^[=+\-@]/.test(v) ? "'" + v : v)

function doPost(e) {
  const ss = SpreadsheetApp.getActiveSpreadsheet()
  const sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME)
  if (sheet.getLastRow() === 0) sheet.appendRow(['timestamp', ...FIELDS])
  sheet.appendRow([new Date(), ...FIELDS.map(f => safe(String((e.parameter || {})[f] || '')))])
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

To go back to demo mode, set `enquiryEndpoint` back to `''`.

## Field reference

| Field      | Form control                        | Notes                         |
| ---------- | ----------------------------------- | ----------------------------- |
| `name`     | Name                                | required                      |
| `email`    | Business email                      | required, format checked      |
| `company`  | Company                             | optional                      |
| `country`  | Country                             | required                      |
| `phone`    | Phone / WhatsApp                    | optional                      |
| `type`     | Enquiry type (dropdown)             |                               |
| `interest` | Product interest (dropdown)         | pre-filled by product "Enquire" links |
| `quantity` | Quantity / volume                   | optional                      |
| `message`  | Tell us about your requirement      | pre-filled with the product name when empty |
| `page`     | —                                   | URL the enquiry was sent from |

If you add a field to the form, give the input a `name`, add that name to `FIELDS` in `assets/js/main.js`, and add it to `FIELDS` in the Apps Script too.

## Notes

- The browser cannot read Apps Script's reply (it sends no CORS headers), so the form shows "Enquiry received" once the request has left the browser. Check your sheet after the first test enquiry to confirm it arrived.
- If the request fails (offline, blocked, or no answer within `requestTimeoutMs`), the visitor sees an error and their typing is kept so they can retry.
- The URL in `config.js` is visible to anyone who views the page source. That is normal for an Apps Script web app: the script above can only append rows.
- The form has a hidden honeypot field to filter simple bots. For heavier spam you can add a CAPTCHA later.
- Nobody is notified when a row is added. To get an email for each enquiry, add `MailApp.sendEmail('you@yourdomain.com', 'New enquiry', JSON.stringify(e.parameter, null, 2))` inside `doPost`.
