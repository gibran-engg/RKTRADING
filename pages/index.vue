<script setup>
import { computed, ref } from 'vue'

const menuOpen = ref(false)
const activeCategory = ref('All')
const search = ref('')
const submitted = ref(false)
const blankForm = () => ({
  name: '', email: '', company: '', country: '', phone: '',
  type: 'Product enquiry', interest: 'FMCG & beverages', quantity: '', message: ''
})
const form = ref(blankForm())

// ---- Enquiry form -> Google Sheets -------------------------------------------------
// Set NUXT_PUBLIC_ENQUIRY_ENDPOINT in .env (or enquiryEndpoint in nuxt.config.ts) to your
// Google Apps Script web-app URL. See google-sheets-setup.md. While it is empty the form
// runs in demo mode and nothing is sent.
const endpoint = useRuntimeConfig().public.enquiryEndpoint
const demoMode = !endpoint
const sending = ref(false)
const errorMsg = ref('')
const honeypot = ref('') // hidden field: real visitors leave it empty, simple bots fill it

async function submitInquiry() {
  errorMsg.value = ''
  if (honeypot.value) { submitted.value = true; return } // silently drop bot submissions
  if (demoMode) { submitted.value = true; return }
  sending.value = true
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), 20000) // don't leave the button stuck on "Sending…"
  try {
    // Field names must match FIELDS in the Apps Script (see google-sheets-setup.md).
    const body = new URLSearchParams({ ...form.value, page: window.location.href })
    // no-cors: Apps Script does not send CORS headers, so the response is opaque.
    await fetch(endpoint, { method: 'POST', mode: 'no-cors', body, signal: controller.signal })
    submitted.value = true
    form.value = blankForm()
  } catch {
    errorMsg.value = 'Sorry, we could not send your enquiry. Please check your connection and try again.'
  } finally {
    clearTimeout(timer)
    sending.value = false
  }
}

// ---- Business details --------------------------------------------------------------
// Placeholders: replace with your verified details (shown in the Contact section).
const contact = {
  location: '[ Street address, Area, Mumbai – PIN code ]',
  locationNote: 'Placeholder: replace with your registered office address.',
  email: 'hello@rktrading.in',
  emailNote: 'Placeholder: replace with your verified business email.',
  phone: '+91 XXXXX XXXXX',
  phoneNote: 'Placeholder: replace with your business phone / WhatsApp number.'
}

// Placeholders: replace each value with your real number. Delete a row you do not hold,
// or set the array to [] to hide the "Registrations & licences" block.
const credentials = [
  { label: 'Import Export Code (IEC)', value: '[ IEC number ]' },
  { label: 'GST registration', value: '[ GSTIN ]' },
  { label: 'FSSAI licence', value: '[ FSSAI licence number ]' },
  { label: 'APEDA registration (RCMC)', value: '[ APEDA registration number ]' },
  { label: 'Spices Board registration', value: '[ Spices Board registration number ]' }
]

const enquiryTypes = [
  'Product enquiry', 'Bulk / wholesale order', 'Shipment & logistics', 'Labelling & packaging',
  'Distributor / retail partnership', 'Sample request', 'Other'
]
const interests = [
  'FMCG & beverages', 'Botanical raw materials', 'Fresh produce', 'Import / export partnership', 'Other'
]

// ---- Portfolio ---------------------------------------------------------------------
const categories = ['All', 'FMCG & beverages', 'Botanical raw materials', 'Fresh produce']
const products = [
  {
    name: 'Beverages & Energy Drinks',
    category: 'FMCG & beverages',
    origin: 'Multi-country sourcing',
    description: 'Branded soft drinks, energy drinks, juices and packaged beverages for retail, wholesale and distribution buyers.',
    items: ['Soft drinks', 'Energy drinks', 'Juices', 'Branded waters', 'Tea & coffee'],
    examples: 'Examples: Red Bull, Pepsi, Tropicana and comparable branded drinks.',
    image: 'https://images.unsplash.com/photo-1581636625402-29b2a704ef13?auto=format&fit=crop&w=1000&q=85'
  },
  {
    name: 'Snacks, Biscuits & Confectionery',
    category: 'FMCG & beverages',
    origin: 'India and international brands',
    description: 'Packaged snacks, biscuits, chocolates and sweets for supermarkets, wholesalers and distribution networks.',
    items: ['Biscuits & cookies', 'Chocolates', 'Candies & gums', 'Chips & namkeen', 'Instant noodles'],
    examples: 'Examples: Parle-G, Cadbury, Oreo, Lay’s and similar ranges.',
    image: 'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?auto=format&fit=crop&w=1000&q=85'
  },
  {
    name: 'Nutrition & Packaged Foods',
    category: 'FMCG & beverages',
    origin: 'Brand and market dependent',
    description: 'Packaged nutrition, malt-based drinks, breakfast and grocery products from established consumer food categories.',
    items: ['Malt drinks', 'Milk powder', 'Breakfast cereals', 'Sauces & condiments'],
    examples: 'Examples: Horlicks, Bournvita, Kellogg’s and similar packaged nutrition products.',
    image: 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=1000&q=85'
  },
  {
    name: 'Rice, Grains & Staples',
    category: 'FMCG & beverages',
    origin: 'India and other source markets',
    description: 'Everyday grocery staples sourced to grade, packaging size and destination-market labelling requirements.',
    items: ['Basmati & non-basmati rice', 'Atta & flours', 'Dals & pulses', 'Cooking oil', 'Spices & masalas'],
    examples: 'Examples: Basmati rice, wheat atta, toor and moong dal, whole and ground spices.',
    image: 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=1000&q=85'
  },
  {
    name: 'Personal Care & Hygiene',
    category: 'FMCG & beverages',
    origin: 'Multi-brand sourcing',
    description: 'Personal care, baby care and hygiene essentials from recognised consumer categories.',
    items: ['Oral care', 'Skin & hair care', 'Shaving', 'Soaps & hand wash', 'Baby care'],
    examples: 'Examples: Johnson’s, Colgate, Dettol and comparable ranges.',
    image: 'https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?auto=format&fit=crop&w=1000&q=85'
  },
  {
    name: 'Household & Home Care',
    category: 'FMCG & beverages',
    origin: 'Multi-brand sourcing',
    description: 'Cleaning, laundry and everyday household essentials for wholesale, supermarket and distribution buyers.',
    items: ['Laundry & detergents', 'Dishwashing', 'Surface & toilet cleaners', 'Tissue & paper goods', 'Batteries'],
    examples: 'Examples: Persil, Harpic and comparable household brands.',
    image: 'https://images.unsplash.com/photo-1563453392212-326f5e854473?auto=format&fit=crop&w=1000&q=85'
  },
  {
    name: 'Botanical Roots & Herbs',
    category: 'Botanical raw materials',
    origin: 'Afghanistan and other source markets',
    description: 'Unprocessed botanical ingredients and dried plant materials supplied as raw commodities for further processing.',
    items: ['Licorice (mulethi) root', 'Dried herbs', 'Selected botanicals'],
    examples: 'Specifications: part used, grade, moisture, cut size and packing.',
    image: 'https://images.unsplash.com/photo-1515586000433-45406d8e6662?auto=format&fit=crop&w=1000&q=85'
  },
  {
    name: 'Fresh Apples & Seasonal Fruit',
    category: 'Fresh produce',
    origin: 'Selected international origins',
    description: 'Fresh fruit sourcing based on season, grade, size, packaging and destination-market requirements.',
    items: ['Apples', 'Grapes', 'Bananas', 'Seasonal fruit'],
    examples: 'Specifications: variety, grade, size, packaging and harvest season.',
    image: 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=1000&q=85'
  },
  {
    name: 'Vegetables & Agri Commodities',
    category: 'Fresh produce',
    origin: 'India and other source markets',
    description: 'Fresh agricultural commodities for importers, wholesalers, distributors and food businesses.',
    items: ['Red onions', 'Tomatoes', 'Selected vegetables'],
    examples: 'Specifications: variety, grade, size, packaging and shelf-life requirements.',
    image: 'https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=1000&q=85'
  }
]

const filteredProducts = computed(() => products.filter(item =>
  (activeCategory.value === 'All' || item.category === activeCategory.value) &&
  [item.name, item.category, item.origin, item.description, item.items.join(' '), item.examples]
    .join(' ').toLowerCase().includes(search.value.toLowerCase())
))

// ---- Company, services, strengths, documentation -----------------------------------
const audiences = [
  'Importers', 'Distributors', 'Wholesalers', 'Retailers & supermarkets',
  'Food & beverage businesses', 'Brand owners'
]

const services = [
  { tag: 'SOURCING', title: 'Sourcing & procurement', text: 'Supplier identification, specification and price comparison, and quotations from relevant origins.' },
  { tag: 'SHIPMENTS', title: 'Import & export shipments', text: 'Consignments arranged end to end, from supplier pickup and loading through to dispatch.' },
  { tag: 'LABELLING', title: 'Labelling', text: 'Product labelling and relabelling prepared to meet destination-market and buyer requirements.' },
  { tag: 'PACKAGING', title: 'Packaging', text: 'Packing formats, carton sizes and export-grade packaging chosen to suit the product and the journey.' },
  { tag: 'QUALITY', title: 'Quality checks', text: 'Pre-shipment checks and verification against the specifications agreed with you.' },
  { tag: 'DOCUMENTATION', title: 'Trade documentation', text: 'Commercial and compliance paperwork prepared to match the product and the destination market.' },
  { tag: 'LOGISTICS', title: 'Logistics & delivery', text: 'Freight booking, transport and shipment tracking coordinated to your port or warehouse.' }
]

const strengths = [
  { title: 'Requirement-first approach', text: 'We start with your product, specification, quantity, destination and commercial terms before proposing a route.' },
  { title: 'One partner, three verticals', text: 'FMCG, botanical raw materials and fresh produce handled through a single point of contact.' },
  { title: 'Multi-origin sourcing', text: 'Supplier options across India, Afghanistan and other source markets, depending on the product.' },
  { title: 'Specification & quality focus', text: 'Grade, packaging and quality expectations are agreed up front, not after shipment.' },
  { title: 'Documentation awareness', text: 'Paperwork and regulatory requirements are reviewed for each product and destination market.' },
  { title: 'Tailored, transparent service', text: 'Every enquiry is assessed individually, with clear communication at each stage.' }
]

const documents = [
  'Commercial invoice', 'Packing list', 'Bill of lading / airway bill', 'Certificate of origin',
  'Phytosanitary certificate (plants & produce)', 'Fumigation certificate (where required)',
  'Food-safety & labelling compliance', 'Quality & inspection reports',
  'Letter of credit / banking documents', 'Customs clearance support'
]

function closeMenu() { menuOpen.value = false }
</script>

<template>
  <div>
    <div class="utility-bar">
      <div class="container utility-inner">
        <span>MUMBAI, INDIA <i></i> INTERNATIONAL SOURCING & TRADE</span>
        <a href="#contact">Business enquiries <b>↗</b></a>
      </div>
    </div>

    <header class="header">
      <div class="container nav">
        <a class="brand" href="#" @click="closeMenu">
          <span class="brand-symbol">RK</span>
          <span class="brand-text"><strong>RK TRADING</strong><small>IMPORT · EXPORT · DISTRIBUTION</small></span>
        </a>
        <button class="menu-toggle" aria-label="Toggle navigation" @click="menuOpen = !menuOpen">☰</button>
        <nav :class="{ open: menuOpen }">
          <a href="#company" @click="closeMenu">Company</a>
          <a href="#portfolio" @click="closeMenu">Our portfolio</a>
          <a href="#services" @click="closeMenu">Services</a>
          <a href="#approach" @click="closeMenu">How we work</a>
          <a class="nav-cta" href="#contact" @click="closeMenu">Contact our team <span>↗</span></a>
        </nav>
      </div>
    </header>

    <main>
      <section class="hero">
        <div class="hero-image"></div>
        <div class="container hero-inner">
          <div class="eyebrow light"><span></span> INTERNATIONAL TRADE & SOURCING</div>
          <h1>Connecting products.<br><em>Connecting markets.</em></h1>
          <p>From international FMCG brands and botanical raw materials to fresh produce, RK Trading connects sourcing opportunities with buyers across markets.</p>
          <div class="hero-actions">
            <a class="button" href="#portfolio">Explore our portfolio <b>↗</b></a>
            <a class="secondary-link" href="#company">Discover RK Trading <span>→</span></a>
          </div>
          <div class="hero-location"><span></span> MUMBAI, MAHARASHTRA, INDIA</div>
        </div>
        <div class="hero-index">01 <span></span> TRADE WITH CLARITY</div>
      </section>

      <section class="intro-strip">
        <div class="container intro-grid">
          <div><small>OUR PORTFOLIO</small><strong>Three key trading verticals</strong></div>
          <div><b>01</b><span>FMCG &<br>beverages</span></div>
          <div><b>02</b><span>Botanical<br>raw materials</span></div>
          <div><b>03</b><span>Fresh<br>produce</span></div>
        </div>
      </section>

      <section id="company" class="section company-section">
        <div class="container company-grid">
          <div class="company-visual">
            <img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1100&q=85" alt="International business district" />
            <div class="visual-caption"><small>BASED IN MUMBAI</small><strong>Local understanding.<br>International outlook.</strong></div>
          </div>
          <div class="company-copy">
            <div class="eyebrow"><span></span> ABOUT RK TRADING</div>
            <h2>A diversified trading partner with a <em>global outlook.</em></h2>
            <p class="lead">RK Trading works across consumer goods, botanical commodities and agricultural produce — bringing suppliers, distributors and buyers together.</p>
            <p>Our approach is built around understanding the requirement first: product specifications, origin, quantity, documentation, destination and commercial terms. We aim to make cross-border sourcing straightforward through clear communication and dependable coordination.</p>
            <div class="serve">
              <small>WHO WE WORK WITH</small>
              <ul class="chips"><li v-for="a in audiences" :key="a">{{ a }}</li></ul>
            </div>
            <a class="text-underline" href="#contact">Discuss a sourcing requirement <span>↗</span></a>
          </div>
        </div>
      </section>

      <section id="portfolio" class="section portfolio-section">
        <div class="container">
          <div class="section-heading">
            <div><div class="eyebrow"><span></span> WHAT WE TRADE</div><h2>Different origins.<br><em>One trading partner.</em></h2></div>
            <p>Explore our core categories, from branded consumer products to raw botanicals and fresh agricultural commodities.</p>
          </div>
          <div class="catalog-toolbar">
            <div class="filters">
              <button v-for="category in categories" :key="category" :class="{ active: activeCategory === category }" @click="activeCategory = category">{{ category }}</button>
            </div>
            <label class="search"><span>⌕</span><input v-model="search" type="search" placeholder="Search products..." /></label>
          </div>
          <div class="product-grid">
            <article v-for="item in filteredProducts" :key="item.name" class="product-card">
              <div class="product-image"><img :src="item.image" :alt="item.name" loading="lazy" /><span>{{ item.category }}</span></div>
              <div class="product-body">
                <small class="origin">{{ item.origin }}</small>
                <h3>{{ item.name }}</h3>
                <p>{{ item.description }}</p>
                <ul class="chips"><li v-for="tag in item.items" :key="tag">{{ tag }}</li></ul>
                <div class="examples">{{ item.examples }}</div>
                <a href="#contact" @click="form.interest = item.category">Enquire about this category <b>↗</b></a>
              </div>
            </article>
            <div v-if="filteredProducts.length === 0" class="empty-state">No matching products. Try a different search.</div>
          </div>
          <p class="disclaimer">Brand names are examples of product categories only and do not imply authorised distribution, endorsement or current stock. All products, origins, supplier access, specifications and destination-market permissions are subject to confirmation. Product details are indicative; buyers remain responsible for confirming import regulations and compliance in their own market.</p>
        </div>
      </section>

      <section class="sourcing-band">
        <div class="container sourcing-grid">
          <div><div class="eyebrow light"><span></span> SOURCING ACROSS MARKETS</div><h2>From origin to opportunity.</h2></div>
          <div>
            <p>We can explore FMCG sourcing from relevant international markets, botanical raw materials such as Afghan licorice root, and fresh produce such as apples from selected origins.</p>
            <p>Each enquiry is assessed individually, including supplier availability, product quality, import/export documentation and applicable regulations.</p>
            <a href="#contact">Talk to our team <span>↗</span></a>
          </div>
        </div>
      </section>

      <section id="services" class="section services-section">
        <div class="container">
          <div class="section-heading">
            <div><div class="eyebrow"><span></span> WHAT WE DO</div><h2>Beyond sourcing.<br><em>End-to-end support.</em></h2></div>
            <p>From finding the right supplier to getting goods to your door, we coordinate the details that make cross-border trade work.</p>
          </div>
          <div class="service-grid">
            <div v-for="(s, i) in services" :key="s.title" class="service-card">
              <small>{{ String(i + 1).padStart(2, '0') }} / {{ s.tag }}</small>
              <h3>{{ s.title }}</h3>
              <p>{{ s.text }}</p>
            </div>
            <a class="service-card service-cta" href="#contact">
              <small>NEED SOMETHING SPECIFIC?</small>
              <h3>Tell us your requirement.</h3>
              <span>Send an enquiry <b>↗</b></span>
            </a>
          </div>
        </div>
      </section>

      <section id="why" class="section why-section">
        <div class="container why-grid">
          <div class="company-copy">
            <div class="eyebrow"><span></span> WHY RK TRADING</div>
            <h2>Built on clarity, <em>not complexity.</em></h2>
            <p class="lead">One team, three verticals and a requirement-first way of working.</p>
            <p>Whether you need a single product or a mixed consignment across categories, we focus on the details that decide whether a trade runs smoothly: specifications, documentation and communication.</p>
            <a class="text-underline" href="#contact">Start a conversation <span>↗</span></a>
          </div>
          <div class="why-list">
            <div v-for="(s, i) in strengths" :key="s.title">
              <b>{{ String(i + 1).padStart(2, '0') }}</b>
              <div><h3>{{ s.title }}</h3><p>{{ s.text }}</p></div>
            </div>
          </div>
        </div>
      </section>

      <section id="approach" class="section approach-section">
        <div class="container">
          <div class="center-heading"><div class="eyebrow"><span></span> OUR APPROACH</div><h2>Clear communication.<br><em>Careful coordination.</em></h2></div>
          <div class="steps">
            <div><small>01 / UNDERSTAND</small><b>01</b><h3>Understand the requirement</h3><p>Product, quantity, specifications, destination and timeline.</p></div>
            <div><small>02 / SOURCE</small><b>02</b><h3>Identify sourcing options</h3><p>Explore suppliers, origin, availability and commercial terms.</p></div>
            <div><small>03 / ALIGN</small><b>03</b><h3>Coordinate trade details</h3><p>Align documentation, compliance and logistics requirements.</p></div>
            <div><small>04 / DEVELOP</small><b>04</b><h3>Build long-term business</h3><p>Keep communication transparent and relationships dependable.</p></div>
          </div>
        </div>
      </section>

      <section id="compliance" class="section docs-section">
        <div class="container docs-grid">
          <div class="company-copy">
            <div class="eyebrow"><span></span> DOCUMENTATION & COMPLIANCE</div>
            <h2>Paperwork handled <em>properly.</em></h2>
            <p class="lead">The right documents, matched to the product and the destination market.</p>
            <p>Requirements differ between processed FMCG, botanical raw materials and fresh produce, and between import markets. We review what each shipment needs up front so documentation does not become a delay at the port.</p>
          </div>
          <div>
            <ul class="doc-list"><li v-for="d in documents" :key="d">{{ d }}</li></ul>
            <div v-if="credentials.length" class="credentials">
              <small>REGISTRATIONS & LICENCES</small>
              <ul class="cred-list"><li v-for="c in credentials" :key="c.label"><span>{{ c.label }}</span><b>{{ c.value }}</b></li></ul>
            </div>
            <p class="disclaimer">Documentation requirements vary by product, origin and destination market, and are confirmed for each shipment.</p>
          </div>
        </div>
      </section>

      <section id="contact" class="contact-section">
        <div class="container contact-grid">
          <div class="contact-copy">
            <div class="eyebrow light"><span></span> BUSINESS ENQUIRIES</div>
            <h2>Let's discuss<br>your next <em>trade.</em></h2>
            <p>Looking to source a product, find a distribution partner or explore a new market? Tell us what you have in mind.</p>
            <div class="contact-detail"><span>⌖</span><div><small>LOCATION</small><strong>{{ contact.location }}</strong><em>{{ contact.locationNote }}</em></div></div>
            <div class="contact-detail"><span>✉</span><div><small>EMAIL</small><strong>{{ contact.email }}</strong><em>{{ contact.emailNote }}</em></div></div>
            <div class="contact-detail"><span>☎</span><div><small>PHONE / WHATSAPP</small><strong>{{ contact.phone }}</strong><em>{{ contact.phoneNote }}</em></div></div>
          </div>
          <div class="form-panel">
            <form v-if="!submitted" @submit.prevent="submitInquiry">
              <small class="form-label">ENQUIRY FORM / 01</small><h3>Tell us what you are looking for.</h3>
              <div class="form-row"><label>Name<input v-model="form.name" required placeholder="Full name" /></label><label>Business email<input v-model="form.email" required type="email" placeholder="you@company.com" /></label></div>
              <div class="form-row"><label>Company <span>(optional)</span><input v-model="form.company" placeholder="Company name" /></label><label>Country<input v-model="form.country" required placeholder="Destination country" /></label></div>
              <div class="form-row"><label>Phone / WhatsApp <span>(optional)</span><input v-model="form.phone" type="tel" placeholder="+country code number" /></label><label>Enquiry type<select v-model="form.type"><option v-for="t in enquiryTypes" :key="t">{{ t }}</option></select></label></div>
              <div class="form-row"><label>Product interest<select v-model="form.interest"><option v-for="i in interests" :key="i">{{ i }}</option></select></label><label>Quantity / volume <span>(optional)</span><input v-model="form.quantity" placeholder="e.g. 1 x 20ft container" /></label></div>
              <label>Tell us about your requirement<textarea v-model="form.message" rows="4" placeholder="Product, origin, specifications, destination market..."></textarea></label>
              <div class="hp" aria-hidden="true"><label>Leave this field empty<input v-model="honeypot" tabindex="-1" autocomplete="off" /></label></div>
              <button class="button submit" type="submit" :disabled="sending">{{ sending ? 'Sending…' : 'Submit enquiry' }} <b>↗</b></button>
              <p v-if="errorMsg" class="form-error" role="alert">{{ errorMsg }}</p>
              <p class="form-note">{{ demoMode ? 'Demo mode: enquiries are not sent anywhere yet. Connect Google Sheets to start receiving them.' : 'We use your details only to respond to your enquiry.' }}</p>
            </form>
            <div v-else class="success">
              <span>✓</span>
              <small>{{ demoMode ? 'DEMO ENQUIRY CAPTURED' : 'ENQUIRY RECEIVED' }}</small>
              <h3>Thank you for reaching out.</h3>
              <p>{{ demoMode ? 'The front-end form is working. Connect Google Sheets to receive enquiries.' : 'Our team will review your requirement and get back to you.' }}</p>
              <button @click="submitted = false">Send another enquiry ↗</button>
            </div>
          </div>
        </div>
      </section>
    </main>

    <footer class="footer">
      <div class="container footer-top"><a class="brand footer-brand" href="#"><span class="brand-symbol">RK</span><span class="brand-text"><strong>RK TRADING</strong><small>IMPORT · EXPORT · DISTRIBUTION</small></span></a><p>Connecting products. Connecting markets.</p><div><a href="#company">Company</a><a href="#portfolio">Portfolio</a><a href="#services">Services</a><a href="#contact">Contact</a></div></div>
      <div class="container footer-bottom"><span>© {{ new Date().getFullYear() }} RK Trading. All rights reserved.</span><span>Mumbai, India · International sourcing & trade</span></div>
    </footer>
  </div>
</template>
