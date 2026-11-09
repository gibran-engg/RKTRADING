/*
 * R.K. Trading: site configuration
 * ------------------------------------------------------------------
 * Edit this one file when the client's details arrive. No other file needs touching.
 *
 * enquiryEndpoint
 *   Google Apps Script web-app URL (ends in /exec). See google-sheets-setup.md.
 *   Leave '' to run every enquiry form in DEMO MODE: forms validate and show the success
 *   screen, but nothing is sent (the payload is logged to the browser console instead).
 *
 * contact
 *   Shown across the site (top bar, footer, Contact page) and used for the WhatsApp button.
 *   Anything left '' stays hidden in the top bar / footer and shows a "to follow" placeholder
 *   on the Contact page. Formats:
 *     phone     '+91 98765 43210'
 *     whatsapp  digits with country code, e.g. '919876543210' (opens https://wa.me/…)
 *     email     'name@yourdomain.com'
 *     address   'Street, Area, Mumbai – PIN code'
 *
 * requestTimeoutMs
 *   How long to wait for Google before showing an error, so the button never stays on "Sending…".
 *
 * Note: this file is served to every visitor, so everything in it is public once deployed.
 */
window.RK_CONFIG = {
  enquiryEndpoint: 'https://script.google.com/macros/s/AKfycbyKAeTAwyK-Lz5b18x-N27_DEMb_zSDBsg057f1C_Snt7NLU3frs5Zi1BxtfMGqhdh2/exec',
  // Option B: send enquiries to a Google Form instead. Run docs/create-google-form.gs once and paste the
  // block it prints here, replacing this empty one. See google-form-setup.md.
  googleForm: { action: '', fields: {} },
  requestTimeoutMs: 20000,
  contact: {
    phone: '+91 70064 01698',
    whatsapp: '917006401698',
    email: 'riyazwani2015@gmail.com',
    address: 'Flat 15, 3rd Floor, Haji Abdul Majid Apartments, Swami Vivekanand Marg (behind Jasmine Apts), Andheri West, Mumbai – 400058, Maharashtra'
  }
};
