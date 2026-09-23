#!/usr/bin/env python3
"""
_build.py — assembles the static pages for no-bsjunk.com.

WHY THIS EXISTS
---------------
The parent site (no-bs-yardwork.com) has the header and footer hand-copied
into 47 separate HTML files. Changing one nav item there means 47 edits. This
script keeps the shared chrome in one place so that never happens here.

The OUTPUT is still plain static HTML with no runtime dependencies — exactly
what the FTP deploy expects. Nothing about the hosting changes.

USAGE
-----
    python3 _build.py

Edit page bodies in _pages/<name>.html (plain HTML fragments), edit the shared
chrome below, then re-run. The generated .html files at the repo root are
committed, so the site works for anyone who never runs this.

If you would rather not keep a build step at all: run it once, delete
_build.py and _pages/, and hand-edit the .html files from then on. Nothing
else depends on this script.
"""

import hashlib
import html
import json
import re
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

# Everything the business takes lives in _categories.py and is rendered below.
# Importing a local module normally leaves a __pycache__ folder in the site
# root, which would then be uploaded along with everything else. Nothing here
# is slow enough to need that cache, so it is never written.
sys.dont_write_bytecode = True
from _categories import CATEGORIES, MIN_ITEMS, NOT_TAKEN, SERVICE_TERMS  # noqa: E402


def strip_tags(s):
    """Plain text from a snippet of display HTML.

    Headlines carry markup and entities (&minus;30) because they are written for
    the page. Structured data and the RSS feed need the literal characters, so
    they run titles through here rather than keeping a second, plain-text copy
    of every headline that could drift from the visible one.
    """
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()

ROOT = Path(__file__).parent
PAGES_DIR = ROOT / "_pages"

# Cloudflare 301s www -> the bare domain at its edge, so the bare domain is
# the canonical host. Canonical tags, og:url and the sitemap must name the
# host visitors actually land on, or every one of them is a redirect hop.
SITE = "https://no-bsjunk.com"
# The image every share of this site shows unless a page names its own. A
# branded card (logo + division tag + tagline + number) rather than a photo:
# a photo of one couch says nothing about who is sharing it, and the crop
# social networks apply to a 4:5 hero cut the crew out of frame anyway. The
# twelve service pages and the before/after pages still pass their own photo,
# which is the right call for a link to one specific job.
#
# Regenerate it with: python3 images/make-og-card.py
OG_CARD = "og-card.png"

PHONE_DISPLAY = "204.900.0438"
PHONE_TEL = "+12049000438"
PHONE_E164 = "+12049000438"
EMAIL = "nobsyardwork@gmail.com"
GTM_ID = "GTM-M3MHCKF5"
# The junk site's own GA4 property. The lawn site keeps G-VN2QZ4KXXH, so the
# two sets of numbers stay apart.
GA4_ID = "G-FRJ9TZ9ZWE"
# The quote form on /quote is a JotForm embed; this is the only place its ID
# is set. Change it here and re-run the build.
#
# "Clone of Request for Quote" in the nobsyardwork JotForm account. Chosen by
# the owner and confirmed by reading the account rather than copying an ID by
# hand. Its fields: name (first/last), phone, email, a message field, and a
# full address — the message field is where the customer describes the pile.
#
# Note it is NOT the form on no-bs-yardwork.com/contact (260105131967250), so
# junk enquiries stay separable from lawn enquiries.
JOTFORM_ID = "262378273577268"

# ---------------------------------------------------------------------------
# Nav — single source of truth. (label, href, [children])
# ---------------------------------------------------------------------------
NAV = [
    ("What We Take", "what-we-take.html", [
        # Three ways in (all categories, every item, what we can't take) plus
        # the five most-searched categories. Kept at eight: the hub carries all
        # twelve, the A-Z carries everything, and a longer dropdown is unusable
        # on a laptop. Renovation Debris is reachable from both.
        ("All 12 Categories", "what-we-take.html"),
        ("Everything, A to Z", "what-we-take-a-z.html"),
        ("What We Can&rsquo;t Take", "what-we-dont-take.html"),
        ("Furniture Removal", "furniture-removal-winnipeg.html"),
        ("Appliance Removal", "appliance-removal-winnipeg.html"),
        ("Mattress Disposal", "mattress-disposal-winnipeg.html"),
        ("Hot Tub Removal", "hot-tub-removal-winnipeg.html"),
        ("Concrete &amp; Heavy Material", "concrete-removal-winnipeg.html"),
    ]),
    ("Pricing", "pricing.html", []),
    ("Commercial", "commercial-junk-removal-winnipeg.html", []),
    ("Winter", "winter-services-winnipeg.html", []),
    ("About", "about.html", [
        ("Our Story", "about.html"),
        ("Where Your Junk Goes", "where-your-junk-goes.html"),
        ("Reviews", "reviews.html"),
        ("Blog", "blog/index.html"),
    ]),
    ("Get a Quote", "quote.html", []),
]

FOOTER_LINKS = [
    ("Home", "index.html"),
    ("What We Take", "what-we-take.html"),
    ("Everything, A to Z", "what-we-take-a-z.html"),
    ("Pricing", "pricing.html"),
    ("Commercial", "commercial-junk-removal-winnipeg.html"),
    ("Winter Services", "winter-services-winnipeg.html"),
    ("Where Your Junk Goes", "where-your-junk-goes.html"),
    ("Reviews", "reviews.html"),
    ("Blog", "blog/index.html"),
    ("Get a Quote", "quote.html"),
]

# ---------------------------------------------------------------------------
# Structured data
# ---------------------------------------------------------------------------
# NOTE: no aggregateRating here on purpose. The 4.9/23 rating on
# no-bs-yardwork.com belongs to a different business entity; reusing it for
# this one would be a Google structured-data violation. Add a rating only once
# this division has collected its own reviews.
LOCAL_BUSINESS = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    # One @id for the business, referenced by every Service page's provider
    # rather than re-inlining this object. Without it each service page
    # declares a separate, unlinked LocalBusiness — thirteen businesses in the
    # graph instead of one with thirteen services.
    "@id": f"{SITE}/#localbusiness",
    "name": "No BS Junk Removal",
    "alternateName": "No-BS Yardwork Junk Removal",
    "image": f"{SITE}/images/{OG_CARD}",
    "url": SITE + "/",
    "telephone": PHONE_E164,
    "email": EMAIL,
    # A real range now that the rate card is published. "$$" told a search
    # engine nothing; the actual span of the volume card is a fact it can use.
    "priceRange": "$139-$689",
    "description": (
        "Junk removal in Winnipeg with upfront pricing and no hidden fees. "
        "Furniture, appliances, mattresses, e-waste, renovation debris, hot tubs, "
        "concrete and estate cleanouts. Skid steer and dump trailer available. "
        "The hauling division of No-BS Yardwork."
    ),
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Lakewood Blvd",
        "addressLocality": "Winnipeg",
        "addressRegion": "MB",
        "postalCode": "R2J 4A9",
        "addressCountry": "CA",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": 49.8951, "longitude": -97.1384},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification",
         "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
         "opens": "09:00", "closes": "18:00"},
        {"@type": "OpeningHoursSpecification",
         "dayOfWeek": ["Saturday", "Sunday"], "opens": "10:00", "closes": "18:00"},
    ],
    # Explicit neighbourhoods rather than just "Winnipeg". Local search is
    # largely a proximity game, and naming the areas actually served is the
    # honest way to appear for "junk removal <neighbourhood>" queries without
    # spinning up a doorway page per suburb, which Google treats as spam.
    "areaServed": [
        {"@type": "City", "name": "Winnipeg", "sameAs": "https://en.wikipedia.org/wiki/Winnipeg"},
    ] + [
        {"@type": "Place", "name": n} for n in [
            "St. Vital", "St. Boniface", "Transcona", "Charleswood", "Fort Garry",
            "River Heights", "St. James", "East Kildonan", "West Kildonan",
            "North Kildonan", "Tuxedo", "Windsor Park", "Sage Creek",
            "Bridgwater", "Southdale", "Headingley", "East St. Paul",
            "West St. Paul",
        ]
    ],
    # A plain coordinate query URL, not a fabricated Place ID. It resolves for
    # real; inventing a listing identifier would not.
    "hasMap": "https://www.google.com/maps/search/?api=1&query=49.8951,-97.1384",
    "paymentAccepted": "Cash, Cheque, e-Transfer, Credit Card",
    "currenciesAccepted": "CAD",
    # Generated from _categories.py, so the expertise this entity declares is
    # exactly the set of categories the site has pages for.
    "knowsAbout": (["Junk removal"] + [c["name"] for c in CATEGORIES]
                   + ["Commercial junk removal", "Snow removal"]),
    "parentOrganization": {
        "@type": "Organization",
        "name": "No-BS Yardwork",
        "url": "https://www.no-bs-yardwork.com",
    },
    "sameAs": [
        "https://www.facebook.com/No.BS.Yardworks",
        "https://www.instagram.com/no_bs_yardwork/",
    ],
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Junk Removal Services",
        # One Offer per real category page plus the two service pages, each
        # with its URL. The hand-kept list named nine services for a site with
        # fourteen pages and gave none of them an address.
        "itemListElement": [
            {"@type": "Offer",
             "itemOffered": {"@type": "Service", "name": name, "url": f"{SITE}/{slug}"}}
            for name, slug in (
                [(c["name"], c["slug"]) for c in CATEGORIES]
                + [("Commercial Junk Removal", "commercial-junk-removal-winnipeg"),
                   ("Snow Removal & Hauling", "winter-services-winnipeg")]
            )
        ],
    },
}


def service_schema(name, description, url, service_type):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "description": description,
        "serviceType": service_type,
        "areaServed": {"@type": "City", "name": "Winnipeg"},
        "url": url,
        # A reference, not a copy — see the @id note on LOCAL_BUSINESS.
        "provider": {"@id": f"{SITE}/#localbusiness"},
    }


def breadcrumbs(trail):
    """trail: list of (name, clean_url_path). Home is prepended automatically."""
    items = [("Home", "/")] + trail
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": n, "item": SITE + p}
            for i, (n, p) in enumerate(items, start=1)
        ],
    }


# ---------------------------------------------------------------------------
# Entity + AI-retrieval schema
# ---------------------------------------------------------------------------
# ORGANIZATION establishes the business as a named entity rather than just a
# page. Search engines and AI assistants resolve "No BS Junk Removal" to this
# node, which is what lets them answer "who does junk removal in Winnipeg"
# with a company rather than a blue link.
ORGANIZATION = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": f"{SITE}/#organization",
    "name": "No BS Junk Removal",
    "url": SITE + "/",
    "logo": {"@type": "ImageObject", "url": f"{SITE}/images/logo-badge.png"},
    "telephone": PHONE_E164,
    "email": EMAIL,
    "areaServed": {"@type": "City", "name": "Winnipeg"},
    "contactPoint": {
        "@type": "ContactPoint",
        "telephone": PHONE_E164,
        "contactType": "customer service",
        "areaServed": "CA",
        "availableLanguage": "English",
    },
    "sameAs": [
        "https://www.facebook.com/No.BS.Yardworks",
        "https://www.instagram.com/no_bs_yardwork/",
        "https://www.no-bs-yardwork.com",
    ],
}

# WEBSITE ties every page to one site entity.
# Deliberately NO SearchAction: that declares an on-site search endpoint, and
# this site has no search. Claiming one that does not exist is a broken promise
# to a crawler, not a ranking boost.
WEBSITE = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": f"{SITE}/#website",
    "url": SITE + "/",
    "name": "No BS Junk Removal",
    "inLanguage": "en-CA",
    "publisher": {"@id": f"{SITE}/#organization"},
}


def speakable_schema(url, selectors=None):
    """Mark which parts of a page are worth reading aloud.

    Voice assistants and AI answer engines use this to pick the passage that
    answers a question. Pointing it at the headline and lead paragraph keeps
    the spoken answer to the part a person actually asked about, instead of a
    machine reading a nav menu out loud.
    """
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "url": url,
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": selectors or ["h1", ".lead-in", ".faq-body"],
        },
    }


def faq_schema(pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    }


# ---------------------------------------------------------------------------
# Chrome
# ---------------------------------------------------------------------------

def render_nav(base="", current=""):
    """Render the nav. `base` is the prefix that walks back up to the web root.

    Every link and asset on this site is relative, which is what lets the whole
    thing run either as its own domain or as a subfolder of no-bs-yardwork.com
    without a rebuild. Blog posts live one directory down, so they need "../"
    in front of everything; root pages need "". Switching to root-relative
    ("/css/...") would have been less code and would have broken the subfolder
    arrangement the site is currently reachable through.
    """
    # aria-current tells a screen reader which item is the page you are on, and
    # gives the CSS something to underline. `current` is the page slug; a
    # dropdown parent is marked too when the page is one of its children, so
    # "Furniture Removal" lights up "What We Take" as well.
    # Every post under blog/ counts as being on the Blog nav item.
    here = "blog/index" if current.startswith("blog/") else current

    def mark(href, extra=""):
        return ' aria-current="page"' if href == f"{here}.html" else extra

    out = []
    for label, href, children in NAV:
        if children:
            kids = "".join(
                f'<li><a href="{base}{h}"{mark(h)}>{l}</a></li>' for l, h in children
            )
            in_section = any(h == f"{here}.html" for _, h in children)
            attrs = mark(href, ' data-section="current"' if in_section else "")
            # The chevron button opens the list in the mobile drawer; the label
            # itself still goes to the hub page. Hidden on desktop, where the
            # list opens on hover.
            sub_id = f"sub-{_anchor(label)}"
            out.append(
                f'<li class="has-sub"><a href="{base}{href}"{attrs}>{label}</a>'
                f'<button class="sub-toggle" type="button" aria-expanded="false" '
                f'aria-controls="{sub_id}"><span class="visually-hidden">'
                f'Show {label} pages</span></button>'
                f'<ul class="sub-menu" id="{sub_id}">{kids}</ul></li>'
            )
        else:
            out.append(f'<li><a href="{base}{href}"{mark(href)}>{label}</a></li>')
    return "\n                  ".join(out)


HEADER = """    <a class="skip-link" href="#main">Skip to content</a>
    <header class="site-header">
      <div class="container header-bar">
        <a class="brand-lockup" href="{BASE}index.html">
          <img src="{BASE}images/logo.svg" alt="No-Bs Junk Removal" width="141" height="50"
               fetchpriority="high" />
          <span class="division-tag">Junk Removal</span>
        </a>

        <nav class="main-menu" id="main-menu" aria-label="Main">
          <ul class="nav-list">
            {NAV}
          </ul>
        </nav>

        <a class="header-call" href="tel:{PHONE_TEL}">
          <span class="hc-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"
                 stroke-linecap="round" stroke-linejoin="round"><path
                 d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .3 1.9.6 2.8a2 2 0 0 1-.4 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.5 2.8.6a2 2 0 0 1 1.8 2.1z"/></svg>
          </span>
          <span class="hc-text">
            <span class="hc-label">Call or text any time</span>
            <span class="header-phone">{PHONE_DISPLAY}</span>
          </span>
        </a>

        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-menu">
          <span class="nav-toggle-bars" aria-hidden="true"></span>
          <span class="visually-hidden">Menu</span>
        </button>
      </div>
    </header>
"""

FOOTER = """    <footer class="site-footer">
      <div class="container">
        <div class="footer-grid">
          <div class="footer-about">
            <img class="footer-logo" src="{BASE}images/footer-logo.svg" alt="No BS Junk Removal Winnipeg"
                 loading="lazy" width="220" height="78" />
            <p>Embrace hard work, honesty and watch amazing things unfold.</p>
            <p><strong>The hauling division of
              <a href="https://www.no-bs-yardwork.com">No-BS Yardwork</a>.</strong></p>
            <ul class="footer-social">
              <li><a href="https://www.facebook.com/No.BS.Yardworks" target="_blank" rel="noopener"
                     aria-label="No-BS on Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path
                     fill="currentColor" d="M14 8.5V6.6c0-.9.6-1.1 1-1.1h2.6V1.6L14 1.6c-4 0-4.9 3-4.9 4.9v2H6.8v4h2.3V22.4H14V12.5h3.3l.4-4z"/></svg></a></li>
              <li><a href="https://www.instagram.com/no_bs_yardwork/" target="_blank" rel="noopener"
                     aria-label="No-BS on Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                     stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle
                     cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor" stroke="none"/></svg></a></li>
            </ul>
          </div>
          <div class="footer-col">
            <h3>Explore</h3>
            <ul class="footer-links">{FOOTER_LINKS}</ul>
          </div>
          <div class="footer-col">
            <h3>Office hours</h3>
            <dl class="footer-hours">
              <div><dt>Monday &ndash; Friday</dt><dd>9:00 &ndash; 6:00</dd></div>
              <div><dt>Saturday</dt><dd>10:00 &ndash; 6:00</dd></div>
              <div><dt>Sunday</dt><dd>10:00 &ndash; 6:00</dd></div>
            </dl>
          </div>
          <div class="footer-col">
            <h3>Contact</h3>
            <p><a class="footer-phone" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
            <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
            <p>Lakewood Blvd<br />Winnipeg, MB R2J 4A9</p>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; No BS Junk Removal &mdash; a No-BS Yardwork company.</p>
          <img src="{BASE}images/payments.webp" alt="Pay by cheque, e-transfer or credit card"
               loading="lazy" width="239" height="35" />
          <a class="btn-default btn-ghost" href="https://www.no-bs-yardwork.com">Visit No-BS Yardwork</a>
        </div>
      </div>
    </footer>

    <div class="mobile-call-bar">
      <a class="mcb-call" href="tel:{PHONE_TEL}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
             stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path
             d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .3 1.9.6 2.8a2 2 0 0 1-.4 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.5 2.8.6a2 2 0 0 1 1.8 2.1z"/></svg>
        Call Now
      </a>
      <a class="mcb-text" href="sms:{PHONE_E164}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
             stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path
             d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.9 8.9 0 0 1-4-.9L3 21l1.9-4.9A8.4 8.4 0 0 1 12 3.1a8.4 8.4 0 0 1 9 8.4z"/></svg>
        Text a Photo
      </a>
    </div>
"""

SCRIPTS = """    <script src="{BASE}js/site.js?v={JS_V}" defer></script>
"""

PAGE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <!-- Google Tag Manager -->
    <script>
      (function (w, d, s, l, i) {{
        w[l] = w[l] || [];
        w[l].push({{ "gtm.start": new Date().getTime(), event: "gtm.js" }});
        var f = d.getElementsByTagName(s)[0],
          j = d.createElement(s),
          dl = l != "dataLayer" ? "&l=" + l : "";
        j.async = true;
        j.src = "https://www.googletagmanager.com/gtm.js?id=" + i + dl;
        f.parentNode.insertBefore(j, f);
      }})(window, document, "script", "dataLayer", "{GTM_ID}");
    </script>
    <!-- End Google Tag Manager -->

    <title>{title}</title>
    <meta name="description" content="{description}" />
    <meta name="author" content="No BS Junk Removal" />
    <meta name="robots" content="{robots}" />
    <link rel="canonical" href="{canonical}" />

    <meta property="og:type" content="{og_type}" />
    <meta property="og:site_name" content="No BS Junk Removal" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:image" content="{SITE}/images/{og_image}" />
    <meta property="og:locale" content="en_CA" />

    <!-- Twitter/X card. Without these a shared link renders as a bare title with
         no image in X, Slack and iMessage, which all read these tags. -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />
    <meta name="twitter:image" content="{SITE}/images/{og_image}" />
    <meta name="twitter:image:alt" content="No BS Junk Removal, Winnipeg" />

    <!-- Geographic signals. Legacy tags, but still read by several local
         directories and aggregators, and free to carry. The authoritative
         location data is the LocalBusiness JSON-LD below. -->
    <meta name="geo.region" content="CA-MB" />
    <meta name="geo.placename" content="Winnipeg" />
    <meta name="geo.position" content="49.8951;-97.1384" />
    <meta name="ICBM" content="49.8951, -97.1384" />

    <link rel="shortcut icon" type="image/x-icon" href="{BASE}images/favicon.webp" />
    <link rel="alternate" type="application/rss+xml"
          title="No BS Junk Removal — Winnipeg" href="{BASE}feed.xml" />

    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="preload" as="style"
      href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap"
      onload="this.onload=null;this.rel='stylesheet';" />
    <noscript><link rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap" /></noscript>

    <link rel="stylesheet" href="{BASE}css/junk.css?v={CSS_V}" />

    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag() {{ dataLayer.push(arguments); }}
      gtag("js", new Date());
      gtag("config", "{GA4_ID}");
    </script>

{schema}  </head>
  <body class="{body_class}">
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
      height="0" width="0" style="display: none; visibility: hidden"></iframe></noscript>

{HEADER}
    <main id="main">
{body}    </main>

{FOOTER}
{SCRIPTS}  </body>
</html>
"""

DEFAULT_ROBOTS = "follow, index, max-snippet:-1, max-video-preview:-1, max-image-preview:large"


# ---------------------------------------------------------------------------
# Page definitions
# ---------------------------------------------------------------------------
def clean_url(slug):
    """The public URL path for a slug, as visitors and Google see it.

    `.html` is stripped by .htaccess, and a directory index is reached by the
    directory name alone — so index -> "/", blog/index -> "/blog". Canonical
    tags, breadcrumbs, the sitemap and the feed all derive from this one
    function, so they cannot disagree about what a page's address is.
    """
    if slug == "index":
        return "/"
    if slug.endswith("/index"):
        # Trailing slash kept on purpose: Apache's DirectorySlash 301s /blog to
        # /blog/, so a sitemap or canonical saying "/blog" hands Google a
        # redirect where a 200 belongs.
        return "/" + slug[: -len("index")]
    return "/" + slug


def P(slug, title, description, og_image=OG_CARD, crumbs=None,
      schema=None, robots=DEFAULT_ROBOTS, body_class="", base="",
      og_type="website", lastmod=None, priority=None, render=None):
    """Define one page.

    `render` is for pages whose body is generated rather than authored — the
    blog index and the post wrapper. It returns text still containing {TOKENS},
    which the page loop substitutes exactly as it does for a hand-written
    fragment, so generated and authored pages go through one code path.
    """
    # Length guards. Google truncates titles past roughly 60 characters and
    # descriptions past roughly 160, and both had drifted well past that on
    # two thirds of the site before anyone noticed — because nothing checked.
    # Failing the build is the only version of this that stays true: a note in
    # a README gets skimmed, a SystemExit does not. Blog posts route through
    # P() too, so this covers them without a second copy in BP().
    #
    # Titles and descriptions carry entities (&amp;) because they are written
    # for the page, so both are measured as the characters a reader actually
    # sees. noindex pages (404, thanks) are exempt from the description floor:
    # they are never a search result, so there is nothing to pad out.
    if len(strip_tags(title)) > 60:
        raise SystemExit(
            f"{slug}: title is {len(strip_tags(title))} chars (max 60)\n  {strip_tags(title)}")
    if "noindex" not in robots:
        n = len(strip_tags(description))
        if not 120 <= n <= 158:
            raise SystemExit(
                f"{slug}: description is {n} chars (want 120-158)\n  {strip_tags(description)}")

    blocks = list(schema or [])
    if crumbs is not None:
        blocks.append(breadcrumbs(crumbs))
    return {
        "slug": slug, "title": title, "description": description,
        "og_image": og_image, "schema": blocks, "robots": robots,
        "body_class": body_class, "base": base, "og_type": og_type,
        "lastmod": lastmod, "priority": priority, "render": render,
    }


# ---------------------------------------------------------------------------
# What we take — generated from _categories.py
# ---------------------------------------------------------------------------
# Every place that lists what the business takes is built from one list, so the
# hub grid, the A-Z, each category page, the homepage and the structured data
# cannot drift apart. That drift had already happened once: the hand-written
# hub described ten categories on a twelve-category site. To add an item, edit
# _categories.py, not this.
#
# The category tokens are expanded by plain string replacement, exactly like
# the FAQ accordion. Never write a token's literal name inside a comment in a
# fragment: the comment gets expanded too, and the block renders twice.

def _e(s):
    """Escape data-file text for HTML. _categories.py is written as plain text."""
    return html.escape(s, quote=True)


def _anchor(name):
    """Anchor id for an item: "Kids' toys" -> "kids-toys"."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _category(slug):
    return next((c for c in CATEGORIES if c["slug"] == slug), None)


def check_categories():
    """Refuse to build on inconsistent category data. The rules are documented
    at the top of _categories.py, where the person editing it will see them."""
    seen = {}

    def claim(term, owner):
        key = term.strip().lower()
        if key in seen:
            where = owner if seen[key] == owner else f"{seen[key]} and {owner}"
            raise SystemExit(f'_categories.py: "{term}" is listed more than once ({where})')
        seen[key] = owner

    icons = set(re.findall(r"\.ti-([a-z-]+)\s*\{",
                           (ROOT / "css" / "junk.css").read_text(encoding="utf-8")))
    for c in CATEGORIES:
        frag = PAGES_DIR / f"{c['slug']}.html"
        if not frag.exists():
            raise SystemExit(f"_categories.py: no page fragment for {c['slug']}")
        if "{CATEGORY_ITEMS}" not in frag.read_text(encoding="utf-8"):
            raise SystemExit(f"{c['slug']}: category page never renders its item list")
        if c["icon"] not in icons:
            raise SystemExit(f"_categories.py: {c['slug']} uses icon '{c['icon']}' "
                             f"but junk.css has no .ti-{c['icon']} rule")
        if len(c["items"]) < MIN_ITEMS:
            raise SystemExit(f"_categories.py: {c['name']} has {len(c['items'])} "
                             f"items (minimum {MIN_ITEMS})")
        for it in c["items"]:
            claim(it["name"], c["name"])
            for a in it["aka"]:
                claim(a, c["name"])
    for group, label in ((SERVICE_TERMS, "SERVICE_TERMS"), (NOT_TAKEN, "NOT_TAKEN")):
        for t in group:
            claim(t["name"], label)
            for a in t["aka"]:
                claim(a, label)


# Runs at import, before PAGES is built — the same moment the title guards in
# P() run — so bad data fails on a clear message rather than deep in a render.
check_categories()


# Real before/after pairs, shown on the homepage. EMPTY ON PURPOSE: the
# section renders only when there is something real to put in it, because a
# strip of placeholder frames is worse than no strip at all. Add an entry once
# a job has been photographed from the same spot twice:
#
#     {"before": "job1-before.webp", "after": "job1-after.webp",
#      "alt": "Garage packed to the door, then swept empty",
#      "caption": "Garage cleanout, St. Vital",
#      "flag": ""}       # "flag" labels work carried over from the lawn side
#
# Both files go in images/ at 1000x667. The two frames must be shot from the
# same spot — a pair where the camera moved is not proof of anything.
BEFORE_AFTER = []


def render_before_after():
    """The before/after strip, or nothing at all if there are no pairs yet."""
    if not BEFORE_AFTER:
        return ""
    cards = []
    for p in BEFORE_AFTER:
        flag = (f'\n                <span class="carryover-flag">{_e(p["flag"])}</span>'
                if p.get("flag") else "")
        cards.append(f'''
              <figure class="ba-pair">{flag}
                <div class="ba-frames">
                  <div class="ba-shot is-before">
                    <img src="{{BASE}}images/{p["before"]}" alt="{_e(p["alt"])} &mdash; before"
                         width="1000" height="667" loading="lazy" decoding="async" />
                    <span class="ba-tag">Before</span>
                  </div>
                  <div class="ba-shot is-after">
                    <img src="{{BASE}}images/{p["after"]}" alt="{_e(p["alt"])} &mdash; after"
                         width="1000" height="667" loading="lazy" decoding="async" />
                    <span class="ba-tag">After</span>
                  </div>
                </div>
                <figcaption>{_e(p["caption"])}</figcaption>
              </figure>''')
    return f'''      <section class="section-space bg-tint">
        <div class="container">
          <div class="section-title text-center">
            <p class="eyebrow">Real jobs</p>
            <h2>Same spot, two hours apart</h2>
          </div>
          <div class="ba-strip">{"".join(cards)}
          </div>
        </div>
      </section>

'''


def render_take_grid():
    """The twelve category tiles, used on the homepage and the hub.

    A tile is a photograph with its label over a gradient. If a category has no
    photo in images/tiles/ yet, that one tile falls back to the line icon it
    used before, so a missing file degrades to the old look instead of leaving
    a hole. Photos are lazy-loaded and sized, so the grid costs no layout shift.
    """
    tiles = []
    for c in CATEGORIES:
        photo = ROOT / "images" / "tiles" / f'{c["icon"]}.webp'
        if photo.exists():
            inner = (
                f'<img src="{{BASE}}images/tiles/{c["icon"]}.webp" alt="" '
                f'width="500" height="333" loading="lazy" decoding="async" />'
            )
            cls = ' class="has-photo"'
        else:
            inner = f'<span class="ti ti-{c["icon"]}"></span>'
            cls = ""
        tiles.append(
            f'\n            <li{cls}><a href="{{BASE}}{c["slug"]}.html">'
            f'{inner}<span class="tk-label">{_e(c["short"])}</span></a></li>'
        )
    return f'<ul class="take-grid">{"".join(tiles)}\n          </ul>'


def render_take_list():
    """The "is my thing on the list?" block for the homepage.

    This used to be all 152 item names as one grey paragraph. The words earn
    their keep for search, but nobody reads a wall of nouns, so they now sit
    inside a closed <details>: still in the page for crawlers, out of the way
    for people. Above it is the thing a visitor actually wants — a search box
    that hands the query to the A-Z page, which filters on load.

    The form is a plain GET, so it works with JavaScript off: without it you
    land on the full A-Z list, which is a reasonable answer to the question.
    """
    names = " ".join(f"{_e(it['name'])}." for c in CATEGORIES for it in c["items"])
    count = sum(len(c["items"]) for c in CATEGORIES)
    return (
        '<div class="take-find">'
        '\n            <form class="take-search" action="{BASE}what-we-take-a-z.html" method="get">'
        '\n              <label for="take-q">Type what you&rsquo;ve got</label>'
        '\n              <div class="take-search-row">'
        '\n                <input type="search" id="take-q" name="q" '
        'placeholder="Treadmill, fridge, hot tub&hellip;" autocomplete="off" />'
        '\n                <button type="submit" class="btn-default">Check the list</button>'
        '\n              </div>'
        '\n            </form>'
        f'\n            <details class="take-all">'
        f'\n              <summary>See all {count} things we take</summary>'
        f'\n              <div class="take-list">{names} '
        f'<a href="{{BASE}}what-we-take-a-z.html">The whole list, A to Z &rarr;</a></div>'
        f'\n            </details>'
        '\n          </div>'
    )


def render_category_items(c):
    """The full item list on one category page."""
    rows = []
    for it in c["items"]:
        aka = (f'<span class="ci-aka">Also: {_e(", ".join(it["aka"]))}</span>'
               if it["aka"] else "")
        rows.append(
            f'\n                <div class="ci-item" id="{_anchor(it["name"])}">'
            f'\n                  <dt>{_e(it["name"])}</dt>'
            f'\n                  <dd>{_e(it["note"])}{aka}</dd>'
            f'\n                </div>'
        )
    return (
        '\n              <h3 class="ci-heading">Everything we take in this category</h3>'
        '\n              <dl class="ci-list">' + "".join(rows) + '\n              </dl>'
        '\n              <p class="ci-more">Not on the list? Check '
        '<a href="{BASE}what-we-take-a-z.html">everything we take, A to Z</a>, or '
        '<a href="sms:{PHONE_E164}">text us a photo</a> and we will tell you straight.</p>\n'
    )


def expand_take_tokens(text, slug):
    """Fill the category tokens in one page. Runs before {BASE} substitution,
    so the {BASE} tokens inside the rendered blocks get filled in too."""
    if "{TAKE_GRID}" in text:
        text = text.replace("{TAKE_GRID}", render_take_grid())
    if "{TAKE_LIST}" in text:
        text = text.replace("{TAKE_LIST}", render_take_list())
    if "{BEFORE_AFTER}" in text:
        text = text.replace("{BEFORE_AFTER}", render_before_after())
    if "{CATEGORY_ITEMS}" in text:
        c = _category(slug)
        if c is None:
            raise SystemExit(f"{slug}: renders a category item list but is not a "
                             f"category in _categories.py")
        text = text.replace("{CATEGORY_ITEMS}", render_category_items(c))
    return text


def _az_entries():
    """Every searchable term, sorted, as (name, dd_html, search_text, css_class)."""
    rows = []

    def add(name, dd_html, search_text, cls=""):
        rows.append((name, dd_html, search_text.lower(), cls))

    def see(alias, target):
        add(alias, f'See <a href="#{_anchor(target)}">{_e(target)}</a>.',
            f"{alias} {target}", "az-see")

    for c in CATEGORIES:
        link = f'<a href="{{BASE}}{c["slug"]}.html">{_e(c["name"])}</a>'
        for it in c["items"]:
            add(it["name"], f'{_e(it["note"])} {link}', f'{it["name"]} {it["note"]}')
            for a in it["aka"]:
                see(a, it["name"])
    for t in SERVICE_TERMS:
        add(t["name"],
            f'<span class="az-tag az-tag-service">Service</span> {_e(t["note"])} '
            f'<a href="{{BASE}}{t["slug"]}.html">More about this service</a>',
            f'{t["name"]} {t["note"]}')
        for a in t["aka"]:
            see(a, t["name"])
    for t in NOT_TAKEN:
        add(t["name"],
            f'<span class="az-tag az-tag-no">We can&rsquo;t take this</span> '
            f'{_e(t["why"])} {_e(t["where"])} '
            f'<a href="{{BASE}}what-we-dont-take.html">Where it goes</a>',
            f'{t["name"]} {t["why"]} {t["where"]}', "az-no")
        for a in t["aka"]:
            see(a, t["name"])

    rows.sort(key=lambda r: r[0].lower())
    ids = {}
    for name, *_ in rows:
        k = _anchor(name)
        if k in ids:
            raise SystemExit(f'A-Z: "{name}" and "{ids[k]}" produce the same anchor #{k}')
        ids[k] = name
    return rows


def render_az(_base=None):
    rows = _az_entries()
    groups = {}
    for name, dd, search, cls in rows:
        first = name[0].upper()
        groups.setdefault(first if first.isalpha() else "#", []).append((name, dd, search, cls))
    order = sorted(groups, key=lambda L: (L != "#", L))

    def gid(L):
        return "letter-num" if L == "#" else f"letter-{L.lower()}"

    jump = "".join(f'<li><a href="#{gid(L)}">{L}</a></li>' for L in order)
    blocks = []
    for L in order:
        entries = []
        for name, dd, search, cls in groups[L]:
            klass = f"az-entry {cls}" if cls else "az-entry"
            entries.append(
                f'\n                <div class="{klass}" data-term="{_e(search)}">'
                f'\n                  <dt id="{_anchor(name)}">{_e(name)}</dt>'
                f'\n                  <dd>{dd}</dd>'
                f'\n                </div>'
            )
        blocks.append(
            f'\n              <div class="az-group" id="{gid(L)}">'
            f'\n                <h2 class="az-letter">{L}</h2>'
            f'\n                <dl class="az-list">{"".join(entries)}'
            f'\n                </dl>'
            f'\n              </div>'
        )

    return f'''      <div class="page-header">
        <div class="container">
          <div class="row align-items-center">
            <div class="col-lg-12">
              <div class="page-header-box">
                <h1>Everything we take, A to Z</h1>
                <nav aria-label="Breadcrumb">
                  <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="{{BASE}}index.html">Home</a></li>
                    <li class="breadcrumb-item"><a href="{{BASE}}what-we-take.html">What We Take</a></li>
                    <li class="breadcrumb-item" aria-current="page">A to Z</li>
                  </ol>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>

      <section class="section-space">
        <div class="container">
          <div class="row justify-content-center">
            <div class="col-lg-9">
              <p class="lead-in">
                {len(rows)} things people ask us to haul, and what is worth knowing about
                each one: what makes it awkward, roughly what it weighs, and where it
                actually goes in Winnipeg. If it is legal for us to haul, it is on here. If
                it is not, it is on here too, with where to take it instead.
              </p>

              <div class="az-tools" id="az-tools" hidden>
                <label for="az-filter" class="az-filter-label">Find something</label>
                <input type="search" id="az-filter" class="az-filter"
                       placeholder="Try &ldquo;treadmill&rdquo; or &ldquo;fridge&rdquo;"
                       autocomplete="off" />
              </div>
              <nav aria-label="Jump to a letter">
                <ul class="az-jump">{jump}</ul>
              </nav>
            </div>
          </div>
        </div>
      </section>

      <section class="section-space bg-tint az-body">
        <div class="container">
          <div class="row justify-content-center">
            <div class="col-lg-9">{"".join(blocks)}
              <p class="az-empty" id="az-empty" hidden>
                Nothing on the list matches that. <a href="sms:{{PHONE_E164}}">Text us a
                photo</a> and we will tell you straight whether we take it.
              </p>

              <div class="callout">
                <h3>Still not sure?</h3>
                <p>
                  Send a photo and we will tell you whether we take it and roughly what it
                  costs, usually within the hour.
                </p>
                <div class="btn-row">
                  <a href="sms:{{PHONE_E164}}" class="btn-default">Text a photo</a>
                  <a href="{{BASE}}what-we-dont-take.html" class="btn-default btn-ghost on-light">What we can&rsquo;t take</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <script>
        /* A-Z filter. Progressive enhancement: the search box ships hidden and
           only appears once this runs, so nobody without JavaScript is shown a
           box that does nothing. The full list is always there regardless. */
        (function () {{
          var tools = document.getElementById("az-tools");
          var input = document.getElementById("az-filter");
          if (!tools || !input) return;
          tools.hidden = false;
          var entries = [].slice.call(document.querySelectorAll(".az-entry"));
          var groups = [].slice.call(document.querySelectorAll(".az-group"));
          var empty = document.getElementById("az-empty");
          function apply() {{
            var q = input.value.trim().toLowerCase();
            var shown = 0;
            entries.forEach(function (e) {{
              var hit = !q || e.getAttribute("data-term").indexOf(q) !== -1;
              e.hidden = !hit;
              if (hit) shown++;
            }});
            groups.forEach(function (g) {{
              g.hidden = !g.querySelector(".az-entry:not([hidden])");
            }});
            if (empty) empty.hidden = shown !== 0;
          }}
          input.addEventListener("input", apply);
          /* The homepage search box hands its query over as ?q=. Run the same
             filter on arrival so the visitor lands on their answer, not on
             735 entries they have to scroll. */
          var q0 = new URLSearchParams(location.search).get("q");
          if (q0) {{
            input.value = q0;
            apply();
            input.focus();
          }}
        }})();
      </script>
'''


def az_itemlist_schema():
    """ItemList of every real item, each pointing at its own A-Z anchor."""
    names = sorted((it["name"] for c in CATEGORIES for it in c["items"]), key=str.lower)
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Everything No BS Junk Removal takes",
        "numberOfItems": len(names),
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": n,
             "url": f"{SITE}{clean_url('what-we-take-a-z')}#{_anchor(n)}"}
            for i, n in enumerate(names, start=1)
        ],
    }


def render_what_we_take(_base=None):
    n_items = sum(len(c["items"]) for c in CATEGORIES)
    cards = []
    for c in CATEGORIES:
        sample = ", ".join(it["name"] for it in c["items"][:6])
        more = len(c["items"]) - 6
        tail = f", and {more} more" if more > 0 else ""
        cards.append(f'''
            <div class="col-lg-6 mb-4" id="{c["icon"]}">
              <div class="reason-card">
                <h3><a href="{{BASE}}{c["slug"]}.html">{_e(c["name"])}</a></h3>
                <p>{_e(c["blurb"])}</p>
                <p class="cat-card-items">{_e(sample)}{tail}.</p>
                <a href="{{BASE}}{c["slug"]}.html" class="cat-card-link">Everything in {_e(c["short"])} &rarr;</a>
              </div>
            </div>''')

    return f'''      <div class="page-header">
        <div class="container">
          <div class="row align-items-center">
            <div class="col-lg-12">
              <div class="page-header-box">
                <h1>What we take</h1>
                <nav aria-label="Breadcrumb">
                  <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="{{BASE}}index.html">Home</a></li>
                    <li class="breadcrumb-item" aria-current="page">What We Take</li>
                  </ol>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>

      <section class="section-space">
        <div class="container">
          <div class="section-title text-center">
            <p class="eyebrow wow fadeInUp">categories</p>
            <h2>If it&rsquo;s legal for us to haul, we take it</h2>
          </div>
          <p class="lead-in text-center" style="margin: 0 auto 40px">
            Twelve categories, one trailer, one price. Between them they cover {n_items}
            kinds of thing, and each category has its own page with what we take, what it
            costs and the questions people actually ask. Looking for one particular item?
            <a href="{{BASE}}what-we-take-a-z.html">Search everything, A to Z</a>.
          </p>
          {render_take_grid()}
        </div>
      </section>

      <section class="section-space bg-tint">
        <div class="container">
          <div class="row">{"".join(cards)}
          </div>

          <div class="text-center" style="margin-top: 20px">
            <p class="lead-in" style="margin: 0 auto 20px">
              <strong>Not sure if we take it? Send us a photo. We&rsquo;ll tell you straight.</strong>
            </p>
            <div class="btn-row justify-content-center">
              <a href="sms:{{PHONE_E164}}" class="btn-default">Text us a photo</a>
              <a href="{{BASE}}what-we-take-a-z.html" class="btn-default btn-ghost on-light">Everything, A to Z</a>
              <a href="{{BASE}}what-we-dont-take.html" class="btn-default btn-ghost on-light">What we can&rsquo;t take</a>
            </div>
          </div>
        </div>
      </section>
'''


def render_not_taken(_base=None):
    cards = "".join(f'''
                <div class="nt-card" id="{_anchor(t["name"])}">
                  <h3>{_e(t["name"])}</h3>
                  <p><span class="nt-label">Why we can&rsquo;t:</span> {_e(t["why"])}</p>
                  <p><span class="nt-label">Where it goes:</span> {_e(t["where"])}</p>
                  <p class="nt-aka">Also covers: {_e(", ".join(t["aka"]))}</p>
                </div>''' for t in NOT_TAKEN)

    return f'''      <div class="page-header">
        <div class="container">
          <div class="row align-items-center">
            <div class="col-lg-12">
              <div class="page-header-box">
                <h1>What we can&rsquo;t take, and who can</h1>
                <nav aria-label="Breadcrumb">
                  <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="{{BASE}}index.html">Home</a></li>
                    <li class="breadcrumb-item"><a href="{{BASE}}what-we-take.html">What We Take</a></li>
                    <li class="breadcrumb-item" aria-current="page">What We Can&rsquo;t Take</li>
                  </ol>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>

      <section class="section-space">
        <div class="container">
          <div class="row justify-content-center">
            <div class="col-lg-9">
              <div class="section-title">
                <p class="eyebrow">the short list</p>
                <h2>If it&rsquo;s legal for us to haul, we take it</h2>
              </div>
              <p class="lead-in">
                Almost everything a house, a yard or a job site produces goes in our trailer.
                The few things below do not, because hauling them without the right licence
                is illegal, dangerous or both, and we are not going to pretend otherwise to
                win a job.
              </p>
              <p>
                What we will do is tell you exactly where each one should go instead. That
                call is free, and several of these are free to drop off if you live in
                Winnipeg.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="section-space bg-tint">
        <div class="container">
          <div class="row justify-content-center">
            <div class="col-lg-10">
              <div class="nt-grid">{cards}
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section-space">
        <div class="container">
          <div class="row justify-content-center">
            <div class="col-lg-9">
              <div class="section-title">
                <h2>The 4R Winnipeg Depots</h2>
              </div>
              <p>
                The City runs three 4R Winnipeg Depots for residents. What each one accepts
                differs, and hours change with the season:
              </p>
              <ul class="price-includes">
                <li><strong>Brady</strong> &mdash; 1825 Brady Road</li>
                <li><strong>Pacific</strong> &mdash; 1120 Pacific Avenue <em>(closed Wednesdays)</em></li>
                <li><strong>Panet</strong> &mdash; 429 Panet Road <em>(closed Wednesdays)</em></li>
              </ul>
              <p>
                Check
                <a href="https://www.winnipeg.ca/services-programs/recycling-garbage/4r-winnipeg-depots"
                   target="_blank" rel="noopener">the City&rsquo;s 4R Depot page</a>
                for what each depot takes and its current hours before you drive over.
              </p>

              <div class="callout">
                <h3>Working fridge or freezer? Don&rsquo;t pay us to take it.</h3>
                <p>
                  If it still runs, Efficiency Manitoba will pick it up from your home for free
                  and pay you a $30 rebate. We can&rsquo;t beat that, so take it. If it has
                  stopped working, that is where we come in.
                </p>
                <a href="https://efficiencymb.ca/articles/how-should-i-get-rid-of-my-old-fridge-or-freezer/"
                   class="btn-default" target="_blank" rel="noopener">Efficiency Manitoba pickup</a>
              </div>

              <div class="callout">
                <h3>Not sure which side of the line it&rsquo;s on?</h3>
                <p>
                  Send us a photo. We will tell you straight whether we can take it, and if we
                  can&rsquo;t, where it should go.
                </p>
                <div class="btn-row">
                  <a href="sms:{{PHONE_E164}}" class="btn-default">Text a photo</a>
                  <a href="{{BASE}}what-we-take-a-z.html" class="btn-default btn-ghost on-light">Everything we do take</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
'''


PAGES = [
    P("index",
      "Junk Removal Winnipeg | Upfront Pricing, No Hidden Fees",
      "Winnipeg junk removal with upfront pricing and no hidden fees. Furniture, "
      "appliances, reno debris, hot tubs and concrete. Skid steer available. "
      "Free quotes.",
      # The homepage is the link that actually gets shared. It used the hero
      # photo, which social networks crop from 4:5 to 1.91:1 — cutting the crew
      # out and leaving an anonymous van. OG_CARD says who this is instead.
      og_image=OG_CARD,
      schema=[LOCAL_BUSINESS, ORGANIZATION, WEBSITE], body_class="home"),

    P("pricing",
      "Junk Removal Prices Winnipeg | Upfront Rates, No Hidden Fees",
      "See exactly what junk removal costs in Winnipeg. Labour, hauling and dump fees "
      "all included, and we explain why heavy material is priced by weight.",
      crumbs=[("Pricing", "/pricing")],
      schema=[faq_schema([
          ("How is junk removal priced in Winnipeg?",
           "You pay for the space your junk takes up in our trailer. Our trailer is 14 feet "
           "long by 7 feet wide by 4 feet high, and every price includes labour, hauling, "
           "disposal and dump fees, and a basic sweep-up when we are done. Rates run from "
           "$139 for a single item or half a pickup load up to $689 for a full trailer."),
          ("Why is concrete priced differently from furniture?",
           "Concrete, brick, patio stone, asphalt, gravel, dirt, plaster and shingles are "
           "priced by weight rather than volume, because the landfill charges us by the tonne. "
           "A half-trailer of couches might weigh 400 lbs; a half-trailer of concrete can weigh "
           "over 6,000 lbs."),
          ("Are there hidden fees?",
           "No. There is no fuel surcharge, no stairs fee and no environmental levy added at "
           "the end. The price we quote on site before any work starts is the price you pay."),
          ("What will you not take?",
           "We cannot take wet paint, solvents, chemicals, pesticides, asbestos or suspected "
           "asbestos, propane tanks, fuel, oil, explosives, medical or biohazard waste, or "
           "ammunition. Call us anyway and we will point you to who can handle it."),
      ])]),

    P("what-we-take",
      "What We Take | Junk Removal Winnipeg | No BS Junk Removal",
      "Furniture, appliances, mattresses, e-waste, reno debris, hot tubs, sheds, "
      "concrete, yard waste, estate cleanouts, scrap metal and pianos across Winnipeg.",
      crumbs=[("What We Take", "/what-we-take")],
      render=render_what_we_take),

    P("what-we-take-a-z",
      "Everything We Take, A to Z | Junk Removal Winnipeg",
      "Every item we haul in Winnipeg, from couches and fridges to hot tubs and concrete, "
      "with what it weighs, why it's awkward and where it actually goes.",
      crumbs=[("What We Take", "/what-we-take"), ("A to Z", "/what-we-take-a-z")],
      schema=[az_itemlist_schema()],
      priority="0.90",
      render=render_az),

    P("what-we-dont-take",
      "What We Can't Take, and Who Can | No BS Junk Removal",
      "Paint, propane, asbestos and chemicals can't go in a junk trailer. Here is where "
      "each one goes instead in Winnipeg, much of it free for residents.",
      crumbs=[("What We Take", "/what-we-take"),
              ("What We Can't Take", "/what-we-dont-take")],
      render=render_not_taken),

    P("hot-tub-removal-winnipeg",
      "Hot Tub Removal Winnipeg | Disconnect, Breakdown &amp; Haul-Away",
      "Hot tub removal in Winnipeg. We disconnect, break it down on site and haul every "
      "piece away in one visit, without wrecking your deck, fence or lawn.",
      og_image="hot-tub-removal.webp", crumbs=[("What We Take", "/what-we-take"), ("Hot Tub Removal", "/hot-tub-removal-winnipeg")],
      schema=[
          service_schema("Hot Tub Removal Winnipeg",
                         "Full hot tub disconnect, on-site breakdown and haul-away in Winnipeg, "
                         "including tight-access yards and raised decks.",
                         f"{SITE}/hot-tub-removal-winnipeg", "Hot Tub Removal"),
          faq_schema([
              ("Do I need to drain the hot tub first?",
               "It helps, but we can handle it either way. If you can drain it the day before, "
               "the job goes faster. If not, tell us when you book and we will bring a pump."),
              ("Can you get a hot tub out through a narrow gate?",
               "Yes. Most hot tubs will not fit through a standard 30-inch gate intact, so we cut "
               "them into haulable sections on site. That is normal and it is included in the price."),
              ("Do you disconnect the electrical?",
               "We disconnect the tub at the whip and cap it safely. If the panel or breaker needs "
               "work, that is an electrician's job and we will tell you so rather than guess."),
              ("How much does hot tub removal cost in Winnipeg?",
               "It depends on size and access. We give you a firm price on a free on-site estimate "
               "before any work starts, and that price includes labour, hauling and disposal."),
          ]),
      ]),

    P("appliance-removal-winnipeg",
      "Appliance Removal Winnipeg | Fridges, Washers &amp; Furnaces",
      "Fridges, freezers, washers, dryers, stoves and furnaces hauled away in Winnipeg "
      "and taken to a certified recycler, with refrigerant recovered properly.",
      og_image="appliance-removal.webp", crumbs=[("What We Take", "/what-we-take"), ("Appliance Removal", "/appliance-removal-winnipeg")],
      schema=[
          service_schema("Appliance Removal Winnipeg",
                         "Removal and certified recycling of fridges, freezers, washers, dryers, "
                         "stoves and furnaces in Winnipeg.",
                         f"{SITE}/appliance-removal-winnipeg", "Appliance Removal"),
          faq_schema([
              ("What happens to my old fridge?",
               "It goes to a certified appliance recycler who recovers the refrigerant with a "
               "certified technician. That is a legal requirement, not an optional extra, and we "
               "can tell you where your unit went."),
              ("Can you get an appliance out of a basement?",
               "Yes. Winnipeg character homes often have basement stairs too narrow for a standard "
               "appliance dolly, so we bring stair-climbing gear. Mention the stairs when you book."),
              ("Do you take more than one appliance at a time?",
               "Yes, and it is usually cheaper per item. A full load of metal appliances may qualify "
               "for a reduced rate because we recover value on the scrap."),
              ("Do I need to disconnect it first?",
               "Unplug it if you can. We will handle water lines and dryer vents. Gas appliances "
               "must be disconnected by a licensed gas fitter before we arrive."),
          ]),
      ]),

    P("concrete-removal-winnipeg",
      "Concrete Removal Winnipeg | Brick &amp; Heavy Material",
      "Concrete, brick, patio stone and asphalt removal in Winnipeg. Dump trailer and "
      "skid steer, priced by the tonne with scale tickets available.",
      og_image="concrete-removal.webp", crumbs=[("What We Take", "/what-we-take"), ("Concrete Removal", "/concrete-removal-winnipeg")],
      schema=[
          service_schema("Concrete Removal Winnipeg",
                         "Removal of concrete, brick, patio stone, asphalt, gravel and fill in "
                         "Winnipeg, priced by weight with scale tickets available.",
                         f"{SITE}/concrete-removal-winnipeg", "Concrete Removal"),
          faq_schema([
              ("Why is concrete priced by weight instead of by volume?",
               "Because the landfill charges us by the tonne. A half-trailer of couches might weigh "
               "400 lbs; a half-trailer of concrete can weigh over 6,000 lbs. Charging the same for "
               "both would mean overcharging you for the couches."),
              ("Can I see the scale ticket?",
               "Yes. Ask and we will show you. On commercial jobs we provide scale tickets and "
               "disposal documentation as a matter of course."),
              ("Do you break up the concrete as well as haul it?",
               "Yes. We bring a skid steer for driveways, sidewalks, patio pads and footings, so "
               "breakout and haul-away happen in the same visit."),
              ("Where does the concrete end up?",
               "At a construction and demolition facility for processing and reuse where possible, "
               "rather than straight into landfill."),
          ]),
      ]),

    # ---- The nine remaining What We Take categories -----------------------
    P("furniture-removal-winnipeg",
      "Furniture Removal Winnipeg | Couches, Sectionals &amp; Sofa Beds",
      "Couches, sectionals, sofa beds, dressers, tables and carpet carried out and hauled "
      "away in Winnipeg. Anything still usable goes to local charities first.",
      og_image="furniture-removal.webp", crumbs=[("What We Take", "/what-we-take"), ("Furniture Removal", "/furniture-removal-winnipeg")],
      schema=[
          service_schema("Furniture Removal Winnipeg",
                         "Removal of couches, sectionals, sofa beds, dressers, tables, desks and "
                         "carpet from homes and apartments in Winnipeg, including stairs and "
                         "tight-access carries.",
                         f"{SITE}/furniture-removal-winnipeg", "Furniture Removal"),
          faq_schema([
              ("Do I have to move the furniture outside first?",
               "No. We carry it out from wherever it sits — upstairs bedroom, finished basement, "
               "third-floor walk-up. You point at it, we do the lifting. That is the service."),
              ("What happens to furniture that is still in good shape?",
               "It gets offered to local Winnipeg charities and reuse centres before anything else. "
               "A couch someone can still use is worth more donated than buried, and it keeps our "
               "landfill costs down, which is part of how the pricing works."),
              ("Can you get a sectional through a narrow doorway?",
               "Usually yes. Most sectionals come apart, and where they do not we can often take the "
               "legs and back off. Tell us the access when you book and we will bring the right tools."),
              ("Will you damage my walls or floors?",
               "We put down floor protection and pad the doorframes on interior carries. If a piece "
               "genuinely will not fit without damage, we will stop and tell you before anything "
               "gets scratched."),
          ]),
      ]),

    P("mattress-disposal-winnipeg",
      "Mattress Disposal Winnipeg | Mattress &amp; Box Spring Removal",
      "Curbside will not take mattresses and they do not fit in a car. We bag them on site "
      "and take them to a Winnipeg facility that recycles the metal and foam.",
      og_image="mattress-disposal.webp", crumbs=[("What We Take", "/what-we-take"), ("Mattress Disposal", "/mattress-disposal-winnipeg")],
      schema=[
          service_schema("Mattress Disposal Winnipeg",
                         "Removal and recycling of mattresses and box springs in Winnipeg, bagged on "
                         "site and taken to a facility that recovers the steel and foam.",
                         f"{SITE}/mattress-disposal-winnipeg", "Mattress Disposal"),
          faq_schema([
              ("Why can I not just put a mattress at the curb?",
               "City of Winnipeg garbage collection does not take mattresses or box springs with "
               "regular pickup. Left at the curb they usually just sit there, and in an alley they "
               "attract a bylaw complaint."),
              ("Do you bag them?",
               "Yes, on site before we carry them out. It keeps dust, fibres and anything living in "
               "an old mattress out of your hallway and out of our trailer."),
              ("What if the mattress has bed bugs?",
               "Tell us before we arrive. We will still take it, but it has to be sealed properly "
               "and handled separately so nothing spreads to the next job. Not telling us is how a "
               "problem becomes several people's problem."),
              ("Where does it end up?",
               "At a facility that strips the steel springs for scrap and the foam and fibre for "
               "recycling, rather than straight to the landfill."),
          ]),
      ]),

    P("e-waste-removal-winnipeg",
      "E-Waste &amp; TV Removal Winnipeg | Certified Recycling",
      "TVs, monitors, computers, printers and satellite dishes collected in Winnipeg and "
      "taken to a certified EPRA Manitoba recycler, not the dump.",
      og_image="e-waste.webp", crumbs=[("What We Take", "/what-we-take"), ("E-Waste Removal", "/e-waste-removal-winnipeg")],
      schema=[
          service_schema("E-Waste and Electronics Removal Winnipeg",
                         "Collection of televisions, monitors, computers, printers, cables and "
                         "satellite dishes in Winnipeg for certified EPRA Manitoba e-waste recycling.",
                         f"{SITE}/e-waste-removal-winnipeg", "Electronics Recycling"),
          faq_schema([
              ("What counts as e-waste?",
               "Televisions, monitors, desktops, laptops, printers, scanners, stereo equipment, "
               "cables, keyboards, satellite dishes and most things with a circuit board in them."),
              ("What happens to the data on my old computer?",
               "We do not wipe drives, and you should not assume anyone else will either. Pull the "
               "hard drive out before we take the tower, or physically destroy it. That is the only "
               "advice we will give you that we can actually stand behind."),
              ("Is it true you cannot put a TV in the garbage?",
               "Correct. Most electronics are banned from Manitoba landfills because of the lead, "
               "mercury and flame retardants in them. They have to go to a certified recycler."),
              ("Do you take old tube TVs?",
               "Yes. The big CRT sets are the heaviest and most awkward thing in this category, and "
               "they are exactly the reason people call rather than deal with it themselves."),
          ]),
      ]),

    P("renovation-debris-removal-winnipeg",
      "Renovation Debris Removal Winnipeg | Reno Waste Hauling",
      "Drywall, lumber, shingles, plaster, lathe and tile hauled away in Winnipeg on a "
      "schedule that fits your build. Repeat pickups available.",
      og_image="renovation-debris.webp", crumbs=[("What We Take", "/what-we-take"),
              ("Renovation Debris", "/renovation-debris-removal-winnipeg")],
      schema=[
          service_schema("Renovation and Construction Debris Removal Winnipeg",
                         "Removal of drywall, lumber, shingles, ceiling tile, plaster, lathe and tile "
                         "from renovation and construction sites in Winnipeg, scheduled around the build.",
                         f"{SITE}/renovation-debris-removal-winnipeg", "Construction Debris Removal"),
          faq_schema([
              ("Is this cheaper than renting a bin?",
               "It depends on the job. A bin makes sense if you are producing debris steadily for "
               "weeks. We make more sense for a defined pile, a job with no room for a bin on the "
               "driveway, or a site where a bin would sit half-empty for a month collecting the "
               "neighbourhood's garbage."),
              ("Can you come back more than once?",
               "Yes. On longer renovations we schedule repeat pickups around your trades so debris "
               "never builds up to the point where people are working around it."),
              ("Do you take drywall and plaster?",
               "Yes, both, along with lathe, ceiling tile, lumber, shingles and tile. Plaster and "
               "shingles are heavy, so those get priced by weight — same as concrete."),
              ("What about asbestos?",
               "We cannot take it. Older Winnipeg homes can have it in plaster, tile and insulation. "
               "If there is any doubt, get it tested before demolition starts. We will point you to "
               "an abatement contractor rather than guess."),
          ]),
      ]),

    P("shed-deck-removal-winnipeg",
      "Shed, Deck &amp; Fence Removal Winnipeg | Teardown and Haul-Away",
      "Shed, deck and fence removal in Winnipeg. We tear it down and take it away in one "
      "visit — one contractor, one invoice. Winter teardowns spare your lawn.",
      og_image="shed-deck-removal.webp", crumbs=[("What We Take", "/what-we-take"), ("Shed &amp; Deck Removal", "/shed-deck-removal-winnipeg")],
      schema=[
          service_schema("Shed, Deck and Fence Removal Winnipeg",
                         "Demolition and haul-away of sheds, decks, fences and garages in Winnipeg, "
                         "completed in a single visit with the site left clean.",
                         f"{SITE}/shed-deck-removal-winnipeg", "Demolition and Removal"),
          faq_schema([
              ("Do you take the concrete pad or footings too?",
               "We can. Pads, deck footings and post bases all come out with the skid steer. It gets "
               "priced by weight because it is concrete, so say so when you book and it goes in the "
               "quote instead of becoming a surprise."),
              ("Will it wreck my lawn?",
               "Some marking is normal where equipment runs. We came from a landscaping company, so "
               "we plan the approach around access and drainage rather than driving straight across "
               "the middle of your yard. Frozen ground in winter is genuinely the gentlest time."),
              ("Do I need a permit?",
               "For a straightforward shed, deck or fence teardown on residential property, usually "
               "not. Detached garages and anything structural can be different — check with the "
               "City of Winnipeg first, because that is on the property owner, not the hauler."),
              ("What about the fence posts set in concrete?",
               "They come out with the post and concrete plug attached. Leaving broken posts in the "
               "ground is how the next person building a fence ends up with a bad day."),
          ]),
      ]),

    P("yard-waste-removal-winnipeg",
      "Yard Waste Removal Winnipeg | Brush &amp; Storm Cleanup",
      "Branches, brush, sod, leaves and storm damage hauled to composting and organics "
      "facilities. The crossover with our Winnipeg landscaping side.",
      og_image="yard-waste.webp", crumbs=[("What We Take", "/what-we-take"), ("Yard Waste", "/yard-waste-removal-winnipeg")],
      schema=[
          service_schema("Yard Waste and Brush Removal Winnipeg",
                         "Removal of branches, brush, sod, leaves and storm debris in Winnipeg, taken "
                         "to composting and organics facilities.",
                         f"{SITE}/yard-waste-removal-winnipeg", "Yard Waste Removal"),
          faq_schema([
              ("How is this different from the City's yard waste pickup?",
               "The City takes bagged leaves and grass on a schedule. It does not take a downed "
               "tree, a hedge you just tore out, or forty feet of brush pile. That is the gap we fill."),
              ("Do you cut the branches down as well?",
               "We handle brush, hedges and small trees. Anything requiring a climber or a bucket "
               "truck is an arborist's job, and we will tell you that rather than take a run at it."),
              ("Can you take sod and dirt?",
               "Yes, but they are heavy and get priced by weight rather than trailer space. A "
               "half-trailer of sod weighs far more than a half-trailer of branches."),
              ("Do you do storm cleanup?",
               "Yes, and it is usually the busiest week of our year when a big one comes through. "
               "Call early — after a major storm the whole city calls at once."),
          ]),
      ]),

    P("estate-cleanout-winnipeg",
      "Estate &amp; Hoarding Cleanouts Winnipeg | No BS",
      "Estate and hoarding cleanouts in Winnipeg. Whole houses, garages and storage units "
      "cleared at your pace, with anything you want kept set aside.",
      og_image="garage-cleanout.webp", crumbs=[("What We Take", "/what-we-take"), ("Estate Cleanouts", "/estate-cleanout-winnipeg")],
      schema=[
          service_schema("Estate and Hoarding Cleanout Winnipeg",
                         "Full property cleanouts in Winnipeg for estates, hoarding situations, "
                         "landlord turnovers and realtor listings, with donation sorting and photo "
                         "documentation on completion.",
                         f"{SITE}/estate-cleanout-winnipeg", "Estate Cleanout"),
          faq_schema([
              ("How do you handle things that might matter to the family?",
               "We work at your pace and set aside anything you flag. Paperwork, photographs and "
               "small personal items get put in one place rather than thrown in the trailer. If you "
               "are not sure about something, we leave it out and ask."),
              ("Can you do this if I do not live in Winnipeg?",
               "Yes. This is common with estates. We can walk the property on video, quote from "
               "that, and send photos on completion so you have documentation without flying in."),
              ("Do you handle hoarding situations?",
               "Yes, and without commentary. What we will say honestly: if there is significant "
               "biohazard, mould or pest infestation, that needs a specialist remediation company "
               "before or alongside us, and we will tell you straight rather than take the job and "
               "make it worse."),
              ("What about items with resale value?",
               "We are not an auction house and we will not pretend to value anything. Get an "
               "estate appraiser through before we start if you think there is something worth "
               "money — once it is in the trailer that decision is made."),
          ]),
      ]),

    P("scrap-metal-removal-winnipeg",
      "Scrap Metal Removal Winnipeg | Free on Full Loads",
      "Appliances, lawnmowers, fencing, bed frames, pipe and rims collected in Winnipeg. "
      "Full metal loads may be reduced or free, because we recover value.",
      og_image="scrap-metal.webp", crumbs=[("What We Take", "/what-we-take"), ("Scrap Metal", "/scrap-metal-removal-winnipeg")],
      schema=[
          service_schema("Scrap Metal and Tire Removal Winnipeg",
                         "Collection of scrap metal, appliances, lawnmowers, fencing, pipe and tires "
                         "in Winnipeg, with recovery through local scrap yards and the Tire "
                         "Stewardship Manitoba network.",
                         f"{SITE}/scrap-metal-removal-winnipeg", "Scrap Metal Removal"),
          faq_schema([
              ("Is scrap metal removal really free?",
               "Sometimes. If the load is all metal and there is enough of it, the scrap value can "
               "cover the job — so we can cut the price or take it for nothing. A single rusty "
               "barbecue is not that load. It costs nothing to ask, and we will give you a straight "
               "answer either way."),
              ("What counts as scrap metal?",
               "Appliances, lawnmowers, BBQs, bed frames, fencing, eavestrough, pipe, rims, filing "
               "cabinets, exercise equipment and most things that are mostly steel or aluminium."),
              ("Do you take tires?",
               "Yes. They go through the Tire Stewardship Manitoba network rather than the landfill. "
               "Tires on rims are fine — the rim is scrap metal anyway."),
              ("Will you take a vehicle?",
               "No. A car needs a licensed auto recycler who can handle the fluids, the battery and "
               "the ownership transfer properly. We will point you to one."),
          ]),
      ]),

    P("piano-removal-winnipeg",
      "Piano Removal Winnipeg | Pianos, Safes &amp; Awkward Heavy Items",
      "An upright piano is 400-800 lbs of cast iron in a wooden box and it is not a "
      "two-person job. Neither is a safe, a pool table or a cast iron tub.",
      og_image="piano-removal.webp", crumbs=[("What We Take", "/what-we-take"), ("Piano Removal", "/piano-removal-winnipeg")],
      schema=[
          service_schema("Piano and Odd-Item Removal Winnipeg",
                         "Removal of pianos, safes, pool tables, cast iron tubs and other heavy "
                         "awkward items from Winnipeg homes, including stairs and tight access.",
                         f"{SITE}/piano-removal-winnipeg", "Piano Removal"),
          faq_schema([
              ("How heavy is a piano really?",
               "An upright runs 400 to 800 lbs, a baby grand 500 to 700, and a full grand can pass "
               "1,000. Almost all of that is a cast iron plate. It is not a case of getting enough "
               "friends together — it is a case of the wrong technique breaking a foot or a floor."),
              ("Can my piano be donated instead?",
               "Be realistic: most old uprights have no resale or donation value, and schools and "
               "churches turn them down routinely. If yours is genuinely playable and in tune, try "
               "to rehome it first. If it has been in a damp basement for fifteen years, it is a "
               "removal job."),
              ("Can you get it down a flight of stairs?",
               "Yes. Stairs are the normal case, not the hard one. Tell us how many flights and how "
               "tight the turns are when you book so we send enough people."),
              ("What other odd items do you take?",
               "Safes, pool tables, cast iron tubs, hot water tanks, treadmills, arcade cabinets, "
               "commercial kitchen equipment. If it is heavy, awkward and everyone else said no, "
               "that is usually why people call us."),
          ]),
      ]),

    P("commercial-junk-removal-winnipeg",
      "Commercial Junk Removal &amp; Skid Steer Services Winnipeg",
      "Skid steer and dump trailer for commercial lot cleanups, construction debris, "
      "concrete and demolition in Winnipeg. Contractor accounts available.",
      crumbs=[("Commercial", "/commercial-junk-removal-winnipeg")],
      schema=[
          service_schema("Commercial Junk Removal and Skid Steer Services Winnipeg",
                         "Commercial lot cleanups, construction and renovation debris removal, "
                         "concrete and aggregate removal, structure demolition and turnover "
                         "cleanouts in Winnipeg, with skid steer and dump trailer.",
                         f"{SITE}/commercial-junk-removal-winnipeg",
                         "Commercial Junk Removal"),
      ]),

    P("winter-services-winnipeg",
      "Winter Junk Removal &amp; Snow Hauling Winnipeg",
      "We do not disappear in November. Snow removal and off-site snow hauling, winter "
      "basement and garage cleanouts, and off-season demolition in Winnipeg.",
      og_image="plow_truck.webp",
      crumbs=[("Winter Services", "/winter-services-winnipeg")],
      schema=[
          service_schema("Snow Removal and Winter Junk Removal Winnipeg",
                         "Residential and commercial snow removal with off-site snow hauling, "
                         "winter cleanouts, and off-season demolition in Winnipeg.",
                         f"{SITE}/winter-services-winnipeg", "Snow Removal"),
      ]),

    P("about",
      "About No BS Junk Removal | Winnipeg Hauling Crew",
      "We are new. We are not new at this. No BS Junk Removal is the hauling arm of "
      "No-BS Yardwork — same owners, same crews, same standards, bigger trailer.",
      # Not the headshot: that file is now sized for its 140px circle, and a
      # 280px square is far below the 1200x630 a share preview needs.
      og_image=OG_CARD,
      crumbs=[("About", "/about")]),

    P("where-your-junk-goes",
      "Where Your Junk Actually Goes | No BS Junk Removal Winnipeg",
      "Every junk removal company says they recycle. Almost none say what that means. "
      "Here is where your furniture, metal, e-waste and appliances end up.",
      crumbs=[("About", "/about"), ("Where Your Junk Goes", "/where-your-junk-goes")]),

    P("reviews",
      "Reviews | No BS Junk Removal Winnipeg",
      "What Winnipeg says about No-BS. Real reviews from our landscaping side while the "
      "junk removal division collects its own — clearly labelled, nothing invented.",
      crumbs=[("Reviews", "/reviews")]),

    P("quote",
      "Get a Free Junk Removal Quote | Winnipeg | No BS",
      "Three ways to get a price: text us a photo, call a real person seven days a week, "
      "or fill out the form. No obligation, no pressure, no sales script.",
      crumbs=[("Get a Quote", "/quote")]),

    P("thanks", "Request Received | No BS Junk Removal Winnipeg",
      "Thanks — we have your request and we will get back to you the same day.",
      robots="noindex, follow"),

    P("404", "Page Not Found | No BS Junk Removal Winnipeg",
      "That page does not exist. Here is where to go instead.",
      robots="noindex, follow"),
]


# ---------------------------------------------------------------------------
# Blog
# ---------------------------------------------------------------------------
# A post is defined once, here. Its prose lives in _pages/blog/<slug>.html —
# the same fragment split the rest of the site already uses.
#
# Everything else about a post is derived from this list: the index card, the
# BlogPosting schema, the breadcrumb, the sitemap entry and its lastmod, the
# RSS item, and the related-posts strip. That is deliberate. The usual way a
# small blog rots is the index and the feed drifting out of step with the posts
# because each is maintained by hand. Here there is nothing to keep in sync.
#
# Posts sit in a real /blog/ subdirectory, so they carry base="../" — see
# render_nav() for why the site stays on relative paths rather than switching
# to root-relative ones.
# ---------------------------------------------------------------------------

# Attributed to the business rather than to Stephano or Ben by name. These are
# company operating policies, and putting first-person opinions in a real
# person's mouth is theirs to opt into, not mine. To switch to a named author,
# change this and the "author" block in blog_posting_schema() to
# {"@type": "Person", "name": "..."}.
BLOG_AUTHOR = "No BS Junk Removal"

_MONTHS = ("January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December")


def pretty_date(iso):
    """2026-08-10 -> 10 August 2026."""
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} {_MONTHS[m - 1]} {y}"


def BP(slug, title, h1, crumb, description, date, excerpt, read_min, tags,
       og_image=OG_CARD, updated=None):
    """Define one blog post. `slug` is the bare name; the URL is /blog/<slug>."""
    return {
        "slug": slug, "title": title, "h1": h1, "crumb": crumb,
        "description": description, "date": date, "updated": updated or date,
        "excerpt": excerpt, "read_min": read_min, "tags": tags,
        "og_image": og_image,
    }


POSTS = [
    BP("junk-removal-cost-winnipeg",
       "What Junk Removal Actually Costs in Winnipeg | No BS",
       "What junk removal actually costs in Winnipeg",
       "What It Costs",
       "How junk removal is priced in Winnipeg: volume versus weight, what a real "
       "quote includes, and the add-ons some companies mention once the truck "
       "is loaded.",
       "2026-08-10",
       "Most jobs in this city are quoted one way and billed another. Here is how "
       "volume pricing actually works, and the five add-ons worth asking about before "
       "anyone loads a thing.",
       7, ["pricing"]),

    BP("dumpster-rental-vs-junk-removal-winnipeg",
       "Dumpster Rental vs Junk Removal in Winnipeg | No BS",
       "Dumpster rental vs junk removal: which do you actually need?",
       "Bin or Crew",
       "An honest comparison of bin rental and junk removal for Winnipeg homeowners, "
       "including the jobs where renting a dumpster is genuinely the cheaper call.",
       "2026-07-28",
       "We do junk removal for a living and we will still tell you when to rent a bin "
       "instead. The honest breakdown — including the permit nobody mentions.",
       8, ["pricing", "renovation"]),

    BP("why-concrete-costs-more-than-couches",
       "Why Concrete Costs More to Remove Than a Couch | No BS",
       "Why a half-load of concrete costs more than a full load of couches",
       "Weight vs Volume",
       "Heavy material is priced by weight rather than volume because the landfill "
       "bills by the tonne. Here is the arithmetic, with real trailer weights.",
       "2026-07-14",
       "A half-trailer of couches weighs about 400 lbs. A half-trailer of concrete can "
       "pass 6,000 lbs. Same space, completely different cost — here is why.",
       5, ["pricing", "renovation"]),

    BP("hot-tub-removal-what-to-expect",
       "Hot Tub Removal in Winnipeg: What Actually Happens | No BS",
       "Hot tub removal: what actually happens on the day",
       "Hot Tub Day",
       "A step-by-step account of how a hot tub gets drained, disconnected, cut down "
       "and hauled out of a Winnipeg backyard — including tight access and raised decks.",
       "2026-06-30",
       "Draining, disconnecting, cutting it down, and getting it through a 32-inch gate "
       "without taking the fence with it. What the day looks like, start to finish.",
       6, ["how-it-works"]),

    BP("estate-cleanout-checklist-winnipeg",
       "Estate Cleanout in Winnipeg: A Timeline That Works | No BS",
       "Clearing a parent's house: a timeline that actually works",
       "Estate Cleanouts",
       "A practical, unhurried order of operations for an estate cleanout in Winnipeg — "
       "what to do first, what to never throw out, and where most families get stuck.",
       "2026-06-16",
       "The hardest part is not the hauling, it is the deciding. Here is the order we "
       "have watched families get through this in without regretting anything.",
       9, ["estate", "how-it-works"]),

    BP("what-happens-to-your-junk-winnipeg",
       "Where Your Junk Actually Goes After We Load It | No BS",
       "Where your junk actually goes after we drive away",
       "Where It Goes",
       "Every hauler in Winnipeg says they recycle. Here is what that means at our "
       "shop — what gets donated, what gets scrapped, and what genuinely has to be buried.",
       "2026-05-26",
       "&ldquo;We recycle&rdquo; is the easiest sentence in this industry to say and "
       "the hardest to check. So here is the sorting, category by category.",
       6, ["recycling"]),

    BP("winter-junk-removal-winnipeg",
       "Winter Junk Removal in Winnipeg: What Changes | No BS",
       "What changes when you haul junk at &minus;30",
       "Winter Hauling",
       "Frozen piles, ice-locked sheds and snow-buried yards change how junk removal "
       "works in a Winnipeg winter. What we can still do, and what genuinely has to wait.",
       "2026-05-12",
       "Half of what makes a winter job slow is invisible in October. What actually "
       "changes once the ground freezes, and what we can still take.",
       6, ["winter"]),

    BP("prepare-for-junk-removal-day",
       "How to Prep for Junk Removal Day and Pay Less | No BS",
       "Ten minutes of prep that can cut your bill",
       "Prep Day",
       "Simple things you can do before the trailer arrives that reduce what a Winnipeg "
       "junk removal job costs — and the ones that make no difference at all.",
       "2026-04-28",
       "You are paying for space and for time. Here is what actually moves the needle "
       "on both, and which bits of helpful prep are a waste of your Saturday.",
       5, ["pricing", "how-it-works"]),
]


def blog_posting_schema(post):
    url = f"{SITE}/blog/{post['slug']}"
    return {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": strip_tags(post["h1"]),
        "description": post["description"],
        "datePublished": post["date"],
        "dateModified": post["updated"],
        "url": url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "image": f"{SITE}/images/{post['og_image']}",
        "author": {"@type": "Organization", "name": BLOG_AUTHOR, "url": SITE + "/"},
        "publisher": {
            "@type": "Organization",
            "name": "No BS Junk Removal",
            "url": SITE + "/",
            "logo": {"@type": "ImageObject", "url": f"{SITE}/images/logo-badge.png"},
        },
        "isPartOf": {"@type": "Blog", "name": "No BS Junk Removal Blog",
                     "@id": f"{SITE}/blog"},
    }


def related_posts(post, limit=3):
    """Other posts, most shared tags first, then newest.

    Ranking by shared-tag count keeps the strip relevant without a
    hand-maintained "related" list hanging off every post.
    """
    others = [p for p in POSTS if p["slug"] != post["slug"]]
    return sorted(
        others,
        key=lambda p: (-len(set(p["tags"]) & set(post["tags"])), p["date"]),
    )[:limit]


# {BASE} is left in place for subst() to fill at write time, which is why this
# is a plain template rather than an f-string.
POST_CARD = """
            <div class="col-lg-4 col-md-6">
              <article class="post-card">
                <p class="post-card-meta">
                  <time datetime="{DATE}">{DATE_PRETTY}</time>
                  <span aria-hidden="true">&middot;</span> {READ} min read
                </p>
                <{LEVEL}><a href="{BASE}blog/{SLUG}.html">{H1}</a></{LEVEL}>
                <p>{EXCERPT}</p>
                <span class="post-card-more" aria-hidden="true">Read it &rarr;</span>
              </article>
            </div>"""


def render_post_card(post, level="h3"):
    """One post card. `level` is the heading level its title takes.

    The same card appears in two places at different depths: on the blog index
    the cards ARE the page content, so they sit directly under the h1 and must
    be h2. In the "More from the blog" strip at the foot of a post they sit
    under an h2, so there they are h3. One template, correct outline in both.
    """
    return subst(POST_CARD, {
        "DATE": post["date"], "DATE_PRETTY": pretty_date(post["date"]),
        "READ": post["read_min"], "SLUG": post["slug"],
        "H1": post["h1"], "EXCERPT": post["excerpt"], "LEVEL": level,
    })


POST_BODY = """      <div class="page-header">
        <div class="container">
          <div class="row align-items-center">
            <div class="col-lg-12">
              <div class="page-header-box">
                <h1>{H1}</h1>
                <nav aria-label="Breadcrumb">
                  <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="{BASE}index.html">Home</a></li>
                    <li class="breadcrumb-item"><a href="{BASE}blog/index.html">Blog</a></li>
                    <li class="breadcrumb-item" aria-current="page">{CRUMB}</li>
                  </ol>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>

      <article class="section-space blog-post">
        <div class="container">
          <div class="row justify-content-center">
            <div class="col-lg-8">
              <p class="post-meta">
                Published <time datetime="{DATE}">{DATE_PRETTY}</time>
                <span aria-hidden="true">&middot;</span> {READ} min read
                <span aria-hidden="true">&middot;</span> {AUTHOR}
              </p>

{CONTENT}

              <div class="post-cta">
                <h3>Want a price for your own pile?</h3>
                <p>
                  Text a photo and we will quote it, or call and talk to one of the
                  people who will actually be doing the work.
                </p>
                <div class="btn-row">
                  <a href="{BASE}quote.html" class="btn-default">Get a free quote</a>
                  <a href="tel:{PHONE_TEL}" class="btn-default btn-ghost on-light">{PHONE_DISPLAY}</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </article>

      <section class="section-space bg-tint">
        <div class="container">
          <div class="section-title text-center">
            <p class="eyebrow">Keep reading</p>
            <h2>More from the blog</h2>
          </div>
          <div class="row g-4">{RELATED}
          </div>
        </div>
      </section>
"""


BLOG_INDEX_BODY = """      <div class="page-header">
        <div class="container">
          <div class="row align-items-center">
            <div class="col-lg-12">
              <div class="page-header-box">
                <h1>Advice from the people who actually haul it</h1>
                <nav aria-label="Breadcrumb">
                  <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="{BASE}index.html">Home</a></li>
                    <li class="breadcrumb-item" aria-current="page">Blog</li>
                  </ol>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>

      <section class="section-space">
        <div class="container">
          <div class="row justify-content-center">
            <div class="col-lg-9">
              <p class="lead-in" style="margin-bottom: 46px">
                No filler and no keyword soup. These are the questions we get asked on
                quotes often enough that it was worth writing the answers down &mdash;
                what things cost, what we can and cannot take, and how the awkward jobs
                actually go.
              </p>
            </div>
          </div>
          <div class="row g-4">{CARDS}
          </div>
        </div>
      </section>
"""


def render_blog_index(_base=None):
    return subst(BLOG_INDEX_BODY, {
        "CARDS": "".join(render_post_card(p, "h2") for p in POSTS),
    })


def make_post_renderer(post):
    def render(_base=None):
        frag = PAGES_DIR / "blog" / f"{post['slug']}.html"
        if not frag.exists():
            raise SystemExit(f"missing post fragment: {frag}")
        return subst(POST_BODY, {
            "H1": post["h1"], "CRUMB": post["crumb"],
            "DATE": post["date"], "DATE_PRETTY": pretty_date(post["date"]),
            "READ": post["read_min"], "AUTHOR": BLOG_AUTHOR,
            "CONTENT": frag.read_text(encoding="utf-8").rstrip("\n"),
            "RELATED": "".join(render_post_card(p) for p in related_posts(post)),
        })
    return render


# Blog pages join the same PAGES list, so the page loop, the sitemap and every
# verification pass treat them exactly like any other page — no parallel
# code path that could rot separately.
PAGES.append(P(
    "blog/index",
    "Junk Removal Advice for Winnipeg | No BS Junk Removal Blog",
    "Straight answers on junk removal in Winnipeg: what it costs, how heavy material "
    "is priced, bin rental versus a crew, estate cleanouts and winter hauling.",
    crumbs=[("Blog", "/blog")],
    base="../",
    priority="0.80",
    lastmod=max(p["updated"] for p in POSTS),
    render=render_blog_index,
))

for _post in POSTS:
    PAGES.append(P(
        f"blog/{_post['slug']}",
        _post["title"],
        _post["description"],
        og_image=_post["og_image"],
        crumbs=[("Blog", "/blog"),
                (strip_tags(_post["h1"]), f"/blog/{_post['slug']}")],
        schema=[blog_posting_schema(_post)],
        base="../",
        og_type="article",
        body_class="blog-single",
        lastmod=_post["updated"],
        priority="0.70",
        render=make_post_renderer(_post),
    ))


# ---------------------------------------------------------------------------
def faq_accordion(pairs, slug):
    """Render the visible FAQ accordion from the same data as the FAQPage schema.

    Google requires FAQ structured data to match what the visitor can actually
    see. Hand-writing the accordion separately from the schema is how those two
    silently drift apart, so both come from one list.
    """
    # Native <details>: opens and closes with no JavaScript, is keyboard and
    # screen-reader accessible by default, and the answer text is in the DOM
    # (so Google still reads it) whether or not it is expanded.
    items = []
    for i, (q, a) in enumerate(pairs, start=1):
        items.append(f"""
                <details class="faq-item" id="faq{i}-{slug}"{' open' if i == 1 else ''}>
                  <summary><h3>{q}</h3></summary>
                  <div class="faq-body">{a}</div>
                </details>""")
    return (f'<div class="faq" id="faq-{slug}">'
            + "".join(items) + "\n              </div>")


def subst(text, mapping):
    """Token replacement for chrome and page fragments.

    Deliberately plain string replacement rather than str.format: fragments
    contain literal braces (inline JSON, the JotForm embed), and format()
    would choke on every one of them.
    """
    for key, value in mapping.items():
        text = text.replace("{" + key + "}", str(value))
    return text


def strip_html_ext(text):
    """Rewrite internal .html hrefs to the canonical extensionless form.

    Every canonical, breadcrumb and sitemap entry is extensionless (clean_url),
    while fragments and NAV are written with .html so they stay readable and
    greppable as plain files. Without this rewrite every internal link costs a
    301 through the .htaccess strip rule, on every click and every crawl hop.

    Directory indexes need the care: "index.html" has to become "./" and not
    "", which would point at the current page instead of the site root.
    """
    def sub(m):
        path, suffix = m.group(1), m.group(2) or ""
        if path.startswith(("http://", "https://", "mailto:", "tel:", "sms:")):
            return m.group(0)
        trimmed = (path[: -len("index.html")] if path.endswith("index.html")
                   else path[: -len(".html")])
        return f'href="{trimmed or "./"}{suffix}"'

    return re.sub(r'href="([^"#?]+\.html)([#?][^"]*)?"', sub, text)


def build_chrome(base, common, current=""):
    """Header and footer rendered for one directory depth and one page.

    Cached on (base, current) by the caller: the chrome only differs between
    pages by which nav item carries aria-current, so pages in the same depth
    that are not in the nav share one build.
    """
    nav_html = render_nav(base, current)
    footer_links = "".join(
        f'<li><a href="{base}{h}">{l}</a></li>' for l, h in FOOTER_LINKS
    )
    scoped = dict(common, BASE=base)
    return (
        strip_html_ext(subst(HEADER.replace("{NAV}", nav_html), scoped)),
        strip_html_ext(subst(FOOTER.replace("{FOOTER_LINKS}", footer_links), scoped)),
    )


def asset_version(relpath):
    """A cache-busting version derived from the file's own contents.

    .htaccess tells browsers to keep CSS and JS for a year, which is right for
    files whose URL changes when they do. The ?v=2 that used to be typed here
    by hand did not: the mobile-menu fix shipped new CSS and new JS under the
    same URL, and any browser that had the old pair would have kept it. A
    content hash cannot be forgotten — edit the file, the URL changes.
    """
    data = (ROOT / relpath).read_bytes()
    return hashlib.sha1(data).hexdigest()[:8]


def sync_robots():
    """Keep robots.txt's host in step with SITE.

    robots.txt is hand-written — the crawler list and the reasoning in it are
    not worth generating — but its two host-bearing lines drifted the moment
    SITE changed from www to the bare domain, and nothing caught it. This
    rewrites those two lines on every build so they cannot disagree again.
    """
    p = ROOT / "robots.txt"
    if not p.exists():
        return
    host = SITE.split("//", 1)[1]
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.startswith("Sitemap:"):
            line = f"Sitemap: {SITE}/sitemap.xml"
        elif line.startswith("# ") and line[2:].strip().endswith("no-bsjunk.com"):
            line = f"# {host}"
        out.append(line)
    p.write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    common = dict(
        PHONE_TEL=PHONE_TEL, PHONE_DISPLAY=PHONE_DISPLAY, PHONE_E164=PHONE_E164,
        EMAIL=EMAIL, SITE=SITE, GTM_ID=GTM_ID, GA4_ID=GA4_ID,
        JOTFORM_ID=JOTFORM_ID,
        CSS_V=asset_version("css/junk.css"),
        JS_V=asset_version("js/site.js"),
    )
    chrome = {}

    written = 0
    for page in PAGES:
        slug = page["slug"]
        base = page.get("base", "")
        # Blog posts live one level down; their slugs carry the "blog/" prefix
        # the nav hrefs use, so they match the nav's Blog entry directly.
        key = (base, slug)
        if key not in chrome:
            chrome[key] = build_chrome(base, common, slug)
        header, footer = chrome[key]
        if page.get("render"):
            raw = page["render"](base)
        else:
            frag = PAGES_DIR / f"{slug}.html"
            if not frag.exists():
                raise SystemExit(f"missing page fragment: {frag}")
            raw = frag.read_text(encoding="utf-8")
        body = strip_html_ext(subst(expand_take_tokens(raw, slug), dict(common, BASE=base)))

        # Fill {FAQ_ACCORDION} from this page's FAQPage block, so the visible
        # questions and the structured data are always the same text.
        if "{FAQ_ACCORDION}" in body:
            faqs = next((b for b in page["schema"] if b.get("@type") == "FAQPage"), None)
            if faqs is None:
                raise SystemExit(f"{slug}: uses {{FAQ_ACCORDION}} but defines no FAQ schema")
            pairs = [(q["name"], q["acceptedAnswer"]["text"]) for q in faqs["mainEntity"]]
            body = body.replace("{FAQ_ACCORDION}", faq_accordion(pairs, slug))

        canonical = SITE + clean_url(slug)

        # Pages carrying an FAQ are the ones an assistant is most likely to be
        # asked to read out, so they get Speakable. Added here rather than on
        # each P() so it can never be forgotten on a new FAQ page.
        if any(b.get("@type") == "FAQPage" for b in page["schema"]):
            page["schema"].append(speakable_schema(canonical))

        if page["schema"]:
            schema_html = "".join(
                '    <script type="application/ld+json">\n'
                + json.dumps(b, indent=2, ensure_ascii=False)
                + "\n    </script>\n"
                for b in page["schema"]
            )
        else:
            schema_html = ""

        # Not named `html`: that shadows the stdlib module the feed uses below.
        page_html = PAGE.format(
            title=page["title"], description=page["description"],
            canonical=canonical, og_image=page["og_image"],
            robots=page["robots"], body_class=page["body_class"],
            og_type=page.get("og_type", "website"),
            schema=schema_html, body=body,
            HEADER=header, FOOTER=footer,
            # SCRIPTS is a value passed into format(), not part of the
            # template, so its own tokens have to be filled in here.
            SCRIPTS=SCRIPTS.replace("{BASE}", base).replace("{JS_V}", common["JS_V"]),
            **dict(common, BASE=base),
        )
        out = ROOT / f"{slug}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page_html, encoding="utf-8")
        written += 1

    # Sitemap, generated from the same list so it can never drift out of sync.
    urls = []
    for page in PAGES:
        if "noindex" in page["robots"]:
            continue
        slug = page["slug"]
        loc = SITE + clean_url(slug)
        priority = page["priority"] or (
            "1.00" if slug == "index" else (
                "0.90" if slug in {"pricing", "commercial-junk-removal-winnipeg",
                                   "what-we-take", "quote"} else "0.80"))
        # Posts set lastmod explicitly. Everything else falls back to the mtime
        # of its source fragment, so all 30 entries carry a date that is
        # actually true without anyone having to remember to bump it.
        stamp = page["lastmod"]
        if not stamp:
            frag = PAGES_DIR / f"{slug}.html"
            # Generated pages (the hub, the A-Z, what we can't take) have no
            # fragment. Their content comes from the renderers in this file
            # and the data in _categories.py, so they are as fresh as the
            # newer of those two.
            sources = [frag] if frag.exists() else [ROOT / "_build.py", ROOT / "_categories.py"]
            newest = max(p.stat().st_mtime for p in sources if p.exists())
            stamp = datetime.fromtimestamp(newest, timezone.utc).strftime("%Y-%m-%d")
        lastmod = f"    <lastmod>{stamp}</lastmod>\n" if stamp else ""
        urls.append(
            f"  <url>\n    <loc>{loc}</loc>\n{lastmod}"
            f"    <changefreq>monthly</changefreq>\n"
            f"    <priority>{priority}</priority>\n  </url>"
        )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")

    # RSS. Cheap to generate from POSTS and the only thing that lets anyone
    # follow the blog without an account; readers and aggregators expect
    # RFC-822 dates, hence the fixed-format conversion rather than a locale one.
    items = []
    for post in POSTS:
        link = f"{SITE}/blog/{post['slug']}"
        y, m, d = (int(x) for x in post["date"].split("-"))
        pub = format_datetime(datetime(y, m, d, 9, 0, tzinfo=timezone.utc))
        items.append(
            "    <item>\n"
            f"      <title>{html.escape(strip_tags(post['h1']))}</title>\n"
            f"      <link>{link}</link>\n"
            f"      <guid isPermaLink=\"true\">{link}</guid>\n"
            f"      <pubDate>{pub}</pubDate>\n"
            f"      <description>{html.escape(strip_tags(post['excerpt']))}</description>\n"
            "    </item>"
        )
    (ROOT / "feed.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        "    <title>No BS Junk Removal — Winnipeg</title>\n"
        f"    <link>{SITE}/blog</link>\n"
        "    <description>Straight answers on junk removal in Winnipeg.</description>\n"
        "    <language>en-ca</language>\n"
        f'    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml" />\n'
        + "\n".join(items)
        + "\n  </channel>\n</rss>\n", encoding="utf-8")

    # -----------------------------------------------------------------
    # llms.txt — generated, not hand-written.
    #
    # The hand-maintained version had already drifted: it listed none of the
    # eight blog posts. Deriving it from PAGES, POSTS and the FAQ data means it
    # cannot fall behind the site again.
    #
    # The Q&A block matters more than the link list. Assistants quote a passage
    # that answers the question directly, so the answers are reproduced here in
    # full rather than being linked to.
    # -----------------------------------------------------------------
    def short(title):
        return title.split(" | ")[0].strip()

    faq_pairs = []
    seen_q = set()
    for page in PAGES:
        for block in page["schema"]:
            if block.get("@type") != "FAQPage":
                continue
            for q in block["mainEntity"]:
                name = q["name"]
                if name not in seen_q:
                    seen_q.add(name)
                    faq_pairs.append((name, q["acceptedAnswer"]["text"]))

    L = []
    L.append("# no-bsjunk.com llms.txt")
    L.append("")
    L.append("> No BS Junk Removal is the junk removal and hauling division of No-BS")
    L.append("> Yardwork in Winnipeg, Manitoba. Pricing is by volume — the space your")
    L.append("> junk takes in a 14ft x 7ft x 4ft trailer — and every quote already")
    L.append("> includes labour, hauling, disposal and dump fees. Heavy material")
    L.append("> (concrete, brick, shingles, dirt) is priced by weight instead, because")
    L.append("> the landfill bills by the tonne. Call or text 204.900.0438.")
    L.append("")
    L.append("## Services")
    L.append("")
    for page in PAGES:
        if page["slug"].startswith("blog/") or "noindex" in page["robots"]:
            continue
        L.append(f"- [{short(page['title'])}]({SITE}{clean_url(page['slug'])}): {page['description']}")
    L.append("")
    L.append("## Articles")
    L.append("")
    for post in POSTS:
        L.append(f"- [{strip_tags(post['h1'])}]({SITE}/blog/{post['slug']}): {post['description']}")
    L.append("")
    L.append("## Common questions, answered")
    L.append("")
    for q, a in faq_pairs:
        L.append(f"### {q}")
        L.append("")
        L.append(a)
        L.append("")
    L.append("## Business details")
    L.append("")
    L.append("- Trading name: No BS Junk Removal, a division of No-BS Yardwork")
    L.append(f"- Phone: {PHONE_DISPLAY} (call or text)")
    L.append(f"- Email: {EMAIL}")
    L.append("- Address: Lakewood Blvd, Winnipeg, MB R2J 4A9, Canada")
    L.append("- Service area: Winnipeg and surrounding communities, including "
             "St. Vital, St. Boniface, Transcona, Charleswood, Fort Garry, "
             "River Heights, St. James, the Kildonans, Headingley and St. Paul")
    L.append("- Hours: Mon-Fri 09:00-18:00, Sat-Sun 10:00-18:00")
    L.append("- Equipment: skid steer and dump trailer (14ft x 7ft x 4ft)")
    L.append("- Parent company: No-BS Yardwork (https://www.no-bs-yardwork.com)")
    L.append("")
    # Both lists come from _categories.py, so an assistant quoting this file
    # gets the same answer a visitor gets from the site.
    L.append("## What we take")
    L.append("")
    for c in CATEGORIES:
        L.append(f"- {c['name']} ({SITE}{clean_url(c['slug'])}): "
                 + ", ".join(it["name"] for it in c["items"]))
    L.append(f"- Every item, A to Z: {SITE}{clean_url('what-we-take-a-z')}")
    L.append("")
    L.append("## What we cannot take, and where it goes instead")
    L.append("")
    for t in NOT_TAKEN:
        L.append(f"- {t['name']}: {t['why']} {t['where']}")
    L.append("")
    (ROOT / "llms.txt").write_text("\n".join(L), encoding="utf-8")
    sync_robots()

    print(f"built {written} pages + sitemap.xml + feed.xml + llms.txt ({len(POSTS)} posts, {len(faq_pairs)} FAQs)")


if __name__ == "__main__":
    main()
