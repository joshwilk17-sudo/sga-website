/* Silly Goose Audio — custom page behaviour. Safe to include on every page (each part no-ops if its markup is missing). */
(function () {
  var root = document.querySelector(".sga");
  if (!root) return;
  root.classList.add("sga-js");
  var assets = root.getAttribute("data-assets") || "";

  /* Easter egg: anything with .sga-honk plays one of the 7 house honks (same samples as the plugins). */
  var honks = [], words = ["HONK!", "HONK!!", "HJONK", "*hiss*", "HONK?", "HONNNK", "SKRONK"];
  for (var i = 1; i <= 7; i++) honks.push(assets + "audio/honk" + i + ".m4a");
  root.addEventListener("click", function (e) {
    var t = e.target.closest(".sga-honk");
    if (!t) return;
    var a = new Audio(honks[Math.floor(Math.random() * honks.length)]);
    a.volume = 0.7; a.play().catch(function () {});
    var pop = document.createElement("div");
    pop.className = "sga-honkpop";
    pop.textContent = words[Math.floor(Math.random() * words.length)];
    pop.style.left = e.clientX + "px"; pop.style.top = (e.clientY - 20) + "px";
    document.body.appendChild(pop);
    setTimeout(function () { pop.remove(); }, 950);
  });

  /* Shop tabs, deep-linkable: #originals, #sister, #all */
  var tabs = root.querySelectorAll(".sga-tab");
  if (tabs.length) {
    var show = function (id, push) {
      var found = false;
      tabs.forEach(function (t) {
        var on = t.getAttribute("data-tab") === id;
        found = found || on;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
      });
      if (!found) return show("all", push);
      root.querySelectorAll(".sga-panel").forEach(function (p) { p.hidden = p.id !== "panel-" + id; });
      if (push && history.replaceState) history.replaceState(null, "", "#" + id);
    };
    tabs.forEach(function (t) {
      t.addEventListener("click", function () { show(t.getAttribute("data-tab"), true); });
      t.addEventListener("keydown", function (e) {
        if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
        var list = Array.prototype.slice.call(tabs), i = list.indexOf(t);
        var next = list[(i + (e.key === "ArrowRight" ? 1 : list.length - 1)) % list.length];
        next.focus(); next.click();
      });
    });
    var fromHash = function () { show((location.hash || "#all").slice(1), false); };
    window.addEventListener("hashchange", fromHash);
    fromHash();
  }

  /* FAQ search */
  var search = root.querySelector(".sga-search");
  if (search) {
    var qs = root.querySelectorAll(".sga-q"), empty = root.querySelector(".sga-empty");
    search.addEventListener("input", function () {
      var term = search.value.trim().toLowerCase(), any = false;
      qs.forEach(function (q) {
        var hit = !term || q.textContent.toLowerCase().indexOf(term) !== -1;
        q.style.display = hit ? "" : "none";
        if (term && hit) q.open = true;
        any = any || hit;
      });
      root.querySelectorAll(".sga-faq__group").forEach(function (g) {
        g.style.display = g.querySelector('.sga-q:not([style*="none"])') ? "" : "none";
      });
      if (empty) empty.style.display = any ? "none" : "block";
    });
  }

  /* Contact form: composes an email in the visitor's mail app (no server needed). */
  var form = root.querySelector(".sga-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var f = form.elements;
      var subject = "[" + f.topic.value + "] " + (f.plugin.value ? f.plugin.value + " — " : "") + "from " + f.name.value;
      var body = f.message.value + "\n\n— " + f.name.value + " (" + f.email.value + ")";
      location.href = "mailto:" + form.getAttribute("data-to") + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    });
  }

  /* Photo lightbox (Re-Feedback Hardware gallery). Without JS each photo just opens on its own. */
  var shots = root.querySelectorAll(".sga-gallery a.sga-shot"), box = root.querySelector(".sga-lightbox");
  if (shots.length && box) {
    var bImg = box.querySelector("img"), bCap = box.querySelector("figcaption"), cur = 0;
    var showShot = function (i) {
      cur = (i + shots.length) % shots.length;
      bImg.src = shots[cur].getAttribute("href");
      bImg.alt = bCap.textContent = shots[cur].getAttribute("data-caption") || "";
    };
    var closeBox = function () { box.hidden = true; document.documentElement.style.overflow = ""; };
    shots.forEach(function (a, i) {
      a.addEventListener("click", function (e) { e.preventDefault(); showShot(i); box.hidden = false; document.documentElement.style.overflow = "hidden"; });
    });
    box.querySelector(".sga-lightbox__prev").addEventListener("click", function () { showShot(cur - 1); });
    box.querySelector(".sga-lightbox__next").addEventListener("click", function () { showShot(cur + 1); });
    box.querySelector(".sga-lightbox__close").addEventListener("click", closeBox);
    box.addEventListener("click", function (e) { if (e.target === box) closeBox(); });
    document.addEventListener("keydown", function (e) {
      if (box.hidden) return;
      if (e.key === "Escape") closeBox();
      if (e.key === "ArrowRight") showShot(cur + 1);
      if (e.key === "ArrowLeft") showShot(cur - 1);
    });
  }

  /* Scroll-in reveal */
  var rev = root.querySelectorAll(".sga-reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    rev.forEach(function (el) { io.observe(el); });
  } else rev.forEach(function (el) { el.classList.add("is-in"); });
})();
