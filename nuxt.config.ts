export default defineNuxtConfig({
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      // Google Apps Script web-app URL. Set NUXT_PUBLIC_ENQUIRY_ENDPOINT in .env, or paste it here.
      // Leave empty to run the enquiry form in demo mode. See google-sheets-setup.md.
      enquiryEndpoint: ''
    }
  },
  css: ['~/assets/css/main.css'],
  app: {
    head: {
      title: 'RK Trading | International Sourcing & Distribution',
      meta: [{ name: 'description', content: 'Mumbai-based trading partner for international FMCG, botanical raw materials and fresh produce, with sourcing, shipments, packaging, labelling, quality checks, documentation and logistics.' }],
      link: [
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap' }
      ]
    }
  }
})
