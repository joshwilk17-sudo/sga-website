/* Silly Goose Audio — Payhip product page reskin.
   Loaded on every page via Header Code Injection. Does nothing unless the page is a Payhip product page.
   It only ADDS elements and moves the read-only parts (screenshots, description, file list) further down;
   Payhip's price box, Add to Cart, Buy Now and wishlist stay exactly where Payhip put them. */
(function () {
  var D = window.SGA_DATA;
  if (!D) return;

  function el(html) { var t = document.createElement("div"); t.innerHTML = html.trim(); return t.firstChild; }

  function run() {
    var sec = document.getElementById("page-section-product");
    var body = document.body;
    if (!sec || body.classList.contains("sga-pp")) return;

    /* product key: Payhip puts it on the buy buttons (works with custom URL slugs like /b/angry-goose); URL is the fallback */
    var keyEl = sec.querySelector("[data-product]") || sec.querySelector("[data-product-key]");
    var m = location.pathname.match(/\/b\/([A-Za-z0-9]+)/);
    var id = (keyEl && (keyEl.getAttribute("data-product") || keyEl.getAttribute("data-product-key"))) || (m && m[1]);
    var p = id && D.products[id];

    body.classList.add("sga-pp");
    if (!document.querySelector('link[data-sga-fonts]')) {
      var f = document.createElement("link");
      f.rel = "stylesheet"; f.href = D.fonts; f.setAttribute("data-sga-fonts", "");
      document.head.appendChild(f);
    }

    /* slogan strip under Payhip's header */
    var header = document.getElementById("header");
    if (header) header.insertAdjacentElement("afterend", el(D.strip));

    var outer = sec.querySelector(".media-and-details-wrapper-outer");
    var col = sec.querySelector(".product-details-wrapper .col-md-12") || sec.querySelector(".product-details-wrapper");
    var media = sec.querySelector(".media-wrapper-outer");
    var h1 = sec.querySelector("h1.font-section-product-name");
    var contents = sec.querySelector(".section-contents") || outer && outer.parentNode;

    /* hero: box art left, title + specs right */
    if (p && outer) {
      body.classList.add("sga-pp--box");
      outer.insertBefore(el('<div class="sga-pp-box"><img class="sga-honk" src="' + D.assets + "images/box/" + p.box + '.webp" alt="' + p.name + ' box art" width="720" height="720"></div>'), outer.firstChild);
    }
    if (p && h1) {
      var kind = p.kind === "sister" ? "Free sister plugin" : "Silly Goose original";
      var price = p.price === 0 ? '<span class="sga-chip">Free</span>' : '<span class="sga-chip sga-chip--solid">$' + p.price + "</span>";
      var isNew = p["new"] ? '<span class="sga-chip">New</span>' : "";
      h1.insertAdjacentElement("beforebegin", el('<div class="sga-pp-eyebrow"><span class="sga-eyebrow">' + kind + "</span>" + price + isNew + "</div>"));
      var after = '<div class="sga-pp-after"><p class="sga-pp-sub">' + p.sub + "</p>" +
        (p.blurb ? '<p class="sga-pp-blurb">' + p.blurb + "</p>" : "") +
        '<div class="sga-pp-chips"><span class="sga-chip">VST3</span><span class="sga-chip">AU</span><span class="sga-chip">Standalone</span><span class="sga-chip sga-chip--dim">macOS</span><span class="sga-chip sga-chip--dim">Windows</span></div></div>';
      h1.insertAdjacentElement("afterend", el(after));
    }

    /* reassurance lines under the buttons */
    if (p && col) {
      var anchor = col.querySelector(".preview-link-and-wishlist-link-wrapper") || col.querySelector(".payhip-buy-button") || col.querySelector(".btn-primary");
      var lines = ["Instant download after checkout", "Mac (Apple Silicon + Intel) and Windows", p.price === 0 ? "Free. No payment needed" : "License key included with your receipt"];
      if (anchor) anchor.insertAdjacentElement("afterend", el('<div class="sga-pp-trust"><div>' + lines.join("</div><div>") + "</div></div>"));
    }

    /* below the fold: screenshots, description, file list, share */
    if (p && contents) {
      var more = el('<div class="sga-pp-more"></div>');
      if (media) {
        more.appendChild(el('<div><div class="sga-pp-kicker">Inside the box</div><h2 class="sga-pp-h2">Meet <em>' + p.name + "</em></h2></div>"));
        more.appendChild(media);
      }
      ["product-description", "product-meta-wrapper", "social-media-buttons-wrapper"].forEach(function (c) {
        var n = sec.querySelector("." + c);
        if (n) more.appendChild(n);
      });
      contents.appendChild(more);
    }

    /* "More from the flock" replaces "You might also like" */
    if (p) {
      var same = [], other = [];
      Object.keys(D.cards).forEach(function (k) {
        if (k === id) return;
        (D.products[k].kind === p.kind ? same : other).push(k);
      });
      var shuffle = function (a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; };
      var pick = shuffle(same).concat(shuffle(other)).slice(0, 4);
      var rel = el('<div class="sga sga-pp-related"><section class="sga-section"><div class="sga-wrap">' +
        '<div class="sga-head"><div><span class="sga-eyebrow">Keep shopping</span><h2 class="sga-h2">More from <em>the flock</em></h2></div>' +
        '<a class="sga-btn sga-btn--ghost sga-btn--sm" href="' + D.shop + '#all">Browse all →</a></div>' +
        '<div class="sga-grid">' + pick.map(function (k) { return D.cards[k]; }).join("") + "</div></div></section></div>");
      var relSec = document.getElementById("page-section-related-products");
      var reviews = document.getElementById("page-section-customer-reviews");
      var spot = relSec || reviews || sec;
      spot.insertAdjacentElement("afterend", rel);
      body.classList.add("sga-pp--related");
    }

    /* footer band */
    var main = document.querySelector(".content-main-wrapper") || sec.parentNode;
    main.appendChild(el(D.foot));
  }

  /* the honk Easter egg (box art, slogan geese, footer goose) */
  document.addEventListener("click", function (e) {
    var t = e.target.closest && e.target.closest(".sga-pp .sga-honk");
    if (!t) return;
    var a = new Audio(D.assets + "audio/honk" + (1 + Math.floor(Math.random() * 7)) + ".m4a");
    a.volume = 0.7; a.play().catch(function () {});
  });

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();
})();
