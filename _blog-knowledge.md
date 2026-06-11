# No-BS Yardwork — Blog Knowledge Base

This file is the brain of the daily blog autopilot. The scheduled-task `SKILL.md`
reads this file instead of re-deriving templates/keywords each run, to save tokens
and enforce a consistent SEO + conversion bar.

Update rule: the skill appends a dated entry to `## L. Learning Log` every 7 posts
and refreshes sections **B** (title formulas) and **C** (query bank) with any new
patterns or keyword gaps spotted.

---

## A. Template block (copy-paste — only swap placeholders)

Placeholders to replace per post:
- `{{TITLE}}` — SEO title (matches one of the formulas in B)
- `{{META}}` — meta description ≤155 chars, contains "Winnipeg"
- `{{SLUG}}` — filename without `.html` (e.g., `blog-sod-cost-winnipeg`)
- `{{H1}}` — page H1 (can be a shorter variant of the title)
- `{{BREADCRUMB_LABEL}}` — breadcrumb trailing label
- `{{DATE}}` — YYYY-MM-DD
- `{{IMAGE}}` — `images/{{SLUG}}.webp` (Pexels-fetched hero)
- `{{KEYWORDS}}` — comma-separated target keywords

### Full `<head>` block

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>{{TITLE}} | No-BS Yardwork</title>
    <meta name="description" content="{{META}}" />
    <meta name="keywords" content="{{KEYWORDS}}" />
    <meta name="author" content="No-BS Yardwork" />
    <meta name="robots" content="follow, index, max-snippet:-1, max-video-preview:-1, max-image-preview:large" />
    <link rel="canonical" href="https://www.no-bs-yardwork.com/{{SLUG}}" />

    <meta property="og:title" content="{{TITLE}}" />
    <meta property="og:description" content="{{META}}" />
    <meta property="og:url" content="https://www.no-bs-yardwork.com/{{SLUG}}" />
    <meta property="og:type" content="article" />
    <meta property="og:image" content="https://www.no-bs-yardwork.com/{{IMAGE}}" />

    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{{TITLE}}",
      "description": "{{META}}",
      "author": { "@type": "Organization", "name": "No-BS Yardwork" },
      "publisher": {
        "@type": "Organization",
        "name": "No-BS Yardwork",
        "logo": { "@type": "ImageObject", "url": "https://www.no-bs-yardwork.com/images/logo.webp" }
      },
      "datePublished": "{{DATE}}",
      "image": "https://www.no-bs-yardwork.com/{{IMAGE}}",
      "url": "https://www.no-bs-yardwork.com/{{SLUG}}"
    }
    </script>

    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.no-bs-yardwork.com/" },
        { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://www.no-bs-yardwork.com/blog.html" },
        { "@type": "ListItem", "position": 3, "name": "{{BREADCRUMB_LABEL}}", "item": "https://www.no-bs-yardwork.com/{{SLUG}}" }
      ]
    }
    </script>

    <link rel="shortcut icon" type="image/x-icon" href="images/favicon.webp" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,600;0,700;1,400&display=swap" />
    <link rel="stylesheet" href="css/bootstrap.min.css" />
    <link rel="stylesheet" href="css/all.min.css" />
    <link rel="stylesheet" href="css/slicknav.min.css" />
    <link rel="stylesheet" href="css/custom.css?v=3" />
    <style>
      .blog-post-content { padding: 60px 0 80px; }
      .blog-post-content h2 { font-size: 1.6rem; color: #1b3d2f; margin: 40px 0 16px; }
      .blog-post-content h3 { font-size: 1.2rem; color: #2e7d32; margin: 28px 0 12px; }
      .blog-post-content p { font-size: 1.05rem; line-height: 1.85; color: #333; margin-bottom: 18px; }
      .blog-post-content ul, .blog-post-content ol { margin: 0 0 22px 20px; }
      .blog-post-content ul li, .blog-post-content ol li { font-size: 1.05rem; line-height: 1.8; color: #333; margin-bottom: 8px; }
      .blog-cta-box { background: linear-gradient(135deg, #1b3d2f, #2e7d32); color: #fff; border-radius: 16px; padding: 40px; margin-top: 50px; text-align: center; }
      .blog-cta-box h3 { color: #f9a825; font-size: 1.5rem; margin-bottom: 12px; }
      .blog-cta-box p { color: rgba(255,255,255,0.9); margin-bottom: 24px; }
      .blog-cta-box a { background: #f9a825; color: #1b3d2f; font-weight: 700; padding: 14px 32px; border-radius: 30px; text-decoration: none; font-size: 15px; }
      .blog-meta { color: #888; font-size: 0.9rem; margin-bottom: 30px; }
      .blog-callout { background: #f4f9f4; border-left: 4px solid #2e7d32; border-radius: 0 12px 12px 0; padding: 20px 24px; margin: 28px 0; }
      .blog-callout p { margin: 0; color: #1b3d2f; font-weight: 600; }
      .blog-inline-cta { background: #fffbe6; border: 1px dashed #f9a825; border-radius: 10px; padding: 14px 20px; margin: 24px 0; }
      .blog-inline-cta p { margin: 0; color: #1b3d2f; }
      .blog-inline-cta a { color: #2e7d32; font-weight: 700; }
      .blog-hero-img { width: 100%; height: auto; border-radius: 12px; margin-bottom: 32px; display: block; }
      .slicknav_btn { background-color: #1b3d2f !important; border-radius: 12px !important; }
      .slicknav_nav { background-color: #1b3d2f !important; }
    </style>

    <script async src="https://www.googletagmanager.com/gtag/js?id=G-VN2QZ4KXXH"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag() { dataLayer.push(arguments); }
      gtag("js", new Date());
      gtag("config", "G-VN2QZ4KXXH");
    </script>
  </head>
```

### Header/nav, breadcrumb, footer

Copy from `blog-why-spring-aeration-winnipeg.html` lines 86–148 (header + page-header
breadcrumb) and 226–327 (footer + scripts) verbatim. Only change the breadcrumb label
and the H1 text.

### Body shell

```html
    <div class="blog-post-content">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto">
            <!-- Hero image: REQUIRED — fetched from Pexels via autopilot --fetch-image -->
            <img src="{{IMAGE}}" alt="{{H1}} — No-BS Yardwork Winnipeg" class="blog-hero-img" width="1200" height="900" loading="eager" />

            <!-- Byline: always "Written by The No-BS Team" + full date (e.g. April 18, 2026) + Winnipeg, MB -->
            <p class="blog-meta">Written by The No-BS Team &nbsp;|&nbsp; {{FULL_DATE}} &nbsp;|&nbsp; Winnipeg, MB</p>

            <!-- HOOK: 2 sentences, answer the query immediately -->
            <p>{{HOOK_SENTENCE_1}} {{HOOK_SENTENCE_2}}</p>

            <!-- CTA #1 — above the fold -->
            <div class="blog-inline-cta">
              <p>{{CTA_ABOVE_FOLD}}</p>
            </div>

            <!-- 4–6 H2 sections drawn from Section Menu (D) -->

            <!-- CTA #2 — mid-article (after section 2 or 3) -->
            <div class="blog-inline-cta">
              <p>{{CTA_MID}}</p>
            </div>

            <!-- Remaining H2 sections -->

            <!-- CTA #3 — end of article -->
            <div class="blog-cta-box">
              <h3>{{CTA_END_HEADING}}</h3>
              <p>{{CTA_END_SUPPORT}}</p>
              <a href="contact.html">Get a Free Quote</a>
            </div>

          </div>
        </div>
      </div>
    </div>
```

---

## B. Title formulas (rotate; one per post)

Must match exactly one of these — the whole point is to mirror real search queries.

1. **Cost** — `How Much Does {Service} Cost in Winnipeg? (2026 Pricing Guide)`
2. **Timing** — `When Should You {Verb} Your Lawn in Winnipeg?` / `When Is the Best Time to {X} in Winnipeg?`
3. **Need** — `Do You Need {Service} in Winnipeg?` / `Signs Your Winnipeg Lawn Needs {X}`
4. **Comparison** — `{A} vs {B}: Which Does Your Winnipeg Lawn Need?`
5. **Frequency** — `How Often Should You {X} in Winnipeg?`
6. **Tips** — `N {Adjective} {Service} Tips That Actually Work in Winnipeg`

Rules:
- Include "Winnipeg" in the title.
- Years use the current calendar year.
- Keep titles ≤70 chars where possible.

---

## C. Winnipeg Query Bank (seed; grows via Learning Log)

### Cost queries
sod cost winnipeg · patio installation cost winnipeg · retaining wall cost winnipeg ·
spring cleanup cost winnipeg · yard cleanup cost winnipeg · weed control cost winnipeg ·
fall cleanup cost winnipeg · leaf removal cost winnipeg · snow removal cost winnipeg ·
weekly lawn care cost winnipeg · aeration cost winnipeg · power raking cost winnipeg ·
fencing cost winnipeg · overseeding cost winnipeg · lawn installation cost winnipeg ·
mulch delivery cost winnipeg · grading cost winnipeg.

### Timing queries
when to aerate lawn winnipeg · when to overseed winnipeg · when to power rake winnipeg ·
when to do first cut winnipeg · when to fertilize lawn winnipeg ·
when to book spring cleanup winnipeg · when to do fall cleanup winnipeg ·
when to install sod winnipeg · when to dethatch lawn winnipeg ·
when to apply weed control winnipeg.

### Service-need queries
do I need power raking winnipeg · signs lawn needs aeration winnipeg ·
do I need spring cleanup winnipeg · signs of grub damage winnipeg ·
why is my lawn patchy winnipeg · do I need fall cleanup winnipeg ·
why dandelions keep coming back winnipeg · do I need a retaining wall winnipeg ·
why is my grass yellow winnipeg · why is my lawn burning in summer winnipeg ·
watering lawn during dry spells winnipeg · signs lawn needs fertilizer winnipeg ·
do I need lawn fertilizing winnipeg.

### Frequency queries
how often cut grass winnipeg · how often aerate winnipeg ·
how often apply weed control winnipeg · how often fertilize lawn winnipeg ·
how often water lawn winnipeg · how often overseed lawn winnipeg ·
how often power rake winnipeg.

### Comparison queries
power raking vs aeration winnipeg · sod vs seed winnipeg ·
paver patio vs concrete winnipeg · DIY vs hiring lawn care winnipeg ·
weekly vs biweekly mowing winnipeg · mulch vs rock winnipeg.

### Category coverage (pull seasonally)
**Lawn Care:** mowing · first cut · weekly maintenance · recurring care · lawn health ·
fertilizing · overseeding · patch repair · lawn renovation.
**Spring:** spring cleanup · power raking · dethatching · aeration · debris removal ·
bed cleanouts · first mow · spring lawn prep.
**Summer:** recurring mowing · lawn stress · dry spots · weed control · edging · trimming ·
lawn thickening · watering · maintenance packages.
**Fall:** fall cleanup · leaf cleanup · final cut · overseeding · aeration · hedge trimming ·
garden bed cleanup · winter prep.
**Winter:** snow removal · ice control · de-icing · walkway clearing · winter contracts ·
property maintenance.
**Landscaping/Softscaping:** sod · grading · garden beds · mulch · decorative rock ·
edging · shrubs · trees · full yard installs.
**Hardscaping:** patios · retaining walls · walkways · pavers · steps · firepit areas ·
backyard builds · fence-adjacent installs.
**Recurring/Contract:** weekly cuts · seasonal packages · lawn care subscriptions ·
residential recurring · commercial maintenance.
**Weed Control/Problem Topics:** weeds · dandelions · patchy lawn · compacted soil ·
dead grass · moss · drainage issues · overgrown yards.

---

## D. Section Menu (H2 pool — pick 4–6 per post)

- Average cost in Winnipeg
- What affects price
- When to do it in Winnipeg
- Signs you need it
- What's included
- Common mistakes
- DIY vs professional
- Best option for Winnipeg conditions
- How to get a quote

Rule: at least one cost/number section and one Winnipeg-specific timing/conditions section.

---

## E. Hook patterns (2-line direct answer)

Rule: sentence 1 = the answer. Sentence 2 = what the post will cover.

**Cost:**
- "Sod in Winnipeg usually runs $0.80–$1.50/sq ft installed, depending on grading, prep, and access. Here's what actually moves the price and when sod beats seeding."

**Timing:**
- "The best time to aerate your lawn in Winnipeg is late April through mid-May, or again in early September. Here's how to know which window your yard needs."

**Need:**
- "If your Winnipeg lawn feels spongy, grew thin last summer, or has a thatch layer thicker than half an inch, you need power raking this spring. Here's how to tell for sure."

**Comparison:**
- "Power raking pulls up dead thatch. Aeration punches cores to relieve compaction. Most Winnipeg lawns need both — but in a specific order. Here's which one yours needs first."

**Frequency:**
- "In Winnipeg, grass should be cut every 5–7 days from late May through August — longer between cuts stresses the lawn. Here's the schedule that keeps your yard healthy."

---

## F. CTA bank

### CTA #1 — above the fold (pick one; paraphrase OK)
- "Want an exact price for your yard? [Get a quote now](contact.html)."
- "Skip the guesswork — [request a quote](contact.html) and we'll price it for your Winnipeg property fast."
- "Not sure where to start? [Get a free quote](contact.html) and we'll walk you through it."

### CTA #2 — mid-article
- "Not sure what your yard actually needs? [Get a quick quote](contact.html) and we'll tell you straight."
- "We can price this out for your Winnipeg property in minutes. [Request a quote](contact.html)."
- "Want this priced for your exact yard? [Book a free quote](contact.html)."

### CTA #3 — end `.blog-cta-box`
Heading + support + "Get a Free Quote" button. Heading variants:
- "Want This Done Right the First Time?"
- "Get a Clear Price for Your Winnipeg Yard"
- "Book Your {Service} in Winnipeg"
- "Stop Guessing — Get a Real Quote"

Support-line variants:
- "We service all of Winnipeg and surrounding areas. Quotes are fast, free, and specific to your yard."
- "No pressure, no runaround. You'll get a clear price based on your actual property."
- "Spots fill up fast this season. Lock yours in before the calendar fills."

---

## G. Internal Link Map

| Topic | Link | Suggested anchor text |
|---|---|---|
| Lawn care (basic) | `lawn-care-winnipeg.html` | "our basic lawn care in Winnipeg" |
| Premium lawn care | `premium-lawn-care.html` | "our premium lawn care plan" |
| Grass cutting | `grass-cutting-winnipeg.html` | "weekly grass cutting in Winnipeg" |
| Weed control | `weed-control-winnipeg.html` | "weed control service" |
| Cleanups | `spring-fall-cleanups.html` | "spring and fall cleanup packages" |
| Fencing | `fencing-winnipeg.html` | "fence installation in Winnipeg" |
| Landscaping | `landscaping-winnipeg.html` | "landscaping services in Winnipeg" |
| Yard maintenance | `yard-maintenance-winnipeg.html` | "full-yard maintenance" |
| Snow | `winter-packages.html` | "Winnipeg snow removal packages" |
| Quote | `contact.html` | "get a free quote" |

Rules:
- 2–3 internal links per post.
- Descriptive anchors — never "click here."
- At least one link must point to the service the post targets.

---

## H. Pexels keyword recipes (topic → search string)

| Topic | Pexels query |
|---|---|
| sod install | `fresh green sod lawn residential` |
| patio | `modern paver patio backyard` |
| retaining wall | `stone retaining wall garden` |
| spring cleanup | `spring lawn cleanup rake` |
| aeration | `lawn aeration core plugs` |
| power raking | `lawn dethatching rake grass` |
| fall cleanup | `autumn leaves yard cleanup` |
| leaf removal | `fall leaves rake yard` |
| snow removal | `residential driveway snow clearing` |
| weed control | `dandelion free green lawn` |
| overseeding | `grass seed lawn spreader` |
| overseeding | `grass seed lawn spreader` |
| mowing | `lawn mower striping green grass` |
| fencing | `wood fence backyard residential` |
| mulch | `garden bed mulch landscaping` |
| grading | `lawn grading topsoil` |
| fertilizer | `lawn fertilizer spreader green grass` |
| watering / irrigation | `lawn sprinkler green grass summer` |

---

## I. Local-signal phrase bank

Use Winnipeg ≥6× per post; sprinkle ≥2 of these per post:

Winnipeg · Manitoba · prairie climate · zone 3 · clay soil · heavy clay ·
freeze-thaw cycles · short growing season · Manitoba winters · Red River Valley ·
after the snowmelt · late spring frost.

Neighborhood mentions (use when talking service coverage):
St. Vital · Transcona · River Heights · Charleswood · St. James · Fort Garry ·
Tuxedo · East Kildonan · West Kildonan · Headingley · Oak Bluff · St. Boniface ·
Garden City · Windsor Park · Linden Woods.

---

## J. Categories (for posts.json / blog.html filter)

`Lawn Care` · `Cleanups` · `Fencing` · `Landscaping` · `Snow Removal` ·
`Hardscaping` · `Weed Control` · `Recurring Services`.

---

## K. Scoring rubric (topic selection, /20)

| Dimension | Points | What scores 5 |
|---|---|---|
| Local intent | /5 | Query explicitly mentions Winnipeg or is a Winnipeg-specific concern |
| Buyer intent | /5 | Cost, timing, need, or comparison phrasing — someone about to hire |
| Quote path | /5 | Topic maps cleanly to a service on the Internal Link Map |
| Gap | /5 | Not in `published_slugs`; Bulger/competitors haven't owned the angle |

**Reject any topic <14 or without a clear path to a quote.**

---

## L. Learning Log

*(Appended every 7 posts. Format: `### YYYY-MM-DD — Cycle #N` followed by four
bullet lists: new formulas, retire, new keywords, H2 patterns to promote.)*

<!-- No entries yet. First cycle triggers after 7 posts published under this system. -->

### 2026-04-19 — Post: blog-sod-vs-seed-winnipeg (mini)
- What went wrong: Pexels image was fetched and saved by autopilot but never rendered in the article body — only existed in OG meta and JSON-LD. Post published without a visible hero image.
- What worked well: Topic scoring (20/20), competitor check, all SEO gate items, and internal link mix all executed cleanly first pass.
- One thing to do differently next post: Place the `<img class="blog-hero-img">` tag in the article body *before* writing any content — treat it as the first required element of the body shell, not an afterthought.

### 2026-04-20 — Post: blog-when-to-apply-weed-control-winnipeg (mini)
- What went well: Hero image confirmed live (200) on first attempt — path-equality guard fix from previous run held. Dandelion callout block adds a scannable visual break mid-article that reinforces the timing signal without adding words.
- What nearly went wrong: `posts_since_learn` was already incremented by autopilot but still needed a manual +1 since autopilot only tracks slug append, not the learn counter.
- One thing to do differently next post: Pre-count Winnipeg mentions explicitly during drafting rather than checking after — saves a review pass.

### 2026-04-21 — Post: blog-overseeding-cost-winnipeg (mini)
- What went well: Hero image placed first in body shell (before blog-meta) as per learning log — no repeat of the 2026-04-19 image incident. Price table rendered via CSS class rather than inline styles, keeping the no-inline-styles gate clean.
- What nearly went wrong: Autopilot updated `last_content_type` and slug list but did not increment `posts_since_learn` — manual +1 required as noted in previous mini-learn. Consistent pattern; expect this every run.
- One thing to do differently next post: Pre-verify the Pexels query maps directly to a section H entry before running autopilot — "overseeding" has no explicit H entry, required judgment call to use "grass seed lawn spreader". Add "overseeding" → "grass seed lawn spreader" to section H to remove ambiguity.

### 2026-04-25 — Post: blog-first-cut-winnipeg (mini)
- What went well: Hero image placed first in body shell (before blog-meta), all three CTAs present, competitor check clean. Autopilot patched blog.html and uploaded correctly first pass.
- What nearly went wrong: Autopilot set `last_content_type` to "how-to" (the type just written) instead of the next-in-rotation "tips-and-tricks" — required manual correction. Pattern confirmed: always override autopilot's content-type to next-in-rotation after every run.
- One thing to do differently next post: Pre-count Winnipeg body mentions during drafting (≥6 required); confirmed 15+ this run but checking during write is faster than reviewing after.

### 2026-04-25 — Post: blog-mulch-vs-rock-winnipeg (mini)
- What went well: Hero image placed first in body shell before blog-meta; all three CTAs present; competitor check confirmed no collision; image returned 200 on first verify attempt.
- What nearly went wrong: Autopilot set `last_content_type` to "comparison" (type just written) instead of next-in-rotation "timing-guide" — required manual correction as expected every run.
- One thing to do differently next post: Autopilot pattern now confirmed across 3+ runs: always override `last_content_type` to next-in-rotation after every run. Add note to skill to make this explicit.

### 2026-04-26 — Post: blog-weed-control-cost-winnipeg (mini)
- What went well: Hero image placed first in body shell before blog-meta; all three CTAs present; image confirmed live (200) immediately after autopilot; competitor check clean; topic perfectly timed for peak dandelion season in Winnipeg.
- What nearly went wrong: Autopilot set `last_content_type` to "cost-guide" (type just written) instead of next-in-rotation "how-to" — manually corrected as per established pattern. Also autopilot did not increment `posts_since_learn` — manually incremented from 5 to 6.
- One thing to do differently next post: `posts_since_learn` is now 6 — next run triggers the full learning cycle (Step 11). Pre-read the last 7 slugs early in the run to avoid a mid-post context spike.

### 2026-04-27 — Cycle #1
- New title formulas to add: None — existing 6 cover the space. However, Formula 3 (Need/Signs) and Formula 5 (Frequency) were completely absent from the last 7 posts. Next 7 posts should include at least 2 Formula 3 and 1 Formula 5.
- Overused angles to retire (for now): Formula 1 cost guides (2/7 posts) and Formula 4 comparisons (2/7 posts) — hold off for 2–3 posts each. "DIY vs Professional" H2 appeared in every cost post — vary with "Is It Worth Hiring Someone?" or "When to Call a Pro" instead.
- New Winnipeg keyword opportunities: "how often water lawn winnipeg" (zero posts, summer relevance building), "why is my grass yellow winnipeg" (strong need/buyer intent, zero coverage), "lawn fertilizing winnipeg when to start", "watering lawn during dry spells winnipeg" — all coming into season by May/June. Competitor check (Bulger Brothers, April 27): still zero maintenance/weed/lawn care content — full gap advantage remains.
- H2 patterns to promote: "What Winnipeg's Climate Does to X" (strong local authority, only used in mulch post) — apply to any topic where climate is a real factor. Numbered tip structure "Tip N — [Action]" used in today's post — performs well for scanability, reuse for any tips-and-tricks type. "The [specific window]: Why [timing] Matters in Manitoba" — regional authority framing from blog-first-cut-winnipeg, expand to other services.

### 2026-04-27 — Post: blog-dandelion-control-winnipeg (mini)
- What went well: Learning cycle triggered cleanly; hero image live on first verify (binary WebP returned by WebFetch = 200); all 3 CTAs present; internal links to all 3 target pages (weed-control, grass-cutting, lawn-care); Winnipeg count 8+; clay soil + freeze-thaw + Manitoba + zone 3 local signals all present.
- What nearly went wrong: autopilot confirmed pattern — set last_content_type to type just written ("tips-and-tricks") and did not increment posts_since_learn. Both required manual correction as expected.
- One thing to do differently next post: Formula 3 (Need) and Formula 5 (Frequency) have zero coverage in the last 7 posts — next post must use one of these to rebalance the mix.

### 2026-04-28 — Post: blog-lawn-fertilizer-winnipeg (mini)
- What went well: Hero image placed first in body shell before blog-meta; all 3 CTAs present; image confirmed live (binary WebP 200.1KB returned by WebFetch); competitor check clean; topic perfectly timed for spring fertilizer season. Autopilot slug append correct (17 total).
- What nearly went wrong: Autopilot set `last_content_type` to "comparison" (next-in-rotation) instead of "need" (type actually written) — manually corrected as per established pattern. Also did not increment `posts_since_learn` — manually set to 1. Rotation note: comparison is still overdue (not written in Cycle #1's 7 posts); Cycle #1 log says hold off 2–3 posts — next run should use Formula 5 (Frequency) or timing-guide.
- One thing to do differently next post: Section H has no "fertilizer" entry — used "lawn fertilizer spreader green grass" as judgment call; add to brain to avoid ambiguity.

### 2026-04-30 — Post: blog-watering-lawn-winnipeg (mini)
- What went wrong or nearly wrong: Autopilot set `last_content_type` to "how-to" correctly this run (next-from-cost-guide = how-to = what was written — a lucky alignment). Still did not increment `posts_since_learn` — manually corrected to 3 as per established pattern. Pexels query "lawn sprinkler green grass summer" had no section H entry; added "watering/irrigation" → "lawn sprinkler green grass summer" to brain.
- What worked well: Hero image placed first in body shell before blog-meta; image confirmed live (binary WebP 193.1KB); all 3 CTAs present; 3 internal links (lawn-care, landscaping, grass-cutting); 15+ Winnipeg/Manitoba mentions; competitor check clean (Bulger has zero watering/irrigation coverage); topic well-timed for spring-to-summer transition.
- One thing to do differently next post: Next type is "tips-and-tricks" — pick a topic where numbered or scannable tips add clear value (e.g. lawn problem-solving, seasonal prep list). Confirm Pexels query maps to section H before running autopilot.

### 2026-04-29 — Post: blog-best-time-install-sod-winnipeg (mini)
- What nearly went wrong: First topic choice ("When Should You Book Your Spring Lawn Cleanup in Winnipeg?") collided with a Bulger Brothers post from April 13 on the same angle — the competitor check (Step 5) caught it and saved the post from being redundant. Second topic (sod timing) had zero competitor coverage and scored 20/20.
- What worked well: Hero image placed first in body shell before blog-meta; image confirmed live (binary WebP 569.8KB, 200) on first verify; autopilot correctly set `last_content_type` to "cost-guide" (next-in-rotation after timing-guide) without manual correction — first time this has happened cleanly.
- One thing to do differently next post: When first topic gets rejected via competitor check, generate the replacement score from the already-scored candidate list rather than re-scoring from scratch — saves a full scoring pass.

### 2026-05-05 — Post: blog-weed-prevention-tips-winnipeg (mini)
- What went wrong or was nearly wrong: Autopilot set `last_content_type` to "tips-and-tricks" (type just written) instead of next-in-rotation "comparison" — manually corrected as per established pattern. Also did not increment `posts_since_learn` — manually set from 3 to 4.
- What worked well: Hero image placed first in body shell before blog-meta; Pexels "dandelion free green lawn" matched section H exactly; image confirmed live (binary WebP 155.6KB) on first verify; all 3 CTAs present; 3 internal links (grass-cutting, weed-control, spring-fall-cleanups); 12+ Winnipeg/Manitoba mentions; clay soil + freeze-thaw + prairie climate + zone 3 + Red River Valley local signals all present. Numbered tip structure ("Tip N —") gives strong scanability for the tips-and-tricks format.
- One thing to do differently next post: Next type is "comparison" — pick a topic where A vs B framing has genuine buyer decision value (e.g. "weekly vs biweekly mowing winnipeg", "paver patio vs concrete winnipeg"). Confirm no collision with the 3 existing comparison posts (sod-vs-seed, mulch-vs-rock, power-raking-vs-aeration implied in brain C). posts_since_learn=4, learning cycle triggers at 7 — no cycle this run.

### 2026-05-06 — Post: blog-weekly-vs-biweekly-mowing-winnipeg (mini)
- What went wrong or was nearly wrong: Autopilot did not increment `posts_since_learn` (stayed at 4) and did not update `last_post_date` — both required manual correction as per established pattern. Autopilot DID correctly set `last_content_type` to "timing-guide" (next-in-rotation after comparison) without manual override — first clean rotation in several runs.
- What worked well: Hero image placed first in body shell before blog-meta; image confirmed live (binary WebP 149.7KB) on first verify; all 3 CTAs present; 3 internal links (grass-cutting, lawn-care, yard-maintenance); 11+ Winnipeg/Manitoba mentions; prairie climate + zone 3 + clay soil + freeze-thaw + Manitoba winters local signals all present. Competitor check confirmed zero mowing-frequency content on Bulger Brothers — full gap advantage. The hybrid schedule framing (weekly in peak, biweekly in shoulder months) gives this post a more nuanced, credible angle than a simple "always do weekly" take.
- One thing to do differently next post: Next type is "timing-guide" — pick a topic where seasonal timing in Winnipeg is the core value-add (e.g. "when to fertilize", "when to book fall cleanup", "when to dethatch"). Section H Pexels query: confirm mapping before running autopilot to avoid judgment calls.

### 2026-04-19 — Post: blog-sod-vs-seed-winnipeg (mini, follow-up)
- What went wrong (bigger issue): autopilot silently skipped the image FTP upload due to a path-equality guard in `_blog-autopilot.py` (`if image_path != args.image`). The image existed locally but the server returned 404, so the blog.html card rendered as a flat green gradient. Fixed by removing the guard; added Step 7b to the skill as a hard 200-check before marking the post done.
- Second issue: every blog post URL was being written with `.html` in canonical, og:url, JSON-LD, `<loc>`, and the POSTS array `url:` field. User wants clean URLs to match the rest of the site. Fixed across 13 files (10 posts + blog.html + faqs.html + blog-sitemap.xml) and in the autopilot + brain + skill templates so future posts are born clean.
- Takeaway: treat the "file exists locally" and "file is live on server" as two separate facts and always verify the second before declaring success.
