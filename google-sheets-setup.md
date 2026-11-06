# Send website enquiries to Google Sheets

The enquiry form in `pages/index.vue` posts to a Google Apps Script web app, which appends each enquiry as a row in a Google Sheet. Until you set the URL below, the form runs in **demo mode** and sends nothing.

## 1. Create the sheet and script

1. Create a new Google Sheet (any name).
2. Open **Extensions → Apps Script**, delete the sample code and paste this:

```js
const SHEET_NAME = 'Enquiries'
// Must match the field names the website sends (see submitInquiry in pages/index.vue).
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

Create a file named `.env` in the project root:

```
NUXT_PUBLIC_ENQUIRY_ENDPOINT=https://script.google.com/macros/s/XXXXXXXX/exec
```

Restart `npm run dev` (or rebuild for production). Alternatively, paste the URL into `enquiryEndpoint` in `nuxt.config.ts`.

## Notes

- The browser cannot read Apps Script's reply (it sends no CORS headers), so the form shows "Enquiry received" once the request is sent. Check your sheet after the first test enquiry to confirm it arrived.
- The form has a hidden honeypot field to filter simple bots. For heavier spam you can add a CAPTCHA later.
- Nobody is notified when a row is added. To get an email for each enquiry, add `MailApp.sendEmail('you@yourdomain.com', 'New enquiry', JSON.stringify(e.parameter, null, 2))` inside `doPost`.
