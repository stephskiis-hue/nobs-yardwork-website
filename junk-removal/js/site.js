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

  function setOpen(open) {
    if (!header || !toggle) return;
    header.classList.toggle("nav-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  }

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
