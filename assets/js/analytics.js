/* ==========================================================================
   analytics.js — V1
   Google Analytics 4 for pillaiandsons.in

   SETUP: put your Measurement ID on the GA_ID line below. Until you do, this
   file loads nothing and sends nothing, so it is safe to ship as-is.

        var GA_ID = "G-XXXXXXXXXX";

   What it records, on every page, without you tagging anything by hand:

     page_view        automatic
     call_click       any tel: link      → which branch, which city, where on the page
     whatsapp_click   any WhatsApp link  → same
     email_click      any mailto: link
     directions_click branch card "Directions"
     map_click        branch card "Map"
     review_click     branch card "Review"
     review_qr_open   branch card QR code enlarged
     city_select      branch finder dropdown → which city was chosen
     form_submit      every enquiry form, named

   Branch name and city are read from the branch card the link sits in, so a
   call from the Thanjavur ARENA card is distinguishable from one in Trichy.

   Parameter names are deliberately prefixed: GA4 already has a built-in
   geographic dimension called "City", and a custom parameter with the same
   name is confusing to read in reports. Hence branch_city, not city.
   ========================================================================== */
(function () {
  "use strict";

  var GA_ID = "G-XXXXXXXXXX";           // <-- replace with your Measurement ID

  // Not configured yet, or a browser too old for delegated lookups: do nothing.
  if (!/^G-[A-Z0-9]{4,}$/i.test(GA_ID)) return;
  if (!document.querySelector || !Element.prototype.closest) return;

  /* ----------------------------------------------------------- load gtag */
  var tag = document.createElement("script");
  tag.async = true;
  tag.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(GA_ID);
  (document.head || document.documentElement).appendChild(tag);

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag("js", new Date());
  gtag("config", GA_ID);

  /* --------------------------------------------------------- small helpers */
  function txt(el) { return el ? String(el.textContent || "").replace(/\s+/g, " ").trim() : ""; }

  function send(name, params) {
    try { gtag("event", name, params || {}); } catch (e) {}
  }

  /* Where was this clicked, and does it belong to a branch? */
  function context(el) {
    var card = el.closest(".bf-card");
    if (card) {
      var soft = card.querySelectorAll(".bf-tag--soft");
      return {
        branch_name: txt(card.querySelector("h3")) || "(unnamed branch)",
        branch_city: txt(soft[soft.length - 1]) || "(unknown city)",
        link_source: "branch_card"
      };
    }
    var where = el.closest(".fab-stack") ? "floating_button"
              : el.closest("footer")     ? "footer"
              : el.closest("header")     ? "header"
              : "page_body";
    return { branch_name: "(not branch specific)", branch_city: "(not branch specific)", link_source: where };
  }

  function label(el) {
    // The visible wording of a branch-card button, so Directions/Map/Review
    // can be told apart even if the href pattern changes later.
    return txt(el).toLowerCase();
  }

  /* ------------------------------------------------------------- clicks */
  document.addEventListener("click", function (e) {
    var el = e.target.closest ? e.target.closest("a, button") : null;
    if (!el) return;

    var href = el.getAttribute("href") || "";
    var c = context(el);

    /* QR enlarge button on a branch card */
    if (el.classList.contains("bf-qr")) {
      c.branch_name = el.getAttribute("data-qr-title") || c.branch_name;
      send("review_qr_open", c);
      return;
    }

    /* Click to call */
    if (href.indexOf("tel:") === 0) {
      c.phone_number = href.replace("tel:", "");
      send("call_click", c);
      return;
    }

    /* Click to WhatsApp. The floating button's href is "#" until main.js
       rewrites it from the config, so match the attribute as well. */
    if (href.indexOf("wa.me") > -1 ||
        href.indexOf("api.whatsapp.com") > -1 ||
        el.getAttribute("data-biz-href") === "wa") {
      send("whatsapp_click", c);
      return;
    }

    /* Click to email */
    if (href.indexOf("mailto:") === 0) {
      c.email_address = href.replace("mailto:", "").split("?")[0];
      send("email_click", c);
      return;
    }

    /* Branch card actions */
    if (el.classList.contains("bf-btn")) {
      var l = label(el);
      if (l.indexOf("direction") > -1) { send("directions_click", c); return; }
      if (l.indexOf("review") > -1)    { send("review_click", c);     return; }
      if (l.indexOf("map") > -1)       { send("map_click", c);        return; }
    }
  }, true);

  /* --------------------------------------------------- city dropdown */
  document.addEventListener("change", function (e) {
    var el = e.target;
    if (!el || el.id !== "bf-city") return;
    var city = el.value;
    send("city_select", {
      branch_city: city || "(cleared)",
      link_source: location.pathname.indexOf("contact") > -1 ? "contact_page" : "home_page"
    });
  });

  /* -------------------------------------------------------- form submits */
  document.addEventListener("submit", function (e) {
    var f = e.target;
    if (!f || f.nodeName !== "FORM") return;

    var name = f.getAttribute("data-wa-heading") ||
               f.getAttribute("id") ||
               "unnamed form";
    var kind = f.hasAttribute("data-wa-form") ? "whatsapp"
             : f.getAttribute("id") === "careers-form" ? "google_sheet"
             : "other";

    send("form_submit", {
      form_name: name,
      form_destination: kind,
      link_source: location.pathname
    });
  }, true);
})();
