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

import json
import re
from pathlib import Path

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
        ("All Categories", "what-we-take.html"),
        ("Hot Tub Removal", "hot-tub-removal-winnipeg.html"),
        ("Appliance Removal", "appliance-removal-winnipeg.html"),
        ("Concrete &amp; Heavy Material", "concrete-removal-winnipeg.html"),
    ]),
    ("Pricing", "pricing.html", []),
    ("Commercial", "commercial-junk-removal-winnipeg.html", []),
    ("Winter", "winter-services-winnipeg.html", []),
    ("About", "about.html", [
        ("Our Story", "about.html"),
        ("Where Your Junk Goes", "where-your-junk-goes.html"),
        ("Reviews", "reviews.html"),
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

def render_nav():
    out = []
    for label, href, children in NAV:
        if children:
            kids = "".join(
                f'<li class="nav-item"><a class="nav-link" href="{h}">{l}</a></li>'
                for l, h in children
            )
            out.append(
                f'<li class="nav-item submenu"><a class="nav-link" href="{href}">{label}</a>'
                f"<ul>{kids}</ul></li>"
            )
        else:
            out.append(
                f'<li class="nav-item"><a class="nav-link" href="{href}">{label}</a></li>'
            )
    return "\n                  ".join(out)


HEADER = """    <a class="skip-link" href="#main">Skip to content</a>
    <header class="main-header">
      <div class="header-sticky">
        <nav class="navbar navbar-expand-lg">
          <div class="container">
            <a class="navbar-brand brand-lockup" href="index.html">
              <img src="images/logo.svg" alt="No-BS Yardwork" width="150" height="50"
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
                    <img src="images/icon-phone.svg" alt="" width="25" height="25" />
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
                <img src="images/footer-logo.svg" alt="No BS Junk Removal Winnipeg"
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
                  &nbsp;&nbsp;<img src="images/payments.webp"
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

SCRIPTS = """    <script src="js/jquery-3.7.1.min.js" defer></script>
    <script src="js/bootstrap.min.js" defer></script>
    <!-- function.js calls $('#contactForm').validator() unconditionally; without
         this file that throws and every later handler in function.js (including
         the mobile nav) dies with it. -->
    <script src="js/validator.min.js" defer></script>
    <script src="js/jquery.slicknav.min.js" defer></script>
    <script src="js/jquery.waypoints.min.js" defer></script>
    <script src="js/jquery.counterup.min.js" defer></script>
    <script src="js/gsap.min.js" defer></script>
    <script src="js/SplitText.js" defer></script>
    <script src="js/ScrollTrigger.min.js" defer></script>
    <script src="js/function.js" defer></script>
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

    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="No BS Junk Removal" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:image" content="{SITE}/images/{og_image}" />
    <meta property="og:locale" content="en_CA" />

    <link rel="shortcut icon" type="image/x-icon" href="images/favicon.webp" />

    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="preload" as="style"
      href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap"
      onload="this.onload=null;this.rel='stylesheet';" />
    <noscript><link rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap" /></noscript>

    <link rel="preload" href="css/bootstrap.min.css" as="style" onload="this.onload=null;this.rel='stylesheet';" />
    <link rel="preload" href="css/all.min.css" as="style" onload="this.onload=null;this.rel='stylesheet';" />
    <link rel="preload" href="css/slicknav.min.css" as="style" onload="this.onload=null;this.rel='stylesheet';" />
    <link rel="preload" href="css/custom.css" as="style" onload="this.onload=null;this.rel='stylesheet';" />
    <link rel="preload" href="css/junk.css?v=1" as="style" onload="this.onload=null;this.rel='stylesheet';" />
    <noscript>
      <link rel="stylesheet" href="css/bootstrap.min.css" />
      <link rel="stylesheet" href="css/all.min.css" />
      <link rel="stylesheet" href="css/slicknav.min.css" />
      <link rel="stylesheet" href="css/custom.css" />
      <link rel="stylesheet" href="css/junk.css?v=1" />
    </noscript>

    <link rel="preload" href="webfonts/fa-brands-400.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="preload" href="webfonts/fa-solid-900.woff2" as="font" type="font/woff2" crossorigin />

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
def P(slug, title, description, og_image="skid_steer.webp", crumbs=None,
      schema=None, robots=DEFAULT_ROBOTS, body_class=""):
    blocks = list(schema or [])
    if crumbs is not None:
        blocks.append(breadcrumbs(crumbs))
    return {
        "slug": slug, "title": title, "description": description,
        "og_image": og_image, "schema": blocks, "robots": robots,
        "body_class": body_class,
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
def subst(text, mapping):
    """Token replacement for chrome and page fragments.

    Deliberately plain string replacement rather than str.format: fragments
    contain literal braces (inline JSON, the JotForm embed), and format()
    would choke on every one of them.
    """
    for key, value in mapping.items():
        text = text.replace("{" + key + "}", str(value))
    return text


def main():
    nav_html = render_nav()
    footer_links = "".join(
        f'<li><a href="{h}">{l}</a></li>' for l, h in FOOTER_LINKS
    )

    common = dict(
        PHONE_TEL=PHONE_TEL, PHONE_DISPLAY=PHONE_DISPLAY, PHONE_E164=PHONE_E164,
        EMAIL=EMAIL, SITE=SITE, GTM_ID=GTM_ID, GA4_ID=GA4_ID,
        JOTFORM_ID=JOTFORM_ID,
    )
    header = subst(HEADER.replace("{NAV}", nav_html), common)
    footer = subst(FOOTER.replace("{FOOTER_LINKS}", footer_links), common)

    written = 0
    for page in PAGES:
        slug = page["slug"]
        frag = PAGES_DIR / f"{slug}.html"
        if not frag.exists():
            raise SystemExit(f"missing page fragment: {frag}")
        body = subst(frag.read_text(encoding="utf-8"), common)

        canonical = SITE + ("/" if slug == "index" else f"/{slug}")

        if page["schema"]:
            schema_html = "".join(
                '    <script type="application/ld+json">\n'
                + json.dumps(b, indent=2, ensure_ascii=False)
                + "\n    </script>\n"
                for b in page["schema"]
            )
        else:
            schema_html = ""

        html = PAGE.format(
            title=page["title"], description=page["description"],
            canonical=canonical, og_image=page["og_image"],
            robots=page["robots"], body_class=page["body_class"],
            schema=schema_html, body=body,
            HEADER=header, FOOTER=footer, SCRIPTS=SCRIPTS,
            **common,
        )
        (ROOT / f"{slug}.html").write_text(html, encoding="utf-8")
        written += 1

    # Sitemap, generated from the same list so it can never drift out of sync.
    urls = []
    for page in PAGES:
        if "noindex" in page["robots"]:
            continue
        slug = page["slug"]
        loc = SITE + ("/" if slug == "index" else f"/{slug}")
        priority = "1.00" if slug == "index" else (
            "0.90" if slug in {"pricing", "commercial-junk-removal-winnipeg",
                               "what-we-take", "quote"} else "0.80")
        urls.append(
            f"  <url>\n    <loc>{loc}</loc>\n"
            f"    <changefreq>monthly</changefreq>\n"
            f"    <priority>{priority}</priority>\n  </url>"
        )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")

    print(f"built {written} pages + sitemap.xml")


if __name__ == "__main__":
    main()
