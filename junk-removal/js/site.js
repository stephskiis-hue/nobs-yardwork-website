/* site.js — No BS Junk Removal
 *
 * The only script the site loads. It replaces jQuery, Bootstrap JS, SlickNav,
 * GSAP, SplitText, ScrollTrigger, Waypoints, CounterUp and the lawn template's
 * function.js (about 400 KB together). No dependencies.
 *
 * Everything here is an enhancement: with JavaScript off, the nav links are
 * still reachable (the drawer is simply never needed above 1100px, and the
 * mobile call bar carries the phone number below it), the FAQs are native
 * <details>, and no content is ever hidden waiting for an animation.
 */
(function () {
  "use strict";

  var header = document.querySelector(".site-header");

  /* ---- Mobile nav drawer ---- */
  var toggle = document.querySelector(".nav-toggle");
  var menu = document.getElementById("main-menu");
  var root = document.documentElement;
  var subToggles = document.querySelectorAll(".sub-toggle");

  // Drawer sub-menus collapse only once this runs (see .nav-js in the CSS).
  root.classList.add("nav-js");

  function setSub(btn, open) {
    btn.parentNode.classList.toggle("sub-open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  }

  // Every section starts closed, on every page. Opening the one you are in
  // reads well but costs eight rows, which pushes "Get a Quote" off the bottom
  // of a short phone screen — the underlined parent already says where you are.
  function resetSubs() {
    subToggles.forEach(function (btn) { setSub(btn, false); });
  }

  function setOpen(open) {
    if (!header || !toggle) return;
    header.classList.toggle("nav-open", open);
    root.classList.toggle("nav-open-page", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (!open) resetSubs();
  }

  resetSubs();
  // One list open at a time keeps the drawer short enough to see "Get a Quote".
  subToggles.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") !== "true";
      subToggles.forEach(function (other) { if (other !== btn) setSub(other, false); });
      setSub(btn, open);
    });
  });

  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && header.classList.contains("nav-open")) {
        setOpen(false);
        toggle.focus();
      }
    });
    document.addEventListener("click", function (e) {
      if (header.classList.contains("nav-open") && !header.contains(e.target)) setOpen(false);
    });
    // Close the drawer if the window grows past the breakpoint while open.
    window.matchMedia("(min-width: 1100px)").addEventListener("change", function (mq) {
      if (mq.matches) setOpen(false);
    });
  }

  /* ---- Header shadow once the page scrolls ---- */
  if (header) {
    var ticking = false;
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
      ticking = false;
    };
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
    }, { passive: true });
    onScroll();
  }

  /* ---- Print: expand every <details> ----
   * FAQ answers and the full item list live in collapsed <details>. A closed
   * one does not print, and a printed FAQ with no answers is useless. CSS
   * cannot reliably force them open in Chrome, so do it here and put them
   * back afterwards. */
  window.addEventListener("beforeprint", function () {
    document.querySelectorAll("details:not([open])").forEach(function (d) {
      d.setAttribute("data-was-closed", "");
      d.open = true;
    });
  });
  window.addEventListener("afterprint", function () {
    document.querySelectorAll("details[data-was-closed]").forEach(function (d) {
      d.removeAttribute("data-was-closed");
      d.open = false;
    });
  });

  /* ---- Lead tracking ----
   * Calls, texts and the quote form are the only things on this site worth
   * money, and none of them is a page view, so GA4 reports nothing about them
   * on its own. These send the three events the owner reads to tell which
   * pages actually produce work.
   *
   * Everything goes through send(): a large share of visitors run an ad
   * blocker, which means gtag is simply not there, and a missing tag must
   * never turn into a broken button. */
  function send(name, params) {
    try {
      if (typeof window.gtag === "function") window.gtag("event", name, params);
    } catch (err) {
      /* Analytics is never worth an exception on a lead click. */
    }
  }

  // Which piece of furniture the click came from. Counting calls alone says
  // the phone rang; this says whether it was the sticky bar, the hero or a
  // link buried in the copy that did it, which is what decides where the next
  // call button goes.
  function placeOf(el) {
    if (el.closest(".mobile-call-bar")) return "mobile_call_bar";
    if (el.closest(".site-header")) return "header";
    if (el.closest(".site-footer")) return "footer";
    if (el.closest(".junk-hero")) return "hero";
    return "body";
  }

  // Delegated from the document so every tel:/sms: link is covered, including
  // ones added to a page fragment later — there are already thirty-odd of them
  // across the site and no one is going to remember to tag a new one.
  //
  // Nothing here calls preventDefault and nothing waits for a beacon: the dial
  // or the text goes through exactly as it would with this file deleted. A
  // dropped statistic costs nothing; a call that does not dial costs a job.
  document.addEventListener("click", function (e) {
    var el = e.target;
    if (!el || !el.closest) return;
    var link = el.closest('a[href^="tel:"], a[href^="sms:"]');
    if (!link) return;
    var sms = link.getAttribute("href").lastIndexOf("sms:", 0) === 0;
    send(sms ? "text_click" : "call_click", {
      link_location: placeOf(link),
      // GA4 ties the event to the page on its own, but only as page_location.
      // Sending the path as its own parameter is what lets these break down
      // per page in a report without unpicking a full URL first.
      page_path: location.pathname
    });
  });

  /* ---- Quote form submissions ----
   * The form on /quote is a JotForm iframe on another origin. There is no
   * submit event to listen for and no URL to read: the browser will not let
   * this page see inside it. JotForm's own form code posts a message out to
   * the parent window instead, and that message is the only signal there is.
   *
   * We listen for {action: "submission-completed"}. Be clear about what that
   * name rests on: JotForm support name it in their forum answers and every
   * GTM guide uses it, but it is NOT in the code they ship — their form
   * runtime (jotform.forms.js) posts only "submission-started" and
   * "submission-end", and posts both with no targetOrigin, which means the
   * browser delivers them to a same-origin parent and drops them for us.
   * Those two also fire before validation, so a form that never sent would
   * still count as a lead. JotForm say in the same answers that none of these
   * messages are a public API and that they may change without notice.
   *
   * So if quote_form_submit reads zero for a month while leads are sitting in
   * the JotForm inbox, the message shape changed. Check that first — and it is
   * the reason the call and text events are the ones to trust.
   */
  var quoteFrame = document.querySelector('iframe[id^="JotFormIFrame-"]');
  if (quoteFrame) {
    var counted = false;
    window.addEventListener("message", function (e) {
      // Any site, and any frame, can post a message into this window. It only
      // counts if it came out of the form frame itself AND off a JotForm host:
      // without both checks a lead is something a stranger can fake, and the
      // numbers stop meaning anything.
      if (counted || e.source !== quoteFrame.contentWindow) return;
      var host;
      try {
        host = new URL(e.origin).hostname;
      } catch (err) {
        return;
      }
      if (host !== "jotform.com" && host.slice(-12) !== ".jotform.com") return;

      // Height messages arrive as plain strings ("setHeight:940:<id>") and the
      // newer ones as objects, so read the action out of either shape.
      var action = typeof e.data === "string" ? e.data : e.data && e.data.action;
      if (action !== "submission-completed") return;

      // Once per page. The frame is free to repeat itself, and a repeat here
      // would show up as two leads from one customer.
      counted = true;
      send("quote_form_submit", { page_path: location.pathname });
    });
  }

  /* ---- Scroll reveal ----
   * Only elements below the fold are hidden; anything already on screen at
   * load is marked visible immediately so there is no flash on first paint. */
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var items = document.querySelectorAll(".wow");
  if (items.length && "IntersectionObserver" in window && !reduced) {
    var vh = window.innerHeight;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("animated");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });

    items.forEach(function (el) {
      if (el.getBoundingClientRect().top < vh) {
        el.classList.add("animated");
      } else {
        var d = el.getAttribute("data-wow-delay");
        if (d) el.style.setProperty("--reveal-delay", d);
        io.observe(el);
      }
    });
    document.documentElement.classList.add("reveal-ready");
  }
})();
