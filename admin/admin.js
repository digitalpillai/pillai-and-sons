/* ==========================================================================
   admin.js  —  V2
   The site owner's editor. Vanilla JavaScript, no dependencies, no backend.

   Storage model
     psm_site_config_v1   -> partial overrides of window.SITE_CONFIG
                            { business:{}, colors:{}, fonts:{}, social:[], themes:[] }
     psm_site_content_v1  -> flat map  { "home.hero.title": "…", … }

   assets/js/main.js reads both on every page of the public site and paints
   them over the defaults, so a plain browser refresh shows the change.

   The .xlsx reader is hand-written: an XLSX file is a ZIP of XML parts, and
   modern browsers can inflate deflate streams natively via DecompressionStream.
   No spreadsheet library is used or needed.
   ========================================================================== */
(function () {
  "use strict";

  var LS_CONFIG = "psm_site_config_v1";
  var LS_CONTENT = "psm_site_content_v1";

  var BASE_CONFIG = window.SITE_CONFIG || { business: {}, colors: {}, fonts: {}, social: [], themes: [] };
  var META = window.SITE_CONFIG_META || { business: [], colors: [], fonts: [] };
  var CONTENT = window.SITE_CONTENT || { groups: [] };

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  function clone(o) { return JSON.parse(JSON.stringify(o)); }

  function readJSON(key, fallback) {
    try {
      var raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : clone(fallback);
    } catch (e) { return clone(fallback); }
  }

  /* ------------------------------------------------------- working state */
  var cfgOverrides = readJSON(LS_CONFIG, {});
  var contentOverrides = readJSON(LS_CONTENT, {});
  var dirty = false;

  function cfgValue(section, key) {
    if (cfgOverrides[section] && cfgOverrides[section][key] !== undefined) {
      return cfgOverrides[section][key];
    }
    return (BASE_CONFIG[section] || {})[key] !== undefined ? BASE_CONFIG[section][key] : "";
  }

  function setCfg(section, key, value) {
    if (!cfgOverrides[section]) cfgOverrides[section] = {};
    if (String(value) === String((BASE_CONFIG[section] || {})[key])) {
      delete cfgOverrides[section][key];
      if (!Object.keys(cfgOverrides[section]).length) delete cfgOverrides[section];
    } else {
      cfgOverrides[section][key] = value;
    }
    markDirty();
  }

  function contentValue(key, fallback) {
    return contentOverrides[key] !== undefined ? contentOverrides[key] : fallback;
  }

  function setContent(key, value, original) {
    if (value === original) delete contentOverrides[key];
    else contentOverrides[key] = value;
    markDirty();
  }

  function markDirty() {
    dirty = true;
    var el = $("#save-state");
    el.classList.add("is-dirty");
    $("#save-text").textContent = "Unsaved changes";
  }

  function markClean() {
    dirty = false;
    var el = $("#save-state");
    el.classList.remove("is-dirty");
    $("#save-text").textContent = "All changes saved";
  }

  /* ---------------------------------------------------------------- ui */
  var toastTimer;
  function toast(msg, isError) {
    var t = $("#toast");
    t.textContent = msg;
    t.className = "a-toast is-on" + (isError ? " a-toast--err" : "");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.className = "a-toast"; }, 3200);
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined) n.textContent = text;
    return n;
  }

  function field(labelText, hintText, control, changed) {
    var wrap = el("div", "a-field" + (changed ? " is-changed" : ""));
    var id = control.id || ("f-" + Math.random().toString(36).slice(2, 9));
    control.id = id;
    var lab = el("label", null, labelText);
    lab.setAttribute("for", id);
    wrap.appendChild(lab);
    wrap.appendChild(control);
    if (hintText) wrap.appendChild(el("span", "hint", hintText));
    return wrap;
  }

  /* ==================================================================
     TABS
     ================================================================== */
  $$(".a-tab").forEach(function (tab) {
    tab.addEventListener("click", function () {
      $$(".a-tab").forEach(function (t) { t.classList.remove("is-active"); });
      $$(".a-panel").forEach(function (p) { p.classList.remove("is-active"); });
      tab.classList.add("is-active");
      $("#panel-" + tab.getAttribute("data-panel")).classList.add("is-active");
      window.scrollTo({ top: 0, behavior: "smooth" });
      if (tab.getAttribute("data-panel") === "colours") refreshPreview();
      if (tab.getAttribute("data-panel") === "publish") updateStorageMeter();
    });
  });

  /* ==================================================================
     BUSINESS / COLOURS / FONTS FORMS
     ================================================================== */
  function buildConfigForm(section, mountSel) {
    var mount = $(mountSel);
    mount.innerHTML = "";
    (META[section] || []).forEach(function (f) {
      var current = cfgValue(section, f.k);
      var base = (BASE_CONFIG[section] || {})[f.k];
      var changed = String(current) !== String(base);
      var control, wrap;

      if (f.t === "color") {
        control = el("div", "a-color");
        var swatch = document.createElement("input");
        swatch.type = "color";
        swatch.value = normaliseHex(current);
        swatch.setAttribute("aria-label", f.l + " colour picker");
        var text = document.createElement("input");
        text.type = "text";
        text.value = current;
        text.spellcheck = false;
        control.appendChild(swatch);
        control.appendChild(text);

        swatch.addEventListener("input", function () {
          text.value = swatch.value.toUpperCase();
          setCfg(section, f.k, text.value);
          flagChanged(wrap, section, f.k);
          livePreviewColours();
        });
        text.addEventListener("input", function () {
          if (/^#[0-9a-fA-F]{3,8}$/.test(text.value)) swatch.value = normaliseHex(text.value);
          setCfg(section, f.k, text.value);
          flagChanged(wrap, section, f.k);
          livePreviewColours();
        });
        control.id = "c-" + f.k;
      } else if (f.t === "font") {
        control = document.createElement("select");
        ["Montserrat", "Poppins", "Georgia", "Times New Roman", "Arial", "Verdana", "Tahoma"]
          .forEach(function (name) {
            var o = document.createElement("option");
            o.value = name; o.textContent = name + (name === "Montserrat" || name === "Poppins" ? "  (bundled)" : "");
            control.appendChild(o);
          });
        if (current && !Array.prototype.some.call(control.options, function (o) { return o.value === current; })) {
          var extra = document.createElement("option");
          extra.value = current; extra.textContent = current + "  (custom)";
          control.appendChild(extra);
        }
        control.value = current;
        control.addEventListener("change", function () {
          setCfg(section, f.k, control.value);
          flagChanged(wrap, section, f.k);
        });
      } else if (f.t === "textarea") {
        control = document.createElement("textarea");
        control.value = current;
        control.addEventListener("input", function () {
          setCfg(section, f.k, control.value);
          flagChanged(wrap, section, f.k);
        });
      } else {
        control = document.createElement("input");
        control.type = f.t === "number" ? "number" : (f.t === "url" ? "url" : "text");
        if (f.t === "number") { control.step = "any"; }
        control.value = current;
        control.addEventListener("input", function () {
          setCfg(section, f.k, control.value);
          flagChanged(wrap, section, f.k);
        });
      }

      wrap = field(f.l, f.h, control, changed);
      if (f.t === "textarea" || f.k === "map_embed_url") wrap.style.gridColumn = "1 / -1";
      mount.appendChild(wrap);
    });
  }

  function flagChanged(wrap, section, key) {
    var changed = cfgOverrides[section] && cfgOverrides[section][key] !== undefined;
    wrap.classList.toggle("is-changed", !!changed);
  }

  function normaliseHex(v) {
    v = String(v || "").trim();
    if (/^#[0-9a-fA-F]{6}$/.test(v)) return v;
    if (/^#[0-9a-fA-F]{3}$/.test(v)) {
      return "#" + v[1] + v[1] + v[2] + v[2] + v[3] + v[3];
    }
    if (/^#[0-9a-fA-F]{8}$/.test(v)) return v.slice(0, 7);
    return "#000000";
  }

  /* ---- palettes -------------------------------------------------------- */
  function buildPalettes() {
    var mount = $("#palette-list");
    mount.innerHTML = "";
    (BASE_CONFIG.themes || []).forEach(function (t) {
      var b = el("button", "a-swatch");
      b.type = "button";
      b.innerHTML = '<span class="chips">' +
        '<i style="background:' + t.primary + '"></i>' +
        '<i style="background:' + t.secondary + '"></i>' +
        '<i style="background:' + t.tertiary + '"></i>' +
        '<i style="background:' + t.accent_cream + '"></i></span>' +
        '<span>' + t.name + '</span>';
      b.addEventListener("click", function () {
        setCfg("colors", "primary", t.primary);
        setCfg("colors", "secondary", t.secondary);
        setCfg("colors", "tertiary", t.tertiary);
        setCfg("colors", "accent_cream", t.accent_cream);
        setCfg("colors", "footer_bg", t.footer_bg);
        setCfg("colors", "topbar_bg", t.topbar_bg);
        buildConfigForm("colors", "#form-colours");
        livePreviewColours();
        toast("Palette “" + t.name + "” applied — remember to save");
      });
      mount.appendChild(b);
    });
  }

  /* ---- live preview ---------------------------------------------------- */
  var previewLoaded = false;
  function refreshPreview() {
    var frame = $("#preview-frame");
    if (!previewLoaded) {
      frame.src = "../index.html";
      previewLoaded = true;
      frame.addEventListener("load", livePreviewColours);
    } else {
      livePreviewColours();
    }
  }

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

  function livePreviewColours() {
    var frame = $("#preview-frame");
    if (!frame || !frame.contentDocument) return;
    var root = frame.contentDocument.documentElement;
    if (!root || !root.style) return;
    Object.keys(COLOR_VARS).forEach(function (k) {
      var v = cfgValue("colors", k);
      if (v) root.style.setProperty(COLOR_VARS[k], v);
    });
  }

  var refreshBtn = $("#btn-refresh-preview");
  if (refreshBtn) {
    refreshBtn.addEventListener("click", function () {
      previewLoaded = false;
      refreshPreview();
    });
  }

  /* ==================================================================
     SOCIAL
     ================================================================== */
  function socialList() {
    if (cfgOverrides.social) return cfgOverrides.social;
    return clone(BASE_CONFIG.social || []);
  }

  function buildSocialForm() {
    var mount = $("#form-social");
    mount.innerHTML = "";
    var list = socialList();

    list.forEach(function (s, i) {
      var row = el("div", "a-field");
      row.style.marginBottom = "18px";

      var head = el("div", "a-row");
      var lab = el("label", null, s.label || s.platform);
      lab.style.fontSize = "13.5px";
      head.appendChild(lab);

      var sw = el("label", "a-switch");
      var cb = document.createElement("input");
      cb.type = "checkbox";
      cb.checked = s.enabled !== false;
      sw.appendChild(cb);
      sw.appendChild(el("span", null, "Show on site"));
      sw.style.marginLeft = "auto";
      head.appendChild(sw);
      row.appendChild(head);

      var input = document.createElement("input");
      input.type = "url";
      input.value = s.url || "";
      input.placeholder = s.platform === "whatsapp"
        ? "Leave blank to use your WhatsApp number"
        : "https://…";
      row.appendChild(input);

      function push() {
        var next = socialList();
        next[i] = { platform: s.platform, url: input.value.trim(),
                    enabled: cb.checked, label: s.label };
        cfgOverrides.social = next;
        markDirty();
      }
      input.addEventListener("input", push);
      cb.addEventListener("change", push);

      mount.appendChild(row);
    });
  }

  /* ==================================================================
     PAGE CONTENT
     ================================================================== */
  function isImage(f) { return f.t === "image"; }
  function isVideo(f) { return f.t === "url"; }

  function buildContentForms() {
    var textMount = $("#form-content");
    var imgMount = $("#form-images");
    textMount.innerHTML = "";
    imgMount.innerHTML = "";
    var nText = 0, nMedia = 0;

    CONTENT.groups.forEach(function (group, gi) {
      var textFields = group.fields.filter(function (f) { return !isImage(f) && !isVideo(f); });
      var mediaFields = group.fields.filter(function (f) { return isImage(f) || isVideo(f); });
      nText += textFields.length;
      nMedia += mediaFields.length;
      if (textFields.length) textMount.appendChild(groupBlock(group, textFields, "t" + gi, false));
      if (mediaFields.length) imgMount.appendChild(groupBlock(group, mediaFields, "m" + gi, true));
    });

    $("#tab-content-n").textContent = nText;
    $("#tab-images-n").textContent = nMedia;
  }

  function groupBlock(group, fields, idPrefix, media) {
    var wrap = el("div", "a-group");
    wrap.setAttribute("data-group", group.name.toLowerCase());

    var bodyId = "g-" + idPrefix;
    var btn = el("button", "a-group__btn");
    btn.type = "button";
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-controls", bodyId);
    btn.innerHTML = '<span>' + escapeHtml(group.name) + '</span>' +
      '<span class="n">' + fields.length + (media ? " item" : " field") +
      (fields.length === 1 ? "" : "s") + '</span>' +
      '<svg class="chev" viewBox="0 0 12 8" fill="none" aria-hidden="true">' +
      '<path d="M1 1.5 6 6.5l5-5" stroke="currentColor" stroke-width="2" ' +
      'stroke-linecap="round" stroke-linejoin="round"/></svg>';

    var body = el("div", "a-group__body");
    body.id = bodyId;

    var built = false;
    btn.addEventListener("click", function () {
      var open = body.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      if (open && !built) {
        built = true;
        fields.forEach(function (f) {
          body.appendChild(media ? mediaField(f) : textField(f));
        });
      }
    });

    wrap.appendChild(btn);
    wrap.appendChild(body);
    return wrap;
  }

  function textField(f) {
    var current = contentValue(f.k, f.v);
    var changed = contentOverrides[f.k] !== undefined;
    var control;

    if (String(current).length > 90 || f.t === "rich") {
      control = document.createElement("textarea");
      if (String(current).length > 260) control.className = "tall";
    } else {
      control = document.createElement("input");
      control.type = "text";
    }
    control.value = current;

    var wrap = field(f.l, "key: " + f.k, control, changed);
    control.addEventListener("input", function () {
      setContent(f.k, control.value, f.v);
      wrap.classList.toggle("is-changed", contentOverrides[f.k] !== undefined);
    });

    var revert = el("button", "a-btn a-btn--ghost a-btn--sm", "Revert to original");
    revert.type = "button";
    revert.style.alignSelf = "flex-start";
    revert.addEventListener("click", function () {
      control.value = f.v;
      delete contentOverrides[f.k];
      wrap.classList.remove("is-changed");
      markDirty();
    });
    wrap.appendChild(revert);
    return wrap;
  }

  function mediaField(f) {
    var current = contentValue(f.k, f.v);
    var changed = contentOverrides[f.k] !== undefined;

    var wrap = el("div", "a-field" + (changed ? " is-changed" : ""));
    var lab = el("label", null, f.l);
    wrap.appendChild(lab);

    if (isVideo(f)) {
      var input = document.createElement("input");
      input.type = "url";
      input.value = current;
      input.placeholder = "https://www.youtube.com/watch?v=…";
      var id = "v-" + f.k.replace(/[^a-z0-9]/gi, "-");
      input.id = id;
      lab.setAttribute("for", id);
      wrap.appendChild(input);
      wrap.appendChild(el("span", "hint",
        "Paste a YouTube or Vimeo link. It is converted to an embed automatically."));
      input.addEventListener("input", function () {
        setContent(f.k, input.value, f.v);
        wrap.classList.toggle("is-changed", contentOverrides[f.k] !== undefined);
      });
      return wrap;
    }

    var box = el("div", "a-image");
    var prev = el("div", "a-image__preview");
    var img = document.createElement("img");
    img.alt = "";
    img.src = resolvePreview(current);
    prev.appendChild(img);

    var ctrl = el("div", "a-image__ctrl");
    var row = el("div", "row");

    var upBtn = el("button", "a-btn a-btn--sm", "Upload new image");
    upBtn.type = "button";
    var file = document.createElement("input");
    file.type = "file";
    file.accept = "image/*";
    file.className = "sr-only";

    var revert = el("button", "a-btn a-btn--ghost a-btn--sm", "Revert");
    revert.type = "button";

    row.appendChild(upBtn);
    row.appendChild(revert);
    ctrl.appendChild(row);

    var note = el("span", "hint", changed ? "Using your uploaded image." : "Using the original image.");
    ctrl.appendChild(note);

    upBtn.addEventListener("click", function () { file.click(); });
    file.addEventListener("change", function () {
      var f0 = file.files && file.files[0];
      if (!f0) return;
      if (!/^image\//.test(f0.type)) { toast("That is not an image file", true); return; }
      downscale(f0, function (dataUrl, kb) {
        setContent(f.k, dataUrl, f.v);
        img.src = dataUrl;
        wrap.classList.add("is-changed");
        note.textContent = "Using your uploaded image (" + kb + " KB).";
        toast("Image replaced — remember to save");
        updateStorageMeter();
      });
      file.value = "";
    });

    revert.addEventListener("click", function () {
      delete contentOverrides[f.k];
      img.src = resolvePreview(f.v);
      wrap.classList.remove("is-changed");
      note.textContent = "Using the original image.";
      markDirty();
      updateStorageMeter();
    });

    box.appendChild(prev);
    box.appendChild(ctrl);
    box.appendChild(file);
    wrap.appendChild(box);
    return wrap;
  }

  function resolvePreview(src) {
    if (!src) return "";
    if (src.indexOf("data:") === 0 || /^https?:/.test(src)) return src;
    return "../" + src.replace(/^(\.\.\/)+/, "");
  }

  /* ---- image downscaling ---------------------------------------------- */
  function downscale(file, done) {
    var reader = new FileReader();
    reader.onload = function () {
      var image = new Image();
      image.onload = function () {
        var MAX = 1600;
        var w = image.width, h = image.height;
        if (w > MAX || h > MAX) {
          var r = Math.min(MAX / w, MAX / h);
          w = Math.round(w * r); h = Math.round(h * r);
        }
        var canvas = document.createElement("canvas");
        canvas.width = w; canvas.height = h;
        canvas.getContext("2d").drawImage(image, 0, 0, w, h);
        var q = 0.82, out = canvas.toDataURL("image/jpeg", q);
        while (out.length > 700000 && q > 0.4) {
          q -= 0.12;
          out = canvas.toDataURL("image/jpeg", q);
        }
        done(out, Math.round(out.length / 1024));
      };
      image.onerror = function () { toast("Could not read that image", true); };
      image.src = reader.result;
    };
    reader.onerror = function () { toast("Could not read that file", true); };
    reader.readAsDataURL(file);
  }

  /* ---- search ---------------------------------------------------------- */
  function wireSearch(inputSel, mountSel) {
    var input = $(inputSel);
    if (!input) return;
    input.addEventListener("input", function () {
      var term = input.value.trim().toLowerCase();
      $$(".a-group", $(mountSel)).forEach(function (g) {
        if (!term) { g.style.display = ""; return; }
        var hay = g.getAttribute("data-group") + " " + g.textContent.toLowerCase();
        g.style.display = hay.indexOf(term) > -1 ? "" : "none";
      });
    });
  }

  /* ==================================================================
     SAVE / EXPORT / RESET
     ================================================================== */
  function save() {
    try {
      localStorage.setItem(LS_CONFIG, JSON.stringify(cfgOverrides));
      localStorage.setItem(LS_CONTENT, JSON.stringify(contentOverrides));
      markClean();
      updateStorageMeter();
      toast("Saved. Refresh the website to see the change.");
    } catch (e) {
      toast("Could not save — browser storage is full. Remove a large image and try again.", true);
    }
  }

  $("#btn-save").addEventListener("click", save);
  $("#btn-save-2").addEventListener("click", save);

  $("#btn-preview").addEventListener("click", function () {
    if (dirty) save();
    window.open("../index.html", "_blank", "noopener");
  });

  window.addEventListener("beforeunload", function (e) {
    if (!dirty) return;
    e.preventDefault();
    e.returnValue = "";
  });

  function download(name, text, mime) {
    var blob = new Blob([text], { type: mime || "text/plain;charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url; a.download = name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 1500);
  }

  function mergedConfig() {
    var out = clone(BASE_CONFIG);
    ["business", "colors", "fonts"].forEach(function (s) {
      if (cfgOverrides[s]) {
        Object.keys(cfgOverrides[s]).forEach(function (k) { out[s][k] = cfgOverrides[s][k]; });
      }
    });
    if (cfgOverrides.social) out.social = clone(cfgOverrides.social);
    if (cfgOverrides.themes) out.themes = clone(cfgOverrides.themes);
    return out;
  }

  $("#btn-dl-config").addEventListener("click", function () {
    var js = "/* site-config.js  —  V1\n" +
             " * Exported from admin/index.html on " + new Date().toISOString().slice(0, 10) + "\n" +
             " * Replaces assets/js/site-config.js\n" +
             " */\n" +
             "window.SITE_CONFIG = " + JSON.stringify(mergedConfig(), null, 2) + ";\n" +
             "window.SITE_CONFIG_META = " + JSON.stringify(META) + ";\n";
    download("site-config.js", js, "application/javascript");
    toast("Downloaded — put it in assets/js/ and commit");
  });

  $("#btn-dl-content").addEventListener("click", function () {
    if (!Object.keys(contentOverrides).length) {
      toast("There are no text or image edits to export yet", true);
      return;
    }
    var js = "/* content-overrides.js  —  V1\n" +
             " * Exported from admin/index.html on " + new Date().toISOString().slice(0, 10) + "\n" +
             " * Load this AFTER assets/js/content.js on every page.\n" +
             " */\n" +
             "(function(){var o=" + JSON.stringify(contentOverrides) + ";\n" +
             "try{var k='" + LS_CONTENT + "';var cur=JSON.parse(localStorage.getItem(k)||'{}');\n" +
             "for(var p in o){if(cur[p]===undefined)cur[p]=o[p];}\n" +
             "localStorage.setItem(k,JSON.stringify(cur));}catch(e){}\n" +
             "window.SITE_CONTENT_OVERRIDES=o;}());\n";
    download("content-overrides.js", js, "application/javascript");
    toast("Downloaded — put it in assets/js/ and commit");
  });

  $("#btn-backup").addEventListener("click", function () {
    var payload = {
      _format: "pillai-and-sons-site-backup",
      _version: 1,
      _date: new Date().toISOString(),
      config: cfgOverrides,
      content: contentOverrides
    };
    download("site-backup-" + new Date().toISOString().slice(0, 10) + ".json",
             JSON.stringify(payload, null, 2), "application/json");
    toast("Backup downloaded");
  });

  $("#btn-restore").addEventListener("click", function () { $("#restore-input").click(); });
  $("#restore-input").addEventListener("change", function (e) {
    var f = e.target.files && e.target.files[0];
    if (!f) return;
    var r = new FileReader();
    r.onload = function () {
      try {
        var data = JSON.parse(r.result);
        if (data._format !== "pillai-and-sons-site-backup") throw new Error("wrong file");
        cfgOverrides = data.config || {};
        contentOverrides = data.content || {};
        rebuildAll();
        markDirty();
        toast("Backup loaded — press Save to keep it");
      } catch (err) {
        toast("That does not look like a backup file", true);
      }
    };
    r.readAsText(f);
    e.target.value = "";
  });

  function resetAndReload(keys, message) {
    if (!window.confirm(message + "\n\nThis cannot be undone.")) return;
    keys.forEach(function (k) {
      try { localStorage.removeItem(k); } catch (e) {}
    });
    if (keys.indexOf(LS_CONFIG) > -1) cfgOverrides = {};
    if (keys.indexOf(LS_CONTENT) > -1) contentOverrides = {};
    rebuildAll();
    markClean();
    updateStorageMeter();
    toast("Reset done");
  }

  $("#btn-reset-content").addEventListener("click", function () {
    resetAndReload([LS_CONTENT], "Remove all text and image edits?");
  });
  $("#btn-reset-config").addEventListener("click", function () {
    resetAndReload([LS_CONFIG], "Remove all colour, font and business-detail edits?");
  });
  $("#btn-reset-all").addEventListener("click", function () {
    resetAndReload([LS_CONFIG, LS_CONTENT, "psm_visitor_theme_v1"],
                   "Remove every edit and put the site back to how it was delivered?");
  });

  function updateStorageMeter() {
    var bytes = 0;
    try {
      bytes = JSON.stringify(cfgOverrides).length + JSON.stringify(contentOverrides).length;
    } catch (e) {}
    var limit = 5 * 1024 * 1024;
    var pct = Math.min(100, Math.round((bytes / limit) * 100));
    var meter = $("#storage-meter");
    if (!meter) return;
    meter.querySelector("span").style.width = pct + "%";
    meter.classList.toggle("is-high", pct > 70);
    var nImg = Object.keys(contentOverrides).filter(function (k) {
      return String(contentOverrides[k]).indexOf("data:image") === 0;
    }).length;
    var kb = bytes / 1024;
    $("#storage-text").textContent =
      (kb < 10 ? kb.toFixed(1) : kb.toFixed(0)) + " KB of about 5,000 KB used · " +
      Object.keys(contentOverrides).length + " content edit" +
      (Object.keys(contentOverrides).length === 1 ? "" : "s") + " · " +
      nImg + " uploaded image" + (nImg === 1 ? "" : "s");
  }

  /* ==================================================================
     XLSX READER  (ZIP + SpreadsheetML, written from scratch)
     ================================================================== */
  function readU16(dv, o) { return dv.getUint16(o, true); }
  function readU32(dv, o) { return dv.getUint32(o, true); }

  function findEOCD(dv) {
    var max = Math.min(dv.byteLength, 66000);
    for (var i = dv.byteLength - 22; i >= dv.byteLength - max && i >= 0; i--) {
      if (readU32(dv, i) === 0x06054b50) return i;
    }
    return -1;
  }

  function zipEntries(buffer) {
    var dv = new DataView(buffer);
    var eocd = findEOCD(dv);
    if (eocd < 0) throw new Error("Not a zip file");
    var count = readU16(dv, eocd + 10);
    var cdOffset = readU32(dv, eocd + 16);
    var entries = {};
    var p = cdOffset;
    var dec = new TextDecoder("utf-8");
    for (var i = 0; i < count; i++) {
      if (readU32(dv, p) !== 0x02014b50) break;
      var method = readU16(dv, p + 10);
      var compSize = readU32(dv, p + 20);
      var nameLen = readU16(dv, p + 28);
      var extraLen = readU16(dv, p + 30);
      var commentLen = readU16(dv, p + 32);
      var localOffset = readU32(dv, p + 42);
      var name = dec.decode(new Uint8Array(buffer, p + 46, nameLen));
      entries[name] = { method: method, compSize: compSize, localOffset: localOffset };
      p += 46 + nameLen + extraLen + commentLen;
    }
    return { dv: dv, buffer: buffer, entries: entries };
  }

  function inflateEntry(zip, name) {
    var e = zip.entries[name];
    if (!e) return Promise.resolve(null);
    var dv = zip.dv;
    var lnameLen = readU16(dv, e.localOffset + 26);
    var lextraLen = readU16(dv, e.localOffset + 28);
    var start = e.localOffset + 30 + lnameLen + lextraLen;
    var slice = zip.buffer.slice(start, start + e.compSize);

    if (e.method === 0) {
      return Promise.resolve(new TextDecoder("utf-8").decode(new Uint8Array(slice)));
    }
    if (typeof DecompressionStream === "undefined") {
      return Promise.reject(new Error("This browser cannot unzip files. " +
        "Use Chrome, Edge or Safari 16.4 and above — or run python3 tools/build_config.py instead."));
    }
    var ds = new DecompressionStream("deflate-raw");
    var stream = new Blob([slice]).stream().pipeThrough(ds);
    return new Response(stream).text();
  }

  function parseXml(text) {
    return new DOMParser().parseFromString(text, "application/xml");
  }

  function colLetters(ref) { return String(ref || "").replace(/[0-9]/g, ""); }

  function sheetRows(doc, shared) {
    var rows = [];
    var rowEls = doc.getElementsByTagName("row");
    for (var i = 0; i < rowEls.length; i++) {
      var cells = rowEls[i].getElementsByTagName("c");
      var row = {};
      for (var j = 0; j < cells.length; j++) {
        var c = cells[j];
        var t = c.getAttribute("t");
        var val = "";
        if (t === "inlineStr") {
          var isEl = c.getElementsByTagName("t");
          val = isEl.length ? isEl[0].textContent : "";
        } else {
          var vEl = c.getElementsByTagName("v");
          val = vEl.length ? vEl[0].textContent : "";
          if (t === "s") val = shared[parseInt(val, 10)] || "";
        }
        row[colLetters(c.getAttribute("r"))] = val;
      }
      rows.push(row);
    }
    return rows;
  }

  function readWorkbook(buffer) {
    var zip = zipEntries(buffer);
    return inflateEntry(zip, "xl/workbook.xml").then(function (wbXml) {
      if (!wbXml) throw new Error("This file is missing xl/workbook.xml — is it really an .xlsx?");
      var wbDoc = parseXml(wbXml);
      return inflateEntry(zip, "xl/_rels/workbook.xml.rels").then(function (relsXml) {
        var relMap = {};
        if (relsXml) {
          var rels = parseXml(relsXml).getElementsByTagName("Relationship");
          for (var i = 0; i < rels.length; i++) {
            relMap[rels[i].getAttribute("Id")] = rels[i].getAttribute("Target").replace(/^\/?xl\//, "");
          }
        }
        var sheets = {};
        var sh = wbDoc.getElementsByTagName("sheet");
        for (var k = 0; k < sh.length; k++) {
          var rid = sh[k].getAttribute("r:id") ||
                    sh[k].getAttributeNS("http://schemas.openxmlformats.org/officeDocument/2006/relationships", "id");
          sheets[sh[k].getAttribute("name")] = relMap[rid] || ("worksheets/sheet" + (k + 1) + ".xml");
        }
        return inflateEntry(zip, "xl/sharedStrings.xml").then(function (ssXml) {
          var shared = [];
          if (ssXml) {
            var siList = parseXml(ssXml).getElementsByTagName("si");
            for (var s = 0; s < siList.length; s++) {
              var tNodes = siList[s].getElementsByTagName("t");
              var txt = "";
              for (var q = 0; q < tNodes.length; q++) txt += tNodes[q].textContent;
              shared.push(txt);
            }
          }
          var names = Object.keys(sheets);
          return Promise.all(names.map(function (n) {
            return inflateEntry(zip, "xl/" + sheets[n]).then(function (xml) {
              return xml ? sheetRows(parseXml(xml), shared) : [];
            });
          })).then(function (all) {
            var out = {};
            names.forEach(function (n, i) { out[n] = all[i]; });
            return out;
          });
        });
      });
    });
  }

  function configFromSheets(sheets) {
    function kv(name) {
      var rows = sheets[name] || [];
      var out = {};
      rows.forEach(function (r, i) {
        var key = (r.A || "").trim();
        if (!key || i === 0 || key.toUpperCase() === "NOTE" || key.toLowerCase() === "setting") return;
        out[key] = (r.B === undefined ? "" : String(r.B)).trim();
      });
      return out;
    }

    var social = [];
    (sheets["Social"] || []).forEach(function (r, i) {
      var p = (r.A || "").trim().toLowerCase();
      if (!p || i === 0 || p === "note" || p === "platform") return;
      var en = String(r.C === undefined ? "yes" : r.C).trim().toLowerCase();
      social.push({ platform: p, url: (r.B || "").trim(),
                    enabled: ["no", "false", "0", "off"].indexOf(en) === -1,
                    label: (r.D || "").trim() || p });
    });

    var themes = [];
    (sheets["Themes"] || []).forEach(function (r, i) {
      var n = (r.A || "").trim();
      if (!n || i === 0 || n.toUpperCase() === "NOTE" || n.toLowerCase() === "theme name") return;
      themes.push({ name: n, primary: (r.B || "").trim(), secondary: (r.C || "").trim(),
                    tertiary: (r.D || "").trim(), accent_cream: (r.E || "").trim(),
                    footer_bg: (r.F || "").trim(), topbar_bg: (r.G || "").trim() });
    });

    return { business: kv("Business"), colors: kv("Colors"), fonts: kv("Fonts"),
             social: social, themes: themes };
  }

  function handleXlsx(file) {
    var report = $("#xlsx-report");
    report.innerHTML = '<div class="a-note a-note--info">Reading ' + escapeHtml(file.name) + '…</div>';

    file.arrayBuffer().then(readWorkbook).then(function (sheets) {
      var parsed = configFromSheets(sheets);
      var missing = ["Business", "Colors", "Fonts"].filter(function (n) { return !sheets[n]; });
      if (missing.length) {
        throw new Error("Missing sheet(s): " + missing.join(", ") +
                        ". Use the workbook from the config folder, or regenerate it with " +
                        "python3 tools/make_config_xlsx.py");
      }

      var diffs = [];
      ["business", "colors", "fonts"].forEach(function (section) {
        Object.keys(parsed[section]).forEach(function (k) {
          var cur = cfgValue(section, k);
          if (String(parsed[section][k]) !== String(cur)) {
            diffs.push({ section: section, key: k, from: cur, to: parsed[section][k] });
          }
        });
      });

      var html = '<div class="a-card"><h3>Read successfully</h3>' +
        '<p style="font-size:14px">' +
        Object.keys(parsed.business).length + " business settings, " +
        Object.keys(parsed.colors).length + " colours, " +
        Object.keys(parsed.fonts).length + " font settings, " +
        parsed.social.length + " social links, " +
        parsed.themes.length + " palettes.</p>";

      if (!diffs.length) {
        html += '<p style="font-size:14px">Everything matches what the site is already using — nothing to change.</p>';
      } else {
        html += '<p style="font-size:14px"><strong>' + diffs.length + ' value(s) differ:</strong></p>' +
          '<table class="a-table"><thead><tr><th>Sheet</th><th>Setting</th><th>Now</th><th>From the file</th></tr></thead><tbody>';
        diffs.slice(0, 60).forEach(function (d) {
          html += "<tr><td>" + d.section + "</td><td><code>" + escapeHtml(d.key) + "</code></td><td>" +
                  escapeHtml(String(d.from).slice(0, 46)) + "</td><td><strong>" +
                  escapeHtml(String(d.to).slice(0, 46)) + "</strong></td></tr>";
        });
        html += "</tbody></table>";
        if (diffs.length > 60) html += '<p style="font-size:13px">…and ' + (diffs.length - 60) + " more.</p>";
      }
      html += '<div class="a-row" style="margin-top:14px">' +
              '<button type="button" class="a-btn" id="btn-apply-xlsx">Apply to site</button></div></div>';
      report.innerHTML = html;

      var applyBtn = $("#btn-apply-xlsx");
      if (applyBtn) {
        applyBtn.addEventListener("click", function () {
          ["business", "colors", "fonts"].forEach(function (section) {
            Object.keys(parsed[section]).forEach(function (k) {
              setCfg(section, k, parsed[section][k]);
            });
          });
          if (parsed.social.length) { cfgOverrides.social = parsed.social; }
          if (parsed.themes.length) { cfgOverrides.themes = parsed.themes; }
          markDirty();
          rebuildAll();
          save();
          toast("Spreadsheet applied and saved");
        });
      }
    }).catch(function (err) {
      report.innerHTML = '<div class="a-note a-note--warn"><strong>Could not read that file.</strong><br>' +
                         escapeHtml(err.message || String(err)) + "</div>";
    });
  }

  var drop = $("#xlsx-drop");
  var xlsxInput = $("#xlsx-input");
  if (drop) {
    drop.addEventListener("click", function () { xlsxInput.click(); });
    drop.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); xlsxInput.click(); }
    });
    ["dragenter", "dragover"].forEach(function (ev) {
      drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add("is-over"); });
    });
    ["dragleave", "drop"].forEach(function (ev) {
      drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.remove("is-over"); });
    });
    drop.addEventListener("drop", function (e) {
      var f = e.dataTransfer.files && e.dataTransfer.files[0];
      if (f) handleXlsx(f);
    });
    xlsxInput.addEventListener("change", function () {
      if (xlsxInput.files[0]) handleXlsx(xlsxInput.files[0]);
      xlsxInput.value = "";
    });
  }

  /* ==================================================================
     BOOT
     ================================================================== */
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function rebuildAll() {
    buildConfigForm("business", "#form-business");
    buildConfigForm("colors", "#form-colours");
    buildConfigForm("fonts", "#form-fonts");
    buildPalettes();
    buildSocialForm();
    buildContentForms();
  }

  rebuildAll();
  wireSearch("#content-search", "#form-content");
  wireSearch("#image-search", "#form-images");
  updateStorageMeter();
  markClean();

  var brand = cfgValue("business", "business_name");
  if (brand) $("#brand-name").textContent = brand + " — Editor";

  document.addEventListener("keydown", function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") { e.preventDefault(); save(); }
  });
}());
