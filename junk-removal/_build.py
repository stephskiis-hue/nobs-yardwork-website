#!/usr/bin/env python3
"""
_build.py — assembles the static pages for no-bs-junkremoval.com.

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

import html
import json
import re
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path


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

SITE = "https://www.no-bs-junkremoval.com"
PHONE_DISPLAY = "204.900.0438"
PHONE_TEL = "2049000438"
PHONE_E164 = "+12049000438"
EMAIL = "nobsyardwork@gmail.com"
GTM_ID = "GTM-M3MHCKF5"
GA4_ID = "G-VN2QZ4KXXH"
JOTFORM_ID = "260105131967250"

# ---------------------------------------------------------------------------
# Nav — single source of truth. (label, href, [children])
# ---------------------------------------------------------------------------
NAV = [
    ("What We Take", "what-we-take.html", [
        # All twelve categories have their own page; the dropdown carries the
        # six most-searched and the hub page carries the full set, because a
        # thirteen-item dropdown is unusable on a laptop.
        ("All 12 Categories", "what-we-take.html"),
        ("Furniture Removal", "furniture-removal-winnipeg.html"),
        ("Appliance Removal", "appliance-removal-winnipeg.html"),
        ("Mattress Disposal", "mattress-disposal-winnipeg.html"),
        ("Hot Tub Removal", "hot-tub-removal-winnipeg.html"),
        ("Renovation Debris", "renovation-debris-removal-winnipeg.html"),
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
    "name": "No BS Junk Removal",
    "alternateName": "No-BS Yardwork Junk Removal",
    "image": f"{SITE}/images/logo.svg",
    "url": SITE + "/",
    "telephone": PHONE_E164,
    "email": EMAIL,
    "priceRange": "$$",
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
    "areaServed": {"@type": "City", "name": "Winnipeg"},
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
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}}
            for n in [
                "Furniture & Mattress Removal Winnipeg",
                "Appliance Removal Winnipeg",
                "E-Waste & Electronics Removal Winnipeg",
                "Renovation & Construction Debris Removal Winnipeg",
                "Hot Tub Removal Winnipeg",
                "Concrete & Heavy Material Removal Winnipeg",
                "Estate & Hoarding Cleanouts Winnipeg",
                "Commercial Junk Removal & Skid Steer Services Winnipeg",
                "Snow Removal & Hauling Winnipeg",
            ]
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
        "provider": {
            "@type": "LocalBusiness",
            "name": "No BS Junk Removal",
            "telephone": PHONE_E164,
            "email": EMAIL,
            "url": SITE + "/",
            "address": LOCAL_BUSINESS["address"],
            "areaServed": {"@type": "City", "name": "Winnipeg"},
        },
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

def render_nav(base=""):
    """Render the nav. `base` is the prefix that walks back up to the web root.

    Every link and asset on this site is relative, which is what lets the whole
    thing run either as its own domain or as a subfolder of no-bs-yardwork.com
    without a rebuild. Blog posts live one directory down, so they need "../"
    in front of everything; root pages need "". Switching to root-relative
    ("/css/...") would have been less code and would have broken the subfolder
    arrangement the site is currently reachable through.
    """
    out = []
    for label, href, children in NAV:
        if children:
            kids = "".join(
                f'<li class="nav-item"><a class="nav-link" href="{base}{h}">{l}</a></li>'
                for l, h in children
            )
            out.append(
                f'<li class="nav-item submenu"><a class="nav-link" href="{base}{href}">{label}</a>'
                f"<ul>{kids}</ul></li>"
            )
        else:
            out.append(
                f'<li class="nav-item"><a class="nav-link" href="{base}{href}">{label}</a></li>'
            )
    return "\n                  ".join(out)


HEADER = """    <a class="skip-link" href="#main">Skip to content</a>
    <header class="main-header">
      <div class="header-sticky">
        <nav class="navbar navbar-expand-lg">
          <div class="container">
            <a class="navbar-brand brand-lockup" href="{BASE}index.html">
              <img src="{BASE}images/logo.svg" alt="No-BS Yardwork" width="150" height="50"
                   style="height: 50px; width: auto" fetchpriority="high" />
              <span class="division-tag">Junk Removal</span>
            </a>

            <div class="collapse navbar-collapse main-menu">
              <div class="nav-menu-wrapper">
                <ul class="navbar-nav mr-auto" id="menu">
                  {NAV}
                </ul>
              </div>

              <div class="contact-now-box d-inline-flex">
                <div class="icon-box">
                  <a href="tel:{PHONE_TEL}" aria-label="Call No BS Junk Removal">
                    <img src="{BASE}images/icon-phone.svg" alt="" width="25" height="25" />
                  </a>
                </div>
                <div class="contact-now-box-content">
                  <p>Call or text any time</p>
                  <h3><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></h3>
                </div>
              </div>
            </div>
            <div class="navbar-toggle"></div>
          </div>
        </nav>
        <div class="responsive-menu"></div>
      </div>
    </header>
"""

FOOTER = """    <footer class="main-footer">
      <div class="container">
        <div class="row">
          <div class="col-lg-3 col-md-12">
            <div class="about-footer">
              <div class="footer-logo">
                <img src="{BASE}images/footer-logo.svg" alt="No BS Junk Removal Winnipeg"
                     loading="lazy" width="200" height="90" />
              </div>
              <div class="about-footer-content">
                <p>Embrace hard work, honesty and watch amazing things unfold.</p>
                <p><strong>The hauling division of
                  <a href="https://www.no-bs-yardwork.com">No-BS Yardwork</a>.</strong></p>
              </div>
              <div class="footer-social-links">
                <ul>
                  <li><a href="https://www.facebook.com/No.BS.Yardworks" target="_blank"
                         rel="noopener" aria-label="No-BS on Facebook"><i class="fab fa-facebook-f"></i></a></li>
                  <li><a href="https://www.instagram.com/no_bs_yardwork/" target="_blank"
                         rel="noopener" aria-label="No-BS on Instagram"><i class="fab fa-instagram"></i></a></li>
                </ul>
              </div>
            </div>
          </div>
          <div class="col-lg-3 col-md-4 col-6">
            <div class="footer-links">
              <h3>Explore</h3>
              <ul>{FOOTER_LINKS}</ul>
            </div>
          </div>
          <div class="col-lg-3 col-md-4 col-6">
            <div class="working-hour">
              <h3>Office hours</h3>
              <div class="working-hour-box"><p>Monday - Friday</p><p>09.00 - 6.00</p></div>
              <div class="working-hour-box"><p>Saturday</p><p>10.00 - 6.00</p></div>
              <div class="working-hour-box"><p>Sunday</p><p>10.00 - 6.00</p></div>
            </div>
          </div>
          <div class="col-lg-3 col-md-4">
            <div class="footer-contact">
              <div class="footer-info-box">
                <h3>Address</h3>
                <p>Lakewood Blvd<br />Winnipeg, MB<br />R2J 4A9</p>
              </div>
              <div class="footer-info-box">
                <h3>Contact</h3>
                <p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
                <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
              </div>
            </div>
          </div>
        </div>
        <div class="footer-copyright">
          <div class="row align-items-center">
            <div class="col-lg-8 col-md-6">
              <div class="footer-copyright-text">
                <p>&copy; No BS Junk Removal &mdash; a No-BS Yardwork company. All Rights Reserved.
                  &nbsp;&nbsp;<img src="{BASE}images/payments.webp"
                  alt="Pay by cheque, e-transfer or credit card" loading="lazy"
                  width="239" height="35" /></p>
              </div>
            </div>
            <div class="col-lg-4 col-md-6">
              <div class="footer-links">
                <p align="right" class="btn-default">
                  <a href="https://www.no-bs-yardwork.com">Visit No-BS Yardwork</a>
                </p>
              </div>
            </div>
          </div>
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

SCRIPTS = """    <script src="{BASE}js/jquery-3.7.1.min.js" defer></script>
    <script src="{BASE}js/bootstrap.min.js" defer></script>
    <!-- function.js calls $('#contactForm').validator() unconditionally; without
         this file that throws and every later handler in function.js (including
         the mobile nav) dies with it. -->
    <script src="{BASE}js/validator.min.js" defer></script>
    <script src="{BASE}js/jquery.slicknav.min.js" defer></script>
    <script src="{BASE}js/jquery.waypoints.min.js" defer></script>
    <script src="{BASE}js/jquery.counterup.min.js" defer></script>
    <script src="{BASE}js/gsap.min.js" defer></script>
    <script src="{BASE}js/SplitText.js" defer></script>
    <script src="{BASE}js/ScrollTrigger.min.js" defer></script>
    <script src="{BASE}js/function.js" defer></script>
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

    <link rel="preload" href="{BASE}css/bootstrap.min.css" as="style" onload="this.onload=null;this.rel='stylesheet';" />
    <link rel="preload" href="{BASE}css/all.min.css" as="style" onload="this.onload=null;this.rel='stylesheet';" />
    <link rel="preload" href="{BASE}css/slicknav.min.css" as="style" onload="this.onload=null;this.rel='stylesheet';" />
    <link rel="preload" href="{BASE}css/custom.css" as="style" onload="this.onload=null;this.rel='stylesheet';" />
    <link rel="preload" href="{BASE}css/junk.css?v=1" as="style" onload="this.onload=null;this.rel='stylesheet';" />
    <noscript>
      <link rel="stylesheet" href="{BASE}css/bootstrap.min.css" />
      <link rel="stylesheet" href="{BASE}css/all.min.css" />
      <link rel="stylesheet" href="{BASE}css/slicknav.min.css" />
      <link rel="stylesheet" href="{BASE}css/custom.css" />
      <link rel="stylesheet" href="{BASE}css/junk.css?v=1" />
    </noscript>

    <link rel="preload" href="{BASE}webfonts/fa-brands-400.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="preload" href="{BASE}webfonts/fa-solid-900.woff2" as="font" type="font/woff2" crossorigin />

    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag() {{ dataLayer.push(arguments); }}
      gtag("js", new Date());
      gtag("config", "{GA4_ID}");
    </script>

    <style>
      /* Mobile nav colours. Same values the parent site inlines on every page
         (#1b3d2f), so the hamburger menu matches no-bs-yardwork.com exactly. */
      .slicknav_btn {{ background-color: #1b3d2f !important; border-radius: 12px !important; }}
      .slicknav_nav {{ background-color: #1b3d2f !important; }}
      body {{ font-family: "Plus Jakarta Sans", sans-serif; background-color: #ffffff; }}
    </style>
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
        return "/" + slug[: -len("/index")]
    return "/" + slug


def P(slug, title, description, og_image="skid_steer.webp", crumbs=None,
      schema=None, robots=DEFAULT_ROBOTS, body_class="", base="",
      og_type="website", lastmod=None, priority=None, render=None):
    """Define one page.

    `render` is for pages whose body is generated rather than authored — the
    blog index and the post wrapper. It returns text still containing {TOKENS},
    which the page loop substitutes exactly as it does for a hand-written
    fragment, so generated and authored pages go through one code path.
    """
    blocks = list(schema or [])
    if crumbs is not None:
        blocks.append(breadcrumbs(crumbs))
    return {
        "slug": slug, "title": title, "description": description,
        "og_image": og_image, "schema": blocks, "robots": robots,
        "body_class": body_class, "base": base, "og_type": og_type,
        "lastmod": lastmod, "priority": priority, "render": render,
    }


PAGES = [
    P("index",
      "Junk Removal Winnipeg | No BS Junk Removal | Same-Day Service",
      "Winnipeg junk removal with upfront pricing and no hidden fees. Furniture, "
      "appliances, reno debris, hot tubs, concrete. Skid steer available. Backed by "
      "No-BS Yardwork. Free quotes — call or text today.",
      schema=[LOCAL_BUSINESS], body_class="home"),

    P("pricing",
      "Junk Removal Prices Winnipeg | Upfront Rates, No Hidden Fees",
      "See exactly what junk removal costs in Winnipeg. Labour, hauling and dump fees "
      "all included. Free on-site estimates. We even explain why heavy material is "
      "priced differently.",
      crumbs=[("Pricing", "/pricing")],
      schema=[faq_schema([
          ("How is junk removal priced in Winnipeg?",
           "You pay for the space your junk takes up in our trailer. Our trailer is 14 feet "
           "long by 7 feet wide by 4 feet high, and every price includes labour, hauling, "
           "disposal and dump fees, and a basic sweep-up when we are done."),
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
      "If it is not hazardous, we will take it. Furniture, appliances, mattresses, "
      "e-waste, renovation debris, hot tubs, sheds, concrete, yard waste, estate "
      "cleanouts, scrap metal and pianos across Winnipeg.",
      crumbs=[("What We Take", "/what-we-take")]),

    P("hot-tub-removal-winnipeg",
      "Hot Tub Removal Winnipeg | Disconnect, Breakdown &amp; Haul-Away",
      "Hot tub removal in Winnipeg. We disconnect, break it down on site and haul every "
      "piece away in one visit — without wrecking your deck, fence or lawn. Free "
      "on-site estimate.",
      crumbs=[("What We Take", "/what-we-take"), ("Hot Tub Removal", "/hot-tub-removal-winnipeg")],
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
      "Appliance Removal Winnipeg | Fridges, Freezers, Washers &amp; Furnaces",
      "Appliance removal in Winnipeg. Fridges, freezers, washers, dryers, stoves and "
      "furnaces hauled away and taken to a certified recycler — refrigerant recovered "
      "properly, as the law requires.",
      crumbs=[("What We Take", "/what-we-take"), ("Appliance Removal", "/appliance-removal-winnipeg")],
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
      "Concrete Removal Winnipeg | Brick, Patio Stone &amp; Heavy Material",
      "Concrete, brick, patio stone, asphalt and aggregate removal in Winnipeg. Weight-rated "
      "dump trailer and skid steer, priced by the tonne with scale tickets available.",
      crumbs=[("What We Take", "/what-we-take"), ("Concrete Removal", "/concrete-removal-winnipeg")],
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
      "Furniture removal in Winnipeg. Couches, sectionals, sofa beds, dressers, tables and "
      "carpet carried out and hauled away. Anything still usable is offered to local charities "
      "first. Free quotes.",
      crumbs=[("What We Take", "/what-we-take"), ("Furniture Removal", "/furniture-removal-winnipeg")],
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
      "Mattress disposal in Winnipeg. Curbside pickup will not take them and they do not fit in a "
      "car. We bag them on site and take them to a facility that strips the metal and foam for "
      "recycling.",
      crumbs=[("What We Take", "/what-we-take"), ("Mattress Disposal", "/mattress-disposal-winnipeg")],
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
      "E-Waste Removal Winnipeg | TVs, Computers &amp; Electronics Recycling",
      "E-waste removal in Winnipeg. TVs, monitors, computers, printers and satellite dishes taken "
      "to a certified EPRA Manitoba recycler — not the dump, where most of it is illegal anyway.",
      crumbs=[("What We Take", "/what-we-take"), ("E-Waste Removal", "/e-waste-removal-winnipeg")],
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
      "Renovation Debris Removal Winnipeg | Construction Waste Haul-Away",
      "Renovation and construction debris removal in Winnipeg. Drywall, lumber, shingles, plaster, "
      "lathe and tile hauled away on a schedule that fits your build. Repeat pickups available.",
      crumbs=[("What We Take", "/what-we-take"),
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
      "Shed, deck and fence removal in Winnipeg. We tear it down and take it away in one visit — "
      "one contractor, one invoice. Winter teardowns cause less lawn damage.",
      crumbs=[("What We Take", "/what-we-take"), ("Shed &amp; Deck Removal", "/shed-deck-removal-winnipeg")],
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
      "Yard Waste Removal Winnipeg | Branches, Brush &amp; Storm Cleanup",
      "Yard waste and brush removal in Winnipeg. Branches, brush, sod, leaves and storm damage "
      "hauled to composting and organics facilities. The crossover with our landscaping side.",
      crumbs=[("What We Take", "/what-we-take"), ("Yard Waste", "/yard-waste-removal-winnipeg")],
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
      "Estate Cleanout Winnipeg | Hoarding &amp; Full Property Cleanouts",
      "Estate and hoarding cleanouts in Winnipeg. Whole houses, garages and storage units cleared "
      "at your pace, with anything you want kept set aside and photos on completion.",
      crumbs=[("What We Take", "/what-we-take"), ("Estate Cleanouts", "/estate-cleanout-winnipeg")],
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
      "Scrap Metal Removal Winnipeg | Free Pickup on Full Metal Loads",
      "Scrap metal removal in Winnipeg. Appliances, lawnmowers, fencing, bed frames, pipe and rims. "
      "Full metal loads may be reduced or free, because we recover value at the yard.",
      crumbs=[("What We Take", "/what-we-take"), ("Scrap Metal", "/scrap-metal-removal-winnipeg")],
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
      "Piano removal in Winnipeg. An upright is 400-800 lbs of cast iron in a wooden box and it is "
      "not a two-person job. Neither is a safe, a pool table or a cast iron tub.",
      crumbs=[("What We Take", "/what-we-take"), ("Piano Removal", "/piano-removal-winnipeg")],
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
      "Skid steer and dump trailer for commercial lot cleanups, construction debris, concrete "
      "and full demolition in Winnipeg. Contractor accounts with net terms and priority scheduling.",
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
      "Winter Junk Removal &amp; Snow Hauling Winnipeg | No BS Junk Removal",
      "We do not disappear in November. Snow removal and off-site snow hauling, winter "
      "basement and garage cleanouts, off-season demolition and job site debris across Winnipeg.",
      og_image="plow_truck.webp",
      crumbs=[("Winter Services", "/winter-services-winnipeg")],
      schema=[
          service_schema("Snow Removal and Winter Junk Removal Winnipeg",
                         "Residential and commercial snow removal with off-site snow hauling, "
                         "winter cleanouts, and off-season demolition in Winnipeg.",
                         f"{SITE}/winter-services-winnipeg", "Snow Removal"),
      ]),

    P("about",
      "About No BS Junk Removal Winnipeg | The No-BS Yardwork Connection",
      "We are new. We are not new at this. No BS Junk Removal is the hauling arm of "
      "No-BS Yardwork — same owners, same crews, same standards, bigger trailer.",
      og_image="steph-headshot.webp",
      crumbs=[("About", "/about")]),

    P("where-your-junk-goes",
      "Where Your Junk Actually Goes | No BS Junk Removal Winnipeg",
      "Every junk removal company says they recycle. Almost none say what that means. "
      "Here is exactly where your furniture, metal, e-waste, appliances and concrete end up.",
      crumbs=[("About", "/about"), ("Where Your Junk Goes", "/where-your-junk-goes")]),

    P("reviews",
      "Reviews | No BS Junk Removal Winnipeg",
      "What Winnipeg says about No-BS. Real reviews from our landscaping side while the "
      "junk removal division collects its own — clearly labelled, nothing invented.",
      crumbs=[("Reviews", "/reviews")]),

    P("quote",
      "Get a Free Junk Removal Quote in Winnipeg | No BS Junk Removal",
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
       og_image="skid_steer.webp", updated=None):
    """Define one blog post. `slug` is the bare name; the URL is /blog/<slug>."""
    return {
        "slug": slug, "title": title, "h1": h1, "crumb": crumb,
        "description": description, "date": date, "updated": updated or date,
        "excerpt": excerpt, "read_min": read_min, "tags": tags,
        "og_image": og_image,
    }


POSTS = [
    BP("junk-removal-cost-winnipeg",
       "What Junk Removal Actually Costs in Winnipeg | No BS Junk Removal",
       "What junk removal actually costs in Winnipeg",
       "What It Costs",
       "A straight explanation of how junk removal is priced in Winnipeg — volume "
       "versus weight, what a real quote includes, and the add-ons some companies "
       "only mention once the truck is loaded.",
       "2026-08-10",
       "Most jobs in this city are quoted one way and billed another. Here is how "
       "volume pricing actually works, and the five add-ons worth asking about before "
       "anyone loads a thing.",
       7, ["pricing"]),

    BP("dumpster-rental-vs-junk-removal-winnipeg",
       "Dumpster Rental vs Junk Removal in Winnipeg | No BS Junk Removal",
       "Dumpster rental vs junk removal: which do you actually need?",
       "Bin or Crew",
       "An honest comparison of bin rental and junk removal for Winnipeg homeowners, "
       "including the jobs where renting a dumpster is genuinely the cheaper call.",
       "2026-07-28",
       "We do junk removal for a living and we will still tell you when to rent a bin "
       "instead. The honest breakdown — including the permit nobody mentions.",
       8, ["pricing", "renovation"]),

    BP("why-concrete-costs-more-than-couches",
       "Why Concrete Costs More to Remove Than a Couch | No BS Junk Removal",
       "Why a half-load of concrete costs more than a full load of couches",
       "Weight vs Volume",
       "Heavy material is priced by weight rather than volume because the landfill "
       "bills by the tonne. Here is the arithmetic, with real trailer weights.",
       "2026-07-14",
       "A half-trailer of couches weighs about 400 lbs. A half-trailer of concrete can "
       "pass 6,000 lbs. Same space, completely different cost — here is why.",
       5, ["pricing", "renovation"]),

    BP("hot-tub-removal-what-to-expect",
       "Hot Tub Removal in Winnipeg: What Actually Happens | No BS Junk Removal",
       "Hot tub removal: what actually happens on the day",
       "Hot Tub Day",
       "A step-by-step account of how a hot tub gets drained, disconnected, cut down "
       "and hauled out of a Winnipeg backyard — including tight access and raised decks.",
       "2026-06-30",
       "Draining, disconnecting, cutting it down, and getting it through a 32-inch gate "
       "without taking the fence with it. What the day looks like, start to finish.",
       6, ["how-it-works"]),

    BP("estate-cleanout-checklist-winnipeg",
       "Estate Cleanout in Winnipeg: A Timeline That Works | No BS Junk Removal",
       "Clearing a parent's house: a timeline that actually works",
       "Estate Cleanouts",
       "A practical, unhurried order of operations for an estate cleanout in Winnipeg — "
       "what to do first, what to never throw out, and where most families get stuck.",
       "2026-06-16",
       "The hardest part is not the hauling, it is the deciding. Here is the order we "
       "have watched families get through this in without regretting anything.",
       9, ["estate", "how-it-works"]),

    BP("what-happens-to-your-junk-winnipeg",
       "Where Your Junk Actually Goes After We Load It | No BS Junk Removal",
       "Where your junk actually goes after we drive away",
       "Where It Goes",
       "Every hauler in Winnipeg says they recycle. Here is what that means at our "
       "shop — what gets donated, what gets scrapped, and what genuinely has to be buried.",
       "2026-05-26",
       "&ldquo;We recycle&rdquo; is the easiest sentence in this industry to say and "
       "the hardest to check. So here is the sorting, category by category.",
       6, ["recycling"]),

    BP("winter-junk-removal-winnipeg",
       "Winter Junk Removal in Winnipeg: What Changes | No BS Junk Removal",
       "What changes when you haul junk at &minus;30",
       "Winter Hauling",
       "Frozen piles, ice-locked sheds and snow-buried yards change how junk removal "
       "works in a Winnipeg winter. What we can still do, and what genuinely has to wait.",
       "2026-05-12",
       "Half of what makes a winter job slow is invisible in October. What actually "
       "changes once the ground freezes, and what we can still take.",
       6, ["winter"]),

    BP("prepare-for-junk-removal-day",
       "How to Prep for Junk Removal Day and Pay Less | No BS Junk Removal",
       "Ten minutes of prep that can cut your bill",
       "Prep Day",
       "Simple things you can do before the trailer arrives that genuinely reduce what "
       "a Winnipeg junk removal job costs — and the ones that make no difference at all.",
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
            "logo": {"@type": "ImageObject", "url": f"{SITE}/images/logo.svg"},
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
                <h3><a href="{BASE}blog/{SLUG}.html">{H1}</a></h3>
                <p>{EXCERPT}</p>
                <span class="post-card-more" aria-hidden="true">Read it &rarr;</span>
              </article>
            </div>"""


def render_post_card(post):
    return subst(POST_CARD, {
        "DATE": post["date"], "DATE_PRETTY": pretty_date(post["date"]),
        "READ": post["read_min"], "SLUG": post["slug"],
        "H1": post["h1"], "EXCERPT": post["excerpt"],
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
            <h3>Keep reading</h3>
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
        "CARDS": "".join(render_post_card(p) for p in POSTS),
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
    "is priced, dumpster rental versus a crew, estate cleanouts, winter hauling and "
    "where your junk actually ends up.",
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
    items = []
    for i, (q, a) in enumerate(pairs, start=1):
        first = i == 1
        items.append(f"""
                <div class="accordion-item">
                  <h3 class="accordion-header" id="faq{i}h-{slug}">
                    <button class="accordion-button{'' if first else ' collapsed'}" type="button"
                            data-bs-toggle="collapse" data-bs-target="#faq{i}-{slug}"
                            aria-expanded="{'true' if first else 'false'}"
                            aria-controls="faq{i}-{slug}">
                      {q}
                    </button>
                  </h3>
                  <div id="faq{i}-{slug}"
                       class="accordion-collapse collapse{' show' if first else ''}"
                       aria-labelledby="faq{i}h-{slug}" data-bs-parent="#faqAccordion-{slug}">
                    <div class="accordion-body">{a}</div>
                  </div>
                </div>""")
    return (f'<div class="accordion" id="faqAccordion-{slug}">'
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


def build_chrome(base, common):
    """Header and footer rendered for one directory depth.

    Called once per distinct `base` ("" for root pages, "../" for /blog/), not
    once per page — the chrome is identical within a depth.
    """
    nav_html = render_nav(base)
    footer_links = "".join(
        f'<li><a href="{base}{h}">{l}</a></li>' for l, h in FOOTER_LINKS
    )
    scoped = dict(common, BASE=base)
    return (
        subst(HEADER.replace("{NAV}", nav_html), scoped),
        subst(FOOTER.replace("{FOOTER_LINKS}", footer_links), scoped),
    )


def main():
    common = dict(
        PHONE_TEL=PHONE_TEL, PHONE_DISPLAY=PHONE_DISPLAY, PHONE_E164=PHONE_E164,
        EMAIL=EMAIL, SITE=SITE, GTM_ID=GTM_ID, GA4_ID=GA4_ID,
        JOTFORM_ID=JOTFORM_ID,
    )
    chrome = {b: build_chrome(b, common) for b in ("", "../")}

    written = 0
    for page in PAGES:
        slug = page["slug"]
        base = page.get("base", "")
        header, footer = chrome[base]
        if page.get("render"):
            raw = page["render"](base)
        else:
            frag = PAGES_DIR / f"{slug}.html"
            if not frag.exists():
                raise SystemExit(f"missing page fragment: {frag}")
            raw = frag.read_text(encoding="utf-8")
        body = subst(raw, dict(common, BASE=base))

        # Fill {FAQ_ACCORDION} from this page's FAQPage block, so the visible
        # questions and the structured data are always the same text.
        if "{FAQ_ACCORDION}" in body:
            faqs = next((b for b in page["schema"] if b.get("@type") == "FAQPage"), None)
            if faqs is None:
                raise SystemExit(f"{slug}: uses {{FAQ_ACCORDION}} but defines no FAQ schema")
            pairs = [(q["name"], q["acceptedAnswer"]["text"]) for q in faqs["mainEntity"]]
            body = body.replace("{FAQ_ACCORDION}", faq_accordion(pairs, slug))

        canonical = SITE + clean_url(slug)

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
            SCRIPTS=SCRIPTS.replace("{BASE}", base),
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
        lastmod = f"    <lastmod>{page['lastmod']}</lastmod>\n" if page["lastmod"] else ""
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

    print(f"built {written} pages + sitemap.xml + feed.xml ({len(POSTS)} posts)")


if __name__ == "__main__":
    main()
