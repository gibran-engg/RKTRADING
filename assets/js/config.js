/*
 * RK Trading: site configuration
 * ------------------------------------------------------------------
 * enquiryEndpoint
 *   Your Google Apps Script web-app URL (ends in /exec). See google-sheets-setup.md.
 *   Leave it as '' to run the enquiry form in DEMO MODE: the form validates and shows
 *   the success screen, but nothing is sent (the would-be payload is logged to the
 *   browser console instead).
 *
 *   Note: this file is served to every visitor, so the URL is public once deployed.
 *   That is normal for an Apps Script web app; the script only appends rows.
 *
 * requestTimeoutMs
 *   How long to wait for Google before showing an error, so the button never
 *   stays stuck on "Sending…".
 */
window.RK_CONFIG = {
  enquiryEndpoint: '',
  requestTimeoutMs: 20000
};
