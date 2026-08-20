/* ==========================================================================
   Pillai & Sons Motor Company — main.js  —  V1
   Plain ES5-safe JavaScript. No framework, no build step, no dependencies.

   Responsibilities
     1.  Read window.SITE_CONFIG (generated from config/site-config.xlsx) and
         paint it onto CSS custom properties and every [data-biz] node.
     2.  Overlay any edits the owner saved in the admin panel (localStorage)
         onto [data-cms] nodes.
     3.  Navigation: sticky header, mobile drawer, three-level submenus.
     4.  Enquiry forms -> WhatsApp click-to-chat URL.
     5.  Visitor-facing colour switcher.
     6.  Model filters, counters, scroll reveal, back-to-top.

   Nothing here gates content: with JavaScript disabled every page is still
   complete and readable, because the defaults baked into the HTML are the same
   values this script would paint.
   ========================================================================== */
(function () {
  "use strict";

  /* ---------------------------------------------------------------- keys */
  var LS_CONTENT = "psm_site_content_v1";   // owner edits from the admin panel
  var LS_CONFIG  = "psm_site_config_v1";    // owner edits to business/colour/font settings
  var LS_THEME   = "psm_visitor_theme_v1";  // visitor's chosen palette

  /* ------------------------------------------------------------- helpers */
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  function readJSON(key) {
    try {
      var raw = window.localStorage.getItem(key);
      return raw ? JSON.parse(raw) : null;
    } catch (e) { return null; }
  }

  function writeJSON(key, value) {
    try { window.localStorage.setItem(key, JSON.stringify(value)); return true; }
    catch (e) { return false; }
  }

  function deepMerge(base, patch) {
    var out = {}, k;
    for (k in base) if (Object.prototype.hasOwnProperty.call(base, k)) out[k] = base[k];
    if (!patch) return out;
    for (k in patch) {
      if (!Object.prototype.hasOwnProperty.call(patch, k)) continue;
      if (patch[k] && typeof patch[k] === "object" && !(patch[k] instanceof Array) &&
          out[k] && typeof out[k] === "object" && !(out[k] instanceof Array)) {
        out[k] = deepMerge(out[k], patch[k]);
      } else {
        out[k] = patch[k];
      }
    }
    return out;
  }

  /* ------------------------------------------------------- resolved data */
  var baseConfig = window.SITE_CONFIG || { business: {}, colors: {}, fonts: {}, social: [], themes: [] };
  var savedConfig = readJSON(LS_CONFIG);
  var CONFIG = savedConfig ? deepMerge(baseConfig, savedConfig) : baseConfig;

  var biz    = CONFIG.business || {};
  var colors = CONFIG.colors   || {};
  var fonts  = CONFIG.fonts    || {};
  var social = CONFIG.social   || [];
  var themes = CONFIG.themes   || [];

  window.PSM = { config: CONFIG, keys: { content: LS_CONTENT, config: LS_CONFIG, theme: LS_THEME } };

  /* ==================================================================
     1.  TOKENS — paint config onto CSS custom properties
     ================================================================== */
  var COLOR_VARS = {
    primary: "--c-primary", primary_ink: "--c-primary-ink",
    secondary: "--c-secondary", tertiary: "--c-tertiary", tertiary_ink: "--c-tertiary-ink",
    heading: "--c-heading", text: "--c-text", accent_cream: "--c-cream",
    white_smoke: "--c-smoke", border: "--c-border", body_bg: "--c-body-bg",
    topbar_bg: "--c-topbar-bg", topbar_text: "--c-topbar-text", header_bg: "--c-header-bg",
    nav_link: "--c-nav-link", nav_link_active: "--c-nav-link-active",
    footer_bg: "--c-footer-bg", footer_text: "--c-footer-text",
    button_text: "--c-btn-text", star: "--c-star",
    // the five business channels
    ch_arena: "--c-ch-arena", ch_nexa: "--c-ch-nexa", ch_truevalue: "--c-ch-truevalue",
    ch_service: "--c-ch-service", ch_school: "--c-ch-school"
  };

  var FONT_VARS = {
    base_size: ["--fs-base", "px"], base_size_mobile: ["--fs-base-mobile", "px"],
    base_line_height: ["--lh-base", ""], base_weight: ["--fw-base", ""],
    h1_size: ["--fs-h1", "px"], h1_size_tablet: ["--fs-h1-t", "px"], h1_size_mobile: ["--fs-h1-m", "px"], h1_weight: ["--fw-h1", ""],
    h2_size: ["--fs-h2", "px"], h2_size_tablet: ["--fs-h2-t", "px"], h2_size_mobile: ["--fs-h2-m", "px"], h2_weight: ["--fw-h2", ""],
    h3_size: ["--fs-h3", "px"], h3_size_tablet: ["--fs-h3-t", "px"], h3_size_mobile: ["--fs-h3-m", "px"], h3_weight: ["--fw-h3", ""],
    h4_size: ["--fs-h4", "px"], h4_size_mobile: ["--fs-h4-m", "px"], h4_weight: ["--fw-h4", ""],
    h5_size: ["--fs-h5", "px"], h5_size_mobile: ["--fs-h5-m", "px"], h5_weight: ["--fw-h5", ""],
    h6_size: ["--fs-h6", "px"], h6_weight: ["--fw-h6", ""],
    heading_line_height: ["--lh-heading", ""],
    subheading_size: ["--fs-sub", "px"], subheading_weight: ["--fw-sub", ""], subheading_spacing: ["--ls-sub", "px"],
    nav_size: ["--fs-nav", "px"], nav_weight: ["--fw-nav", ""],
    button_size: ["--fs-btn", "px"], button_weight: ["--fw-btn", ""],
    button_radius: ["--r-btn", "px"], card_radius: ["--r-card", "px"],
    container_width: ["--w-container", "px"]
  };

  // NOTE: these write onto <html> as inline styles, which outrank every
  // stylesheet rule including media queries. That is why main.css reads its
  // own --fz-* values at the breakpoints rather than the --fs-* tokens set
  // here — see the "effective type sizes" block in main.css. Adding a token
  // here that the stylesheet also reassigns at a breakpoint will break that
  // breakpoint silently.
  var FALLBACK_STACK = ', "Segoe UI", Arial, sans-serif';

  function applyTokens(c, f) {
    var root = document.documentElement.style, key, v;

    for (key in COLOR_VARS) {
      v = c[key];
      if (v) root.setProperty(COLOR_VARS[key], v);
    }

    for (key in FONT_VARS) {
      v = f[key];
      if (v === undefined || v === null || v === "") continue;
      root.setProperty(FONT_VARS[key][0], String(v) + FONT_VARS[key][1]);
    }

    if (f.heading_family) root.setProperty("--f-heading", '"' + f.heading_family + '"' + FALLBACK_STACK);
    if (f.body_family)    root.setProperty("--f-body",    '"' + f.body_family + '"' + FALLBACK_STACK);
  }

  function loadRemoteFont(url) {
    if (!url || $('link[data-remote-font]')) return;
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = url;
    link.setAttribute("data-remote-font", "1");
    document.head.appendChild(link);
  }

  applyTokens(colors, fonts);
  loadRemoteFont(fonts.google_fonts_url);

  /* ==================================================================
     2.  BUSINESS DETAILS — [data-biz] and link builders
     ================================================================== */
  function digits(s) { return String(s || "").replace(/[^0-9]/g, ""); }

  function waNumber() {
    var n = digits(biz.whatsapp_number);
    if (n) return n;
    return digits(biz.phone_country_code || "91") + digits(biz.phone);
  }

  function waLink(message) {
    var n = waNumber();
    if (!n) return "#";
    return "https://wa.me/" + n + (message ? "?text=" + encodeURIComponent(message) : "");
  }

  var BIZ_DERIVED = {
    full_address: [biz.address_line1, biz.address_line2, biz.city, biz.state, biz.pincode]
      .filter(Boolean).join(", "),
    address_block: [biz.address_line1, biz.address_line2,
                    [biz.city, biz.pincode].filter(Boolean).join(" - "),
                    biz.state].filter(Boolean).join(", "),
    year: String(new Date().getFullYear()),
    whatsapp_link: waLink(biz.whatsapp_greeting)
  };

  function bizValue(key) {
    if (Object.prototype.hasOwnProperty.call(BIZ_DERIVED, key)) return BIZ_DERIVED[key];
    return biz[key] !== undefined ? biz[key] : "";
  }

  function paintBusiness() {
    $$("[data-biz]").forEach(function (el) {
      var v = bizValue(el.getAttribute("data-biz"));
      if (v !== "") el.textContent = v;
    });

    $$("[data-biz-href]").forEach(function (el) {
      var kind = el.getAttribute("data-biz-href");
      var cc = digits(biz.phone_country_code || "91");
      if (kind === "tel")              el.href = "tel:+" + cc + digits(biz.phone);
      else if (kind === "tel_service") el.href = "tel:+" + cc + digits(biz.phone_service || biz.phone);
      else if (kind === "mail")        el.href = "mailto:" + (biz.email || "");
      else if (kind === "mail_service") el.href = "mailto:" + (biz.email_service || biz.email || "");
      else if (kind === "wa")          el.href = waLink(el.getAttribute("data-wa-message") || biz.whatsapp_greeting);
      else if (kind === "map")         el.href = biz.map_link || "#";
    });

    $$("[data-biz-src]").forEach(function (el) {
      var kind = el.getAttribute("data-biz-src");
      if ((kind === "map" || kind === "map_embed") && biz.map_embed_url) el.src = biz.map_embed_url;
    });

    var byPlatform = {};
    social.forEach(function (s) { byPlatform[s.platform] = s; });
    $$("[data-social]").forEach(function (el) {
      var p = el.getAttribute("data-social");
      var s = byPlatform[p];
      if (!s || s.enabled === false) { el.style.display = "none"; return; }
      var url = s.url;
      if (p === "whatsapp" && !url) url = waLink(biz.whatsapp_greeting);
      if (!url) { el.style.display = "none"; return; }
      el.href = url;
      el.style.display = "";
      if (!/^(#|\/|\.)/.test(url)) { el.target = "_blank"; el.rel = "noopener"; }
    });
  }

  /* ==================================================================
     3.  CMS OVERLAY — owner edits saved from the admin panel
     ================================================================== */
  function contentStore() {
    // Published overrides (assets/js/content-overrides.js, exported from the
    // admin panel) apply to every visitor. Anything the owner has edited
    // locally but not yet published wins over them on their own machine.
    var published = window.SITE_CONTENT_OVERRIDES || {};
    var local = readJSON(LS_CONTENT) || {};
    var out = {}, k;
    for (k in published) if (Object.prototype.hasOwnProperty.call(published, k)) out[k] = published[k];
    for (k in local) if (Object.prototype.hasOwnProperty.call(local, k)) out[k] = local[k];
    return out;
  }
  window.PSM.contentStore = contentStore;

  function paintContent() {
    var store = contentStore();
    var n = 0;

    $$("[data-cms]").forEach(function (el) {
      var k = el.getAttribute("data-cms");
      if (store[k] !== undefined && store[k] !== null) { el.innerHTML = store[k]; n++; }
    });

    $$("[data-cms-src]").forEach(function (el) {
      var k = el.getAttribute("data-cms-src");
      if (store[k]) {
        el.src = store[k];
        el.removeAttribute("srcset");
        if (store[k].indexOf("data:") === 0) { el.removeAttribute("width"); el.removeAttribute("height"); }
        n++;
      }
    });

    $$("[data-cms-href]").forEach(function (el) {
      var k = el.getAttribute("data-cms-href");
      if (store[k]) { el.href = store[k]; n++; }
    });

    $$("[data-cms-embed]").forEach(function (el) {
      var k = el.getAttribute("data-cms-embed");
      if (store[k]) { el.src = toEmbedUrl(store[k]); n++; }
    });

    // Car illustrations. The site ships hand-drawn silhouettes because we are
    // the dealer, not the manufacturer, and cannot publish official product
    // photography. When the owner uploads real Maruti media-kit imagery from
    // the admin panel, it replaces the drawing in place.
    $$("[data-cms-art]").forEach(function (el) {
      var k = el.getAttribute("data-cms-art");
      if (!store[k]) return;
      var img = document.createElement("img");
      img.src = store[k];
      img.alt = el.getAttribute("data-art-alt") || "";
      img.loading = "lazy";
      img.decoding = "async";
      el.innerHTML = "";
      el.appendChild(img);
      n++;
    });

    return n;
  }

  function toEmbedUrl(url) {
    if (!url) return "";
    var m = url.match(/(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)([A-Za-z0-9_-]{6,})/);
    if (m) return "https://www.youtube.com/embed/" + m[1];
    var v = url.match(/vimeo\.com\/(\d+)/);
    if (v) return "https://player.vimeo.com/video/" + v[1];
    return url;
  }
  window.PSM.toEmbedUrl = toEmbedUrl;

  /* ==================================================================
     4.  NAVIGATION
     ================================================================== */
  function initNav() {
    var header   = $(".site-header");
    var nav      = $("#site-nav");
    var toggle   = $(".nav-toggle");
    var backdrop = $(".nav-backdrop");
    var closeBtn = $(".nav__close");

    if (!nav || !toggle) return;

    // Mirrors the CSS breakpoint exactly. If one changes, change both.
    var DRAWER_MQ = "(max-width: 1100px), (hover: none) and (pointer: coarse)";
    function isDrawer() { return window.matchMedia(DRAWER_MQ).matches; }

    function openNav() {
      nav.classList.add("is-open");
      toggle.setAttribute("aria-expanded", "true");
      if (backdrop) backdrop.classList.add("is-open");
      document.body.classList.add("is-locked");
    }
    function closeNav() {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      if (backdrop) backdrop.classList.remove("is-open");
      document.body.classList.remove("is-locked");
    }

    toggle.addEventListener("click", function () {
      if (nav.classList.contains("is-open")) closeNav(); else openNav();
    });
    if (backdrop) backdrop.addEventListener("click", closeNav);
    if (closeBtn) closeBtn.addEventListener("click", closeNav);

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) { closeNav(); toggle.focus(); }
    });

    // The expand buttons are already in the markup (one per parent item), so
    // the parent link itself always stays tappable on touch devices.
    $$(".submenu-toggle", nav).forEach(function (btn) {
      var sub = document.getElementById(btn.getAttribute("aria-controls"));
      if (!sub) return;
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        var open = sub.classList.toggle("is-open");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
      });
    });

    // Close the drawer after tapping a real destination.
    $$("a", nav).forEach(function (a) {
      a.addEventListener("click", function () {
        var href = a.getAttribute("href");
        if (isDrawer() && href && href.charAt(0) !== "#") closeNav();
      });
    });

    // Reset drawer state when resizing back up to desktop.
    var lastDrawer = isDrawer();
    window.addEventListener("resize", function () {
      var now = isDrawer();
      if (now !== lastDrawer) {
        lastDrawer = now;
        closeNav();
        $$(".submenu", nav).forEach(function (s) { s.classList.remove("is-open"); });
        $$(".submenu-toggle", nav).forEach(function (b) { b.setAttribute("aria-expanded", "false"); });
      }
    });

    // Third-level dropdowns flip leftwards when they would run off the screen.
    $$(".submenu .submenu", nav).forEach(function (sub) {
      var li = sub.parentNode;
      while (li && li.tagName !== "LI") li = li.parentNode;
      if (!li) return;
      li.addEventListener("mouseenter", function () {
        if (isDrawer()) return;
        sub.classList.remove("submenu--flip");
        var r = sub.getBoundingClientRect();
        if (r.right > window.innerWidth - 12) sub.classList.add("submenu--flip");
      });
    });

    if (header) {
      var onScroll = function () {
        header.classList.toggle("is-stuck", window.pageYOffset > 60);
      };
      window.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
    }
  }

  /* ==================================================================
     5.  FORMS -> WHATSAPP
     ================================================================== */
  var FIELD_LABELS = {
    name: "Name", email: "Email", phone: "Phone", city: "City",
    model: "Model of interest", channel: "Showroom", variant: "Variant",
    budget: "Budget", finance: "Finance needed", exchange: "Exchange car",
    reg_no: "Registration number", service_type: "Service type",
    preferred_date: "Preferred date", preferred_time: "Preferred time",
    pickup: "Pick-up required", course: "Course", subject: "Subject",
    message: "Message", role: "Applying for", experience: "Experience",
    current_car: "Current car", km_driven: "Kilometres driven", year: "Year of purchase"
  };

  function fieldError(input) {
    var wrap = input.parentNode;
    while (wrap && (!wrap.classList || !wrap.classList.contains("form-field"))) wrap = wrap.parentNode;
    return wrap ? wrap.querySelector(".field-error") : null;
  }

  function validateField(input) {
    var errEl = fieldError(input);
    var value = (input.value || "").trim();
    var msg = "";

    if (input.type === "checkbox") {
      if (input.hasAttribute("required") && !input.checked) msg = "Please tick this box to continue.";
    } else if (input.hasAttribute("required") && !value) {
      msg = "This field is required.";
    } else if (value && input.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) {
      msg = "Enter a valid email address.";
    } else if (value && input.type === "tel" && digits(value).length < 10) {
      msg = "Enter a 10-digit phone number.";
    }

    if (errEl) errEl.textContent = msg;
    if (msg) input.setAttribute("aria-invalid", "true");
    else input.removeAttribute("aria-invalid");
    return !msg;
  }

  function setStatus(el, state, html) {
    if (!el) return;
    el.setAttribute("data-state", state);
    el.innerHTML = html;
  }

  function initForms() {
    $$("form[data-wa-form]").forEach(function (form) {
      var status = form.querySelector(".form-status");
      var inputs = $$("input, select, textarea", form).filter(function (i) {
        if (i.type === "submit" || i.type === "button") return false;
        // Hidden fields join the message only when explicitly labelled — e.g.
        // the model name on a car page's test-drive form.
        if (i.type === "hidden") return i.hasAttribute("data-label");
        return true;
      });

      inputs.forEach(function (i) {
        i.addEventListener("blur", function () { validateField(i); });
        i.addEventListener("input", function () {
          if (i.getAttribute("aria-invalid") === "true") validateField(i);
        });
      });

      form.addEventListener("submit", function (e) {
        e.preventDefault();

        var ok = true, firstBad = null;
        inputs.forEach(function (i) {
          if (!validateField(i)) { ok = false; if (!firstBad) firstBad = i; }
        });

        if (!ok) {
          setStatus(status, "err", "Please correct the highlighted fields and try again.");
          if (firstBad) firstBad.focus();
          return;
        }

        var heading = form.getAttribute("data-wa-heading") || "New website enquiry";
        var lines = ["*" + heading + "*", ""];
        inputs.forEach(function (i) {
          var v;
          if (i.type === "checkbox") { v = i.checked ? "Yes" : ""; }
          else { v = (i.value || "").trim(); }
          if (!v) return;
          if (i.getAttribute("data-skip") === "1") return;
          var label = i.getAttribute("data-label") || FIELD_LABELS[i.name] || i.name;
          lines.push(label + ": " + v);
        });
        lines.push("");
        lines.push("Sent from " + (biz.business_name || "the website"));

        var url = waLink(lines.join("\n"));
        var win = window.open(url, "_blank", "noopener");

        setStatus(status, "ok", win
          ? "Thanks! Your enquiry is open in WhatsApp — press <strong>send</strong> there and it reaches our team."
          : 'Thanks! Your enquiry is ready. <a href="' + url + '" target="_blank" rel="noopener">' +
            "Tap here to open WhatsApp and send it.</a>");
        form.reset();
      });
    });

    $$("form[data-demo-form]").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var status = form.querySelector(".form-status") ||
                     (form.parentNode && form.parentNode.querySelector(".form-status"));
        setStatus(status, "ok",
          "Thanks for subscribing. (Demo only — connect a mailing-list service to store addresses.)");
        form.reset();
      });
    });
  }

  /* ==================================================================
     6.  VISITOR COLOUR SWITCHER
     ================================================================== */
  var SWITCHABLE = ["primary", "primary_ink", "secondary", "tertiary", "tertiary_ink",
                    "accent_cream", "footer_bg", "topbar_bg"];

  function applyVisitorTheme(theme) {
    if (!theme) return;
    var patch = {};
    SWITCHABLE.forEach(function (k) { if (theme[k]) patch[k] = theme[k]; });
    applyTokens(deepMerge(colors, patch), {});
  }

  function initThemeSwitcher() {
    var panel = $("#theme-panel");
    var fab   = $("#theme-fab");
    if (!panel || !fab) return;

    var grid  = $(".theme-panel__grid", panel);
    var saved = readJSON(LS_THEME);

    themes.forEach(function (t, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "theme-swatch";
      b.setAttribute("data-theme-index", String(i));
      b.setAttribute("aria-pressed", "false");
      b.innerHTML =
        '<span class="theme-swatch__dots" aria-hidden="true">' +
          '<span style="background:' + t.primary + '"></span>' +
          '<span style="background:' + t.secondary + '"></span>' +
          '<span style="background:' + t.tertiary + '"></span>' +
        "</span><span>" + t.name + "</span>";
      b.addEventListener("click", function () {
        applyVisitorTheme(t);
        writeJSON(LS_THEME, t);
        markActive(t.name);
        syncPickers(t);
      });
      if (grid) grid.appendChild(b);
    });

    function markActive(name) {
      $$(".theme-swatch", panel).forEach(function (b) {
        var idx = parseInt(b.getAttribute("data-theme-index"), 10);
        var on = themes[idx] && themes[idx].name === name;
        b.setAttribute("aria-pressed", on ? "true" : "false");
      });
    }

    var pickers = {
      primary:   $("#tp-primary", panel),
      secondary: $("#tp-secondary", panel),
      tertiary:  $("#tp-tertiary", panel)
    };

    function syncPickers(t) {
      Object.keys(pickers).forEach(function (k) {
        if (pickers[k] && t[k]) pickers[k].value = t[k];
      });
    }

    Object.keys(pickers).forEach(function (k) {
      if (!pickers[k]) return;
      pickers[k].addEventListener("input", function () {
        var current = readJSON(LS_THEME) || {
          name: "Custom", primary: colors.primary, primary_ink: colors.primary_ink,
          secondary: colors.secondary, tertiary: colors.tertiary,
          tertiary_ink: colors.tertiary_ink, accent_cream: colors.accent_cream,
          footer_bg: colors.footer_bg, topbar_bg: colors.topbar_bg
        };
        current.name = "Custom";
        current[k] = pickers[k].value;
        // The ink variants carry white text; keeping them in step with the
        // picked colour is what stops the buttons failing contrast.
        if (k === "primary")  current.primary_ink = darken(pickers[k].value, 5.15);
        if (k === "tertiary") current.tertiary_ink = darken(pickers[k].value, 4.6);
        if (k === "secondary") { current.footer_bg = pickers[k].value; current.topbar_bg = pickers[k].value; }
        applyVisitorTheme(current);
        writeJSON(LS_THEME, current);
        markActive("Custom");
      });
    });

    var resetBtn = $("#theme-reset", panel);
    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        try { window.localStorage.removeItem(LS_THEME); } catch (e) {}
        applyTokens(colors, fonts);
        markActive(themes.length ? themes[0].name : "");
        if (themes.length) syncPickers(themes[0]);
      });
    }

    function closePanel() { panel.classList.remove("is-open"); fab.setAttribute("aria-expanded", "false"); }
    var closeBtn = $("#theme-close", panel);
    if (closeBtn) closeBtn.addEventListener("click", closePanel);

    fab.addEventListener("click", function () {
      var open = panel.classList.toggle("is-open");
      fab.setAttribute("aria-expanded", open ? "true" : "false");
    });

    document.addEventListener("click", function (e) {
      if (!panel.classList.contains("is-open")) return;
      if (panel.contains(e.target) || fab.contains(e.target)) return;
      closePanel();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closePanel();
    });

    if (saved) { applyVisitorTheme(saved); markActive(saved.name); syncPickers(saved); }
    else if (themes.length) { markActive(themes[0].name); syncPickers(themes[0]); }
  }

  /* Relative luminance, so a colour the visitor picks can be darkened just far
     enough to carry white text at WCAG AA. Same maths as tools/config_schema.py. */
  function lin(c) {
    c = c / 255;
    return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  }
  function contrastOnWhite(hex) {
    var h = hex.replace("#", "");
    var r = parseInt(h.substr(0, 2), 16), g = parseInt(h.substr(2, 2), 16), b = parseInt(h.substr(4, 2), 16);
    var L = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
    return 1.05 / (L + 0.05);
  }
  function darken(hex, target) {
    var h = hex.replace("#", "");
    var r = parseInt(h.substr(0, 2), 16), g = parseInt(h.substr(2, 2), 16), b = parseInt(h.substr(4, 2), 16);
    for (var s = 0; s <= 100; s++) {
      var f = 1 - s / 100;
      var cand = "#" + [r, g, b].map(function (v) {
        var x = Math.round(v * f).toString(16);
        return x.length < 2 ? "0" + x : x;
      }).join("");
      if (contrastOnWhite(cand) >= target) return cand;
    }
    return "#000000";
  }

  // Apply the saved visitor theme immediately (before paint) to avoid a flash.
  (function () {
    var saved = readJSON(LS_THEME);
    if (saved) applyVisitorTheme(saved);
  }());

  /* ==================================================================
     7.  ACCORDION — <details> is native; this only adds "one open at a time"
     ================================================================== */
  function initAccordions() {
    $$(".accordion[data-single]").forEach(function (acc) {
      var items = $$("details", acc);
      items.forEach(function (d) {
        d.addEventListener("toggle", function () {
          if (!d.open) return;
          items.forEach(function (o) { if (o !== d) o.open = false; });
        });
      });
    });
  }

  /* ==================================================================
     8.  MODEL FILTERS
     ================================================================== */
  function initFilters() {
    $$(".filter-bar").forEach(function (bar) {
      var targetSel = bar.getAttribute("data-filter-target");
      var target = targetSel ? $(targetSel) : bar.nextElementSibling;
      if (!target) return;
      var items = $$("[data-cat]", target);
      var empty = $(".filter-empty", target.parentNode || document);

      $$("button", bar).forEach(function (btn) {
        btn.addEventListener("click", function () {
          var cat = btn.getAttribute("data-filter");
          $$("button", bar).forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
          btn.setAttribute("aria-pressed", "true");

          var shown = 0;
          items.forEach(function (it) {
            var cats = (it.getAttribute("data-cat") || "").split(" ");
            var show = cat === "all" || cats.indexOf(cat) > -1;
            it.hidden = !show;
            if (show) shown++;
          });
          if (empty) empty.hidden = shown > 0;
        });
      });
    });
  }

  /* ==================================================================
     9.  SCROLL EFFECTS — reveal + counters
     ================================================================== */
  function initScrollFx() {
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var reveals  = $$(".reveal");
    var counters = $$("[data-count]");

    if (reduce || !("IntersectionObserver" in window)) {
      reveals.forEach(function (el) { el.classList.add("is-in"); });
      // The markup already carries the final figure; nothing to do.
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        io.unobserve(el);

        if (el.classList.contains("reveal")) el.classList.add("is-in");

        if (el.hasAttribute("data-count")) {
          var end = parseInt(el.getAttribute("data-count"), 10) || 0;
          // Zero it here, not in the markup: if this callback never runs the
          // visitor still reads the real number rather than a row of zeros.
          el.textContent = "0";
          var start = null, dur = 1400;
          var step = function (ts) {
            if (start === null) start = ts;
            var p = Math.min((ts - start) / dur, 1);
            el.textContent = format(Math.floor(p * (2 - p) * end));
            if (p < 1) requestAnimationFrame(step); else el.textContent = format(end);
          };
          requestAnimationFrame(step);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.15 });

    reveals.concat(counters).forEach(function (el) { io.observe(el); });
  }

  // Indian digit grouping: 18000 -> 18,000 and 1650000 -> 16,50,000
  function format(n) {
    var s = String(parseInt(n, 10) || 0);
    if (s.length <= 3) return s;
    var last3 = s.slice(-3);
    var rest = s.slice(0, -3).replace(/\B(?=(\d{2})+(?!\d))/g, ",");
    return rest + "," + last3;
  }

  /* ==================================================================
     10.  MISC — back to top, current year, click-to-play video
     ================================================================== */
  function initMisc() {
    var top = $("#back-to-top");
    if (top) {
      window.addEventListener("scroll", function () {
        top.classList.toggle("is-visible", window.pageYOffset > 500);
      }, { passive: true });
      top.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    }

    $$("[data-video-target]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var holder = document.getElementById(btn.getAttribute("data-video-target"));
        if (!holder) return;
        var store = contentStore();
        var key = holder.getAttribute("data-cms-embed");
        var url = (key && store[key]) || holder.getAttribute("data-default-video") || "";
        if (!url) return;
        var src = toEmbedUrl(url);
        var iframe = document.createElement("iframe");
        iframe.src = src + (src.indexOf("?") > -1 ? "&" : "?") + "autoplay=1";
        iframe.title = "Video";
        iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
        iframe.allowFullscreen = true;
        iframe.style.cssText = "position:absolute;inset:0;width:100%;height:100%;border:0;";
        holder.innerHTML = "";
        holder.appendChild(iframe);
      });
    });

    $$("[data-year]").forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

    // Pre-fill an enquiry form from ?model=swift so the "Enquire" buttons on a
    // model page land on the contact form with the right car already chosen.
    var m = /[?&]model=([^&]+)/.exec(window.location.search);
    if (m) {
      var want = decodeURIComponent(m[1]).toLowerCase();
      $$("select[name='model']").forEach(function (sel) {
        $$("option", sel).forEach(function (o) {
          if (o.value.toLowerCase() === want) sel.value = o.value;
        });
      });
    }
  }

  /* ==================================================================
     BOOT
     ================================================================== */
  function boot() {
    paintBusiness();
    paintContent();
    initNav();
    initForms();
    initThemeSwitcher();
    initAccordions();
    initFilters();
    initScrollFx();
    initMisc();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
}());
