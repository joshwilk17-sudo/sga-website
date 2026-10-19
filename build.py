#!/usr/bin/env python3
"""Builds the Silly Goose Audio custom pages.

    python3 build.py

Outputs:
  dist/payhip/<page>.html   one self-contained block per page -> paste into a Payhip "Embed Code" section
  dist/preview/<page>.html  full local preview wrapped in a mock of the Payhip header/footer

Products live in PRODUCTS below; settings (asset URL, page links, email) live in config.json.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
CFG = json.loads((ROOT / "config.json").read_text())

# ---------------------------------------------------------------------------------------------
# Catalogue. kind: "original" (paid / house plugins) or "sister" (free parodies).
# box = file in images/box/<box>.webp. id = Payhip product code (payhip.com/b/<id>); None = not listed yet.
# ---------------------------------------------------------------------------------------------
PRODUCTS = [
    # originals
    dict(name="Goose Kicker", ver="V1", id="EwJ4L", price=10, kind="original", box="goose-kicker", new=True,
         sub="Kick generator + Kicker FX",
         blurb="Design 808, 909, hardstyle and rawstyle kicks from scratch, crush them, drag them straight into your DAW."),
    dict(name="Angry Goose", ver="V1", id="jBLYu", price=5, kind="original", box="angry-goose",
         sub="Sample-synthesized distortion & compressor",
         blurb="Seven goose distortion models. Never mess with a mama goose."),
    dict(name="Goose Thumper", ver="V1", id="jY2Fs", price=5, kind="original", box="goose-thumper",
         sub="Drum sampler & step sequencer",
         blurb="Drop in a loop. It finds every hit, chops it onto 16 pads and sorts kicks, snares and hats."),
    dict(name="Goose Delay", ver="V1", id="ongP1", price=5, kind="original", box="goose-delay",
         sub="Paradox feedback delay engine",
         blurb="A delay flying around like a flock of drunk geese. Careful with that feedback knob."),
    dict(name="Goose Re-esser", ver="V1", id="HQinh", price=5, kind="original", box="goose-re-esser",
         sub="Reverse de-esser & sibilance exciter",
         blurb="Finds the sibilance and boosts it. Puts the SSSSS back."),
    dict(name="Bit-Gooser", ver="V1", id="0FnHN", price=0, kind="original", box="bit-gooser",
         sub="Bitcrusher & downsampler",
         blurb="Lower the bits. Crush the goose. The GUI pixelates as you go."),
    dict(name="Goose EQ", ver="V1", id="mCvcM", price=0, kind="original", box="goose-eq",
         sub="Studio-grade parametric equalizer",
         blurb="10-band parametric EQ with HP/LP filters and the special Goose Twin Node."),
    dict(name="Goose Gate", ver="V1", id="mE5f9", price=0, kind="original", box="goose-gate",
         sub="Malfunctioning noise gate",
         blurb="Designed by a goose, who can't open or close a gate. Squeaky hinge included."),
    # sister plugins (free parodies)
    dict(name="Goose Bus Crusher", ver="V1", id="thJX5", price=0, kind="sister", box="goose-bus-crusher",
         sub="All-buttons-in FET limiter",
         blurb="A FET limiter that only knows one setting: every button in."),
    dict(name="Agitate3", ver="", id="EzB3J", price=0, kind="sister", box="agitate3",
         sub="Resonance amplifier",
         blurb="Finds what's harsh. Makes it worse."),
    dict(name="Auto-Detune", ver="V1", id="ZQfJ3", price=0, kind="sister", box="auto-detune",
         sub="Dissonance & anti-scale processor",
         blurb="Forces vocals out of tune and out of key. Guaranteed off-key."),
    dict(name="Goose S1 Stereo Collapser", ver="", id="CU3Km", price=0, kind="sister", box="goose-s1-stereo-collapser",
         sub="Precision stereo width collapser",
         blurb="Every widener promises bigger. This one does the opposite, with surgical precision."),
    dict(name="Re-Feedback", ver="V1", id="fpqKD", price=0, kind="sister", box="re-feedback",
         sub="Acoustic feedback simulator",
         blurb="Puts the feedback back. Mic too close to the amp, on purpose."),
    dict(name="OneKnob Thinner", ver="", id="GQgXz", price=0, kind="sister", box="oneknob-thinner",
         sub="Dynamic progressive audio thinner",
         blurb="Make your audio thinner with one beautiful knob. One knob, zero body."),
    dict(name="OneKnob Quieter", ver="", id="izwmW", price=0, kind="sister", box="oneknob-quieter",
         sub="Dynamic audio attenuator",
         blurb="Make your audio quieter with one beautiful knob. It's a volume knob."),
    # box art exists, not on Payhip yet
    dict(name="Goose Confusion", ver="VX", id=None, price=None, kind="soon", box="goose-confusion",
         sub="Vocal incomprehensibility engine", blurb=""),
    dict(name="Goose Shaper", ver="V1", id=None, price=None, kind="soon", box="goose-shaper",
         sub="Multiband volume shaper", blurb=""),
    dict(name="Goose RX Re-Hum", ver="", id=None, price=None, kind="soon", box="goose-rx-re-hum",
         sub="Mains hum generator", blurb=""),
]

LIVE = [p for p in PRODUCTS if p["id"]]
ORIGINALS = [p for p in LIVE if p["kind"] == "original"]
SISTERS = [p for p in LIVE if p["kind"] == "sister"]
SOON = [p for p in PRODUCTS if p["kind"] == "soon"]
FREE_COUNT = sum(1 for p in LIVE if p["price"] == 0)
by_box = {p["box"]: p for p in PRODUCTS}

e = html.escape


def url(p):
    return f"{CFG['site']}/b/{p['id']}"


def img(box, assets):
    return f"{assets}images/box/{box}.webp"


def price_chip(p):
    if p["price"] is None:
        return '<span class="sga-chip sga-chip--dim">Hatching soon</span>'
    if p["price"] == 0:
        return '<span class="sga-chip">Free</span>'
    return f'<span class="sga-chip sga-chip--solid">${p["price"]}</span>'


def card(p, assets):
    ver = f' <small>{e(p["ver"])}</small>' if p["ver"] else ""
    if not p["id"]:
        return f'''<div class="sga-card sga-card--soon" aria-label="{e(p["name"])} — hatching soon">
  <div class="sga-card__art"><img src="{img(p["box"], assets)}" alt="" loading="lazy" width="720" height="720"><span class="sga-card__price">{price_chip(p)}</span></div>
  <div class="sga-card__body"><h3 class="sga-card__name">{e(p["name"])}{ver}</h3><p class="sga-card__sub">{e(p["sub"])}</p>
  <div class="sga-card__foot"><span class="sga-card__cta" style="color:var(--mute)">Still in the egg</span></div></div>
</div>'''
    cta = "Get it free" if p["price"] == 0 else "View plugin"
    tag = '<span class="sga-chip sga-chip--dim">Free parody</span>' if p["kind"] == "sister" else '<span class="sga-chip sga-chip--dim">Original</span>'
    if p.get("new"):
        tag = '<span class="sga-chip">New</span>'
    return f'''<a class="sga-card" href="{url(p)}">
  <div class="sga-card__art"><img src="{img(p["box"], assets)}" alt="{e(p["name"])} box art" loading="lazy" width="720" height="720"><span class="sga-card__price">{price_chip(p)}</span></div>
  <div class="sga-card__body"><h3 class="sga-card__name">{e(p["name"])}{ver}</h3><p class="sga-card__sub">{e(p["sub"])}</p>
  <div class="sga-card__foot"><span class="sga-card__cta">{cta}</span>{tag}</div></div>
</a>'''


ICON = {
    "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 22v-8h2.7l.4-3.2h-3.1V8.8c0-.9.3-1.5 1.6-1.5h1.7V4.4a22 22 0 0 0-2.5-.1c-2.5 0-4.2 1.5-4.2 4.3v2.3H7.4V14h2.7v8z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    "key": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="8" cy="15" r="4"/><path d="m11 12 9-9m-4 4 3 3m-5-1 2 2"/></svg>',
}


def socials():
    return f'''<div class="sga-socials">
  <a href="{CFG["instagram"]}" aria-label="Silly Goose Audio on Instagram" target="_blank" rel="noopener">{ICON["ig"]}</a>
  <a href="{CFG["facebook"]}" aria-label="Silly Goose Audio on Facebook" target="_blank" rel="noopener">{ICON["fb"]}</a>
</div>'''


# ------------------------------------------------------------------------------------- pages
def page_home(a):
    pg = CFG["pages"]
    kick = by_box["goose-kicker"]
    names = " ".join(f"<span>{e(p['name'].upper())}</span>" for p in LIVE)
    wall = "\n".join(
        f'<a href="{url(p)}" aria-label="{e(p["name"])}"><img src="{img(p["box"], a)}" alt="{e(p["name"])} box art" loading="lazy" width="720" height="720"><span class="sga-wall__tag">{price_chip(p)}</span></a>'
        for p in LIVE
    ) + "\n" + "\n".join(
        f'<a class="sga-wall__soon" aria-label="{e(p["name"])} (hatching soon)"><img src="{img(p["box"], a)}" alt="" loading="lazy" width="720" height="720"><span class="sga-wall__tag">{price_chip(p)}</span></a>'
        for p in SOON
    )
    return f'''
<section class="sga-hero">
  <div class="sga-wrap sga-hero__grid">
    <div>
      <span class="sga-eyebrow">Audio plug-ins · VST3 · AU · Standalone</span>
      <h1 class="sga-display" style="margin-top:18px">Serious plugins<br>for unserious<br>geese.</h1>
      <p class="sga-lede">Real DSP, built by a goose who takes it a little too seriously. <strong>{len(LIVE)} plugins in the flock, {FREE_COUNT} of them free.</strong></p>
      <div class="sga-btns">
        <a class="sga-btn sga-btn--amber" href="{pg["shop"]}#all">Shop the flock</a>
        <a class="sga-btn sga-btn--ghost" href="{pg["shop"]}#sister">Free sister plugins</a>
      </div>
      <div class="sga-specs"><span class="sga-chip">macOS</span><span class="sga-chip">Windows</span><span class="sga-chip">VST3</span><span class="sga-chip">AU</span><span class="sga-chip">Standalone</span></div>
    </div>
    <a class="sga-stack" href="{url(kick)}" aria-label="Goose Kicker V1">
      <img src="{img("angry-goose", a)}" alt="" width="720" height="720">
      <img src="{img("goose-thumper", a)}" alt="" width="720" height="720">
      <img src="{img("goose-kicker", a)}" alt="Goose Kicker V1 box art" width="720" height="720">
      <span class="sga-stack__floor"></span>
    </a>
  </div>
</section>

<div class="sga-ticker" aria-hidden="true"><div class="sga-ticker__track">{names} {names}</div></div>

<section class="sga-section">
  <div class="sga-wrap">
    <div class="sga-head sga-reveal">
      <div><span class="sga-eyebrow">The flock</span><h2 class="sga-h2">Every box on <em>the shelf</em></h2></div>
      <a class="sga-btn sga-btn--ghost sga-btn--sm" href="{pg["shop"]}#all">Browse all {len(LIVE)} →</a>
    </div>
    <div class="sga-wall sga-reveal">{wall}</div>
  </div>
</section>

<section class="sga-section">
  <div class="sga-wrap">
    <div class="sga-spot sga-reveal">
      <a class="sga-spot__art" href="{url(kick)}"><img src="{img("goose-kicker", a)}" alt="Goose Kicker V1 box art" loading="lazy" width="720" height="720"></a>
      <div>
        <span class="sga-chip">Fresh out of the egg</span>
        <h2 class="sga-h2">Goose Kicker <em>V1</em></h2>
        <p class="sga-lede">{e(kick["blurb"])}</p>
        <ul class="sga-bullets">
          <li>Synthesise kicks from scratch: 808, 909, hardstyle, rawstyle</li>
          <li>Built-in Goose Bus Crusher for when it isn't loud enough yet</li>
          <li>Drag the finished kick straight into your DAW</li>
          <li><span><strong style="color:var(--text)">Goose Kicker FX</strong> included, for the kicks you already have. One key unlocks both.</span></li>
        </ul>
        <div class="sga-btns" style="align-items:center">
          <span class="sga-price">${kick["price"]}<small>USD</small></span>
          <a class="sga-btn sga-btn--amber" href="{url(kick)}">Get Goose Kicker</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sga-section">
  <div class="sga-wrap">
    <div class="sga-head sga-reveal"><div><span class="sga-eyebrow">Pick your pond</span><h2 class="sga-h2">Two kinds <em>of goose</em></h2></div></div>
    <div class="sga-duo sga-reveal">
      <a class="sga-cat" href="{pg["shop"]}#originals">
        <div class="sga-cat__boxes"><img src="{img("angry-goose", a)}" alt="" loading="lazy"><img src="{img("goose-delay", a)}" alt="" loading="lazy"><img src="{img("goose-eq", a)}" alt="" loading="lazy"></div>
        <span class="sga-eyebrow">{len(ORIGINALS)} plugins</span>
        <h3>Silly Goose<br>Originals</h3>
        <p>Our own house-built instruments and effects. Some paid, some free, all goose.</p>
        <span class="sga-btn sga-btn--amber sga-btn--sm" style="align-self:flex-start">Shop originals</span>
      </a>
      <a class="sga-cat" href="{pg["shop"]}#sister">
        <div class="sga-cat__boxes"><img src="{img("agitate3", a)}" alt="" loading="lazy"><img src="{img("auto-detune", a)}" alt="" loading="lazy"><img src="{img("goose-bus-crusher", a)}" alt="" loading="lazy"></div>
        <span class="sga-eyebrow">{len(SISTERS)} plugins · all free</span>
        <h3>Sister<br>Plugins</h3>
        <p>Parodies of famous plugins that do the exact opposite of what they should. Always free.</p>
        <span class="sga-btn sga-btn--ghost sga-btn--sm" style="align-self:flex-start">Grab them free</span>
      </a>
    </div>
  </div>
</section>

<section class="sga-section">
  <div class="sga-wrap">
    <div class="sga-feats sga-reveal">
      <div class="sga-feat"><div class="sga-feat__k">2 platforms</div><h4>Mac + Windows</h4><p>VST3, AU and Standalone. Works in Ableton, Logic, FL Studio, Reaper, Studio One, Bitwig and friends.</p></div>
      <div class="sga-feat"><div class="sga-feat__k">1 click</div><h4>Installer included</h4><p>Unzip, run the installer, rescan your plugins. Instructions in every download.</p></div>
      <div class="sga-feat"><div class="sga-feat__k">{FREE_COUNT} free</div><h4>Free means free</h4><p>No card, no catch. Tip the goose if it made you laugh.</p></div>
    </div>
  </div>
</section>

<section class="sga-section">
  <div class="sga-wrap">
    <div class="sga-cta sga-reveal">
      <h2 class="sga-h2">Join <em>the flock</em></h2>
      <p class="sga-lede">New plugins hatch all the time. Follow along for releases, betas and the occasional honk.</p>
      {socials()}
      <p class="sga-note" style="margin-top:24px">psst… every plugin hides a goose. So does this page.</p>
    </div>
  </div>
</section>
'''


def page_shop(a):
    def panel(pid, title, desc, items, extra=""):
        return f'''<div class="sga-panel" id="panel-{pid}" role="tabpanel" aria-labelledby="tab-{pid}">
  <div class="sga-panel__intro"><h2>{title}</h2><p>{desc}</p></div>
  <div class="sga-grid">{"".join(card(p, a) for p in items)}</div>{extra}
</div>'''

    soon = f'<h3 class="sga-subhead">Hatching soon</h3><div class="sga-grid">{"".join(card(p, a) for p in SOON)}</div>' if SOON else ""
    tabs = [("originals", "Original Plugins", len(ORIGINALS)), ("sister", "Sister Plugins", len(SISTERS)), ("all", "All Plugins", len(LIVE))]
    tab_html = "".join(
        f'<button class="sga-tab" role="tab" id="tab-{t}" data-tab="{t}" aria-controls="panel-{t}" aria-selected="{"true" if t == "all" else "false"}">{label} <b>{n}</b></button>'
        for t, label, n in tabs
    )
    return f'''
<header class="sga-pagehead">
  <div class="sga-wrap">
    <span class="sga-eyebrow">The shop</span>
    <h1 class="sga-display">The Pond<br>Shop</h1>
    <p class="sga-lede">Every Silly Goose plugin in one place. Pick a box, check out through Payhip, and you'll get your download straight away.</p>
    <div class="sga-tabs" role="tablist" aria-label="Plugin categories">{tab_html}</div>
  </div>
</header>
<section class="sga-section">
  <div class="sga-wrap">
    {panel("originals", "Original Plugins", "Our own house-built instruments and effects. Serious DSP, unserious names.", ORIGINALS)}
    {panel("sister", "Sister Plugins", "Parodies of plugins you already know, built to do the exact opposite. Every one of them is free.", SISTERS)}
    {panel("all", "All Plugins", f"The whole flock: {len(LIVE)} plugins, {FREE_COUNT} of them free.", LIVE, soon)}
  </div>
</section>
'''


def faq_data():
    return [
    ("Buying & downloads", "buying", [
        ("Are the free plugins really free?",
         "<p>Yes. Every Sister Plugin, plus Bit-Gooser, Goose EQ and Goose Gate, is free. Check out as normal, no payment needed. If a plugin shows a name-your-price box, leave it at <code>$0</code>, or tip the goose if it made you laugh.</p>"),
        ("Where's my download?",
         f"<p>Right after checkout Payhip shows a download button and emails you a receipt with the same link. Lost it? <a href=\"{CFG['login_url']}\">Log in to your Payhip account</a> with the email you bought with, and every purchase is there to re-download.</p>"),
        ("Can I get a refund?",
         f"<p>Because these are instant digital downloads, sales are generally final. But if a plugin won't run on your system and we can't fix it, <a href=\"{CFG['pages']['contact']}\">get in touch</a> and we'll make it right.</p>"),
        ("What payment methods do you take?",
         "<p>Checkout runs through Payhip, which accepts major cards and PayPal. We never see your card details.</p>"),
    ]),
    ("Installing", "installing", [
        ("How do I install a plugin on a Mac?",
         "<ol><li>Unzip the download.</li><li>Open <code>Read Me First.txt</code>.</li><li>Right-click <code>Install &lt;Plugin&gt;.command</code> and choose <strong>Open</strong>.</li><li>Restart your DAW and rescan plugins.</li></ol><p>The installer copies the AU, VST3 and Standalone app into the right folders for you.</p>"),
        ("How do I install a plugin on Windows?",
         "<ol><li>Download the Windows version from the plugin's page and unzip it.</li><li>Run the installer <code>.exe</code> inside.</li><li>Restart your DAW and rescan plugins.</li></ol>"),
        ("Windows says “Windows protected your PC”. What now?",
         "<p>That's SmartScreen being cautious about indie software. Click <strong>More info</strong>, then <strong>Run anyway</strong>.</p>"),
        ("macOS says the installer “can’t be opened”. What now?",
         "<p>That's Gatekeeper being cautious about indie software. Right-click (or Control-click) the installer and choose <strong>Open</strong>, then <strong>Open</strong> again. If that's not offered, go to <strong>System Settings → Privacy &amp; Security</strong> and click <strong>Open Anyway</strong>.</p>"),
        ("Which format should I use?",
         "<p><strong>Logic Pro / GarageBand (Mac):</strong> AU. <strong>Ableton, FL Studio, Reaper, Studio One, Bitwig, Cubase (Mac or Windows):</strong> VST3. AU is Mac-only, so on Windows use VST3. <strong>No DAW?</strong> Open the Standalone app and play.</p>"),
        ("My DAW doesn't show the plugin.",
         "<p>Rescan your plugins (in Ableton, hold Option while clicking Rescan). In Logic, open the Plug-in Manager and reset/rescan the plugin. Still missing? <a href=\"" + CFG["pages"]["contact"] + "\">Send us a honk</a> with your DAW and your Mac or Windows version.</p>"),
        ("Do you support Windows?",
         "<p>Yes. Every plugin comes in a Mac version (Apple Silicon and Intel) and a Windows version. Grab whichever matches your computer from the plugin's Payhip page.</p>"),
    ]),
    ("Licenses & keys", "licensing", [
        ("How do I activate a paid plugin?",
         "<p>Your license key is shown after checkout and in your receipt email. Open the plugin, paste the key into the activation screen, and you're done.</p>"),
        ("Does Goose Kicker include Goose Kicker FX?",
         "<p>Yes. They're one product with one installer, and one key unlocks both the Goose Kicker instrument and the Goose Kicker FX effect.</p>"),
        ("Can I use it on more than one computer?",
         f"<p>Using it on your own machines is fine. Lost your key or moving computers? <a href=\"{CFG['login_url']}\">Your Payhip account</a> keeps a copy, or <a href=\"{CFG['pages']['contact']}\">contact us</a>.</p>"),
    ]),
    ("The plugins", "plugins", [
        ("Are these plugins a joke?",
         "<p>The names are. The audio isn't. Every plugin is real, working DSP you can use on actual records. Some of them just do the opposite of what you'd expect.</p>"),
        ("What's a Sister Plugin?",
         "<p>A free parody of a famous plugin that does the exact opposite of the original: a de-esser that adds sibilance, a stereo imager that collapses width, an Auto-Tune that detunes. Great for sound design, terrible for your reputation.</p>"),
        ("Can I request a plugin?",
         f"<p>Please do. We keep a long list of plugins to parody and we love new ideas. <a href=\"{CFG['pages']['contact']}\">Pitch us yours.</a></p>"),
    ]),
]


def page_faq(a):
    nav = "".join(f'<a href="#faq-{gid}">{e(title)}</a>' for title, gid, _ in faq_data())
    groups = "".join(
        f'<div class="sga-faq__group" id="faq-{gid}"><h2>{e(title)}</h2>'
        + "".join(f'<details class="sga-q"><summary>{e(q)}</summary><div class="sga-q__a">{ans}</div></details>' for q, ans in qs)
        + "</div>"
        for title, gid, qs in faq_data()
    )
    return f'''
<header class="sga-pagehead">
  <div class="sga-wrap">
    <span class="sga-eyebrow">Help</span>
    <h1 class="sga-display">Frequently<br>Honked Questions</h1>
    <p class="sga-lede">Installing, downloading, licenses and the occasional goose. Can't find it here? <a class="sga-link" href="{CFG["pages"]["contact"]}">Ask us directly.</a></p>
  </div>
</header>
<section class="sga-section">
  <div class="sga-wrap sga-faq">
    <nav class="sga-faq__nav" aria-label="FAQ sections">{nav}</nav>
    <div>
      <input class="sga-search" type="search" placeholder="Search the questions…" aria-label="Search the FAQ">
      {groups}
      <p class="sga-empty">No honks found. Try another word, or <a class="sga-link" href="{CFG["pages"]["contact"]}">ask us</a>.</p>
    </div>
  </div>
</section>
'''


def page_contact(a):
    opts = "".join(f"<option>{e(p['name'])}</option>" for p in LIVE)
    return f'''
<header class="sga-pagehead">
  <div class="sga-wrap">
    <span class="sga-eyebrow">Contact</span>
    <h1 class="sga-display">Honk<br>at us</h1>
    <p class="sga-lede">Bug, install trouble, license question or a plugin idea that's too silly to exist? We read everything.</p>
  </div>
</header>
<section class="sga-section">
  <div class="sga-wrap sga-contact">
    <form class="sga-form" data-to="{e(CFG["email"])}">
      <h2>Send a message</h2>
      <div class="sga-row2">
        <div class="sga-field"><label for="sga-name">Your name</label><input id="sga-name" name="name" required autocomplete="name"></div>
        <div class="sga-field"><label for="sga-email">Your email</label><input id="sga-email" name="email" type="email" required autocomplete="email"></div>
      </div>
      <div class="sga-row2">
        <div class="sga-field"><label for="sga-topic">Topic</label><select id="sga-topic" name="topic"><option>Support</option><option>License / key</option><option>Plugin idea</option><option>Collab / press</option><option>Just honking</option></select></div>
        <div class="sga-field"><label for="sga-plugin">Plugin</label><select id="sga-plugin" name="plugin"><option value="">Not about a plugin</option>{opts}</select></div>
      </div>
      <div class="sga-field"><label for="sga-msg">Message</label><textarea id="sga-msg" name="message" required placeholder="For support, include your DAW and your Mac or Windows version."></textarea></div>
      <button class="sga-btn sga-btn--amber" type="submit">Send honk</button>
      <p class="sga-note">This opens your email app with everything filled in. Prefer to write it yourself? Email <a class="sga-link" href="mailto:{e(CFG["email"])}">{e(CFG["email"])}</a></p>
    </form>
    <div class="sga-tiles">
      <a class="sga-tile" href="mailto:{e(CFG["email"])}"><span class="sga-tile__ic">{ICON["mail"]}</span><div><h3>Email</h3><p>{e(CFG["email"])}</p></div><span class="sga-tile__go">→</span></a>
      <a class="sga-tile" href="{CFG["login_url"]}"><span class="sga-tile__ic">{ICON["key"]}</span><div><h3>Lost a download or key?</h3><p>Log in to Payhip to re-download any purchase.</p></div><span class="sga-tile__go">→</span></a>
      <a class="sga-tile" href="{CFG["instagram"]}" target="_blank" rel="noopener"><span class="sga-tile__ic">{ICON["ig"]}</span><div><h3>Instagram</h3><p>@sillygooseaudio</p></div><span class="sga-tile__go">→</span></a>
      <a class="sga-tile" href="{CFG["facebook"]}" target="_blank" rel="noopener"><span class="sga-tile__ic">{ICON["fb"]}</span><div><h3>Facebook</h3><p>Silly Goose Audio</p></div><span class="sga-tile__go">→</span></a>
      <div class="sga-goosebox">
        <img class="sga-honk" src="{a}images/goose-head.png" alt="Click the goose" width="400" height="386">
        <p class="sga-note">Most questions are answered in the <a class="sga-link" href="{CFG["pages"]["faq"]}">FAQ</a>. This goose answers none of them.</p>
      </div>
    </div>
  </div>
</section>
'''


PAGES = {"home": ("Silly Goose Audio", page_home), "shop": ("Shop", page_shop),
         "faq": ("FAQ", page_faq), "contact": ("Contact", page_contact)}

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap">'


SLOGAN = "Serious plugins for unserious geese"


def slogan_top(a):
    return f'''<div class="sga-slogan" role="note"><img class="sga-honk" src="{a}images/goose-head.png" alt="" width="400" height="386"><span>{SLOGAN}</span><img class="sga-honk sga-flip" src="{a}images/goose-head.png" alt="" width="400" height="386"></div>'''


def slogan_foot(a):
    pg = CFG["pages"]
    return f'''<footer class="sga-foot">
  <div class="sga-wrap sga-foot__in">
    <img class="sga-foot__goose sga-honk" src="{a}images/goose-head.png" alt="Click the goose" width="400" height="386" loading="lazy">
    <p class="sga-foot__slogan">{SLOGAN}.</p>
    <nav class="sga-foot__nav" aria-label="Footer"><a href="{pg["home"]}">Home</a><a href="{pg["shop"]}#originals">Originals</a><a href="{pg["shop"]}#sister">Sister Plugins</a><a href="{pg["shop"]}#all">All Plugins</a><a href="{pg["faq"]}">FAQ</a><a href="{pg["contact"]}">Contact</a></nav>
    {socials()}
    <p class="sga-note">© Silly Goose Audio · VST3 · AU · Standalone · macOS + Windows</p>
  </div>
</footer>'''


def embed(name, assets):
    css = (ROOT / "src/sga.css").read_text()
    js = (ROOT / "src/sga.js").read_text()
    body = PAGES[name][1](assets)
    return f'''<!-- Silly Goose Audio · {name} page · generated by WEBSITE/build.py — edit the source, not this file -->
{FONTS}
<style>{css}</style>
<div class="sga sga-page-{name}" data-assets="{assets}">{slogan_top(assets)}{body}{slogan_foot(assets)}</div>
<script>{js}</script>
'''


def mock_shell(name, inner):
    """Local preview only: imitates the Payhip header (nav + search/account/cart) so you can judge the page in context."""
    nav = "".join(
        f'<a href="{k}.html"{" class=on" if k == name else ""}>{label}</a>'
        for k, label in [("home", "Home"), ("shop", "Shop"), ("faq", "FAQ"), ("contact", "Contact")]
    )
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{PAGES[name][0]} · Silly Goose Audio (preview)</title>
<style>
  body {{ margin: 0; background: #0d0d0d; font-family: -apple-system, Helvetica, sans-serif; }}
  .ph-bar {{ background: #f59e0b; color: #111; font: 600 12px/1 -apple-system, sans-serif; text-align: center; padding: 8px; }}
  .ph-head {{ display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 18px 40px; background: #111; border-bottom: 1px solid #262626; }}
  .ph-head img {{ height: 64px; }}
  .ph-nav {{ display: flex; gap: 22px; }}
  .ph-nav a {{ color: #f59e0b; font-size: 14px; text-decoration: none; }}
  .ph-nav a.on {{ text-decoration: underline; text-underline-offset: 5px; }}
  .ph-icons {{ display: flex; gap: 18px; color: #f59e0b; }}
  .ph-icons svg {{ width: 20px; height: 20px; }}
  .ph-foot {{ padding: 40px; text-align: center; color: #6b6b6b; font-size: 13px; background: #111; border-top: 1px solid #262626; }}
  .ph-main {{ max-width: 1100px; margin: 0 auto; }} /* imitates Payhip's centred section container */
  @media (max-width: 720px) {{ .ph-head {{ padding: 14px 16px; flex-wrap: wrap; }} .ph-head img {{ height: 44px; }} .ph-nav {{ order: 3; width: 100%; justify-content: space-between; }} }}
</style></head><body>
<div class="ph-bar">PREVIEW · the bar below imitates Payhip's own header, cart and account, which stay as they are</div>
<header class="ph-head"><a href="home.html"><img src="../../images/sga-logo.webp" alt="Silly Goose Audio"></a><nav class="ph-nav">{nav}</nav>
<div class="ph-icons" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/></svg><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 8h14l-1 12H6zM9 8V6a3 3 0 0 1 6 0v2"/></svg></div></header>
<main class="ph-main">{inner}</main>
<footer class="ph-foot">© Silly Goose Audio · Powered by Payhip</footer>
</body></html>'''


def product_bundle():
    """Header Code Injection assets: product-page reskin, served from GitHub Pages so it can change without re-pasting."""
    a = CFG["assets_base"]
    data = {
        "assets": a,
        "fonts": FONTS.split('href="')[-1].split('"')[0],
        "shop": CFG["pages"]["shop"],
        "products": {p["id"]: {k: p.get(k) for k in ("name", "ver", "sub", "blurb", "box", "kind", "price", "new")} for p in LIVE},
        "cards": {p["id"]: card(p, a) for p in LIVE},
        "strip": f'<div class="sga sga-pp-strip">{slogan_top(a)}</div>',
        "foot": f'<div class="sga sga-pp-foot">{slogan_foot(a)}</div>',
    }
    out = ROOT / "dist/site"
    out.mkdir(parents=True, exist_ok=True)
    (out / "product.js").write_text("window.SGA_DATA = " + json.dumps(data) + ";\n" + (ROOT / "src/product.js").read_text())
    (out / "product.css").write_text((ROOT / "src/sga.css").read_text() + "\n" + (ROOT / "src/product.css").read_text())
    (ROOT / "dist/payhip/header-code.html").write_text(
        "<!-- Silly Goose Audio: product page theme. Paste into Store Builder > Change store style > Advanced > Header code injection. -->\n"
        f'<link rel="stylesheet" href="{a}dist/site/product.css">\n'
        f'<script src="{a}dist/site/product.js" defer></script>\n')
    print("built product theme: dist/payhip/header-code.html (+ dist/site/product.js, product.css)")
    (ROOT / "dist/payhip/checkout.css").write_text((ROOT / "src/checkout.css").read_text().replace("https://joshwilk17-sudo.github.io/sga-website/", a))
    print("built checkout theme: dist/payhip/checkout.css")


def main():
    out_p, out_v = ROOT / "dist/payhip", ROOT / "dist/preview"
    out_p.mkdir(parents=True, exist_ok=True)
    out_v.mkdir(parents=True, exist_ok=True)
    for name in PAGES:
        (out_p / f"{name}.html").write_text(embed(name, CFG["assets_base"]))
        # preview pages link to each other locally
        saved = dict(CFG["pages"])
        CFG["pages"].update({k: f"{k}.html" for k in PAGES})
        (out_v / f"{name}.html").write_text(mock_shell(name, embed(name, "../../")))
        CFG["pages"].update(saved)
        print(f"built {name}: dist/payhip/{name}.html ({(out_p / f'{name}.html').stat().st_size // 1024} KB)")
    product_bundle()
    if "REPLACE-ME" in CFG["assets_base"]:
        print("\nNOTE: assets_base in config.json is still a placeholder. Images/honks in dist/payhip won't load until you set it.")


if __name__ == "__main__":
    main()
