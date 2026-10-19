# Silly Goose Audio: custom Payhip pages

Four custom pages (Home, Shop, FAQ, Contact) in the house dark/amber box-art style. They drop into Payhip as **Embed Code** sections, so Payhip's own header, search, cart, account/login and checkout stay exactly as they are.

```
WEBSITE/
  config.json          <- edit this: asset URL, page links, contact email
  build.py             <- product list + page content; run it after any change
  src/sga.css, sga.js  <- shared styles and behaviour (tabs, FAQ search, honk Easter egg)
  images/              <- web-sized box art (WebP), logo, goose head
  audio/               <- the 7 house honks (for the click-the-goose Easter egg)
  dist/payhip/*.html   <- PASTE THESE into Payhip (generated)
  dist/preview/*.html  <- local preview with a mock Payhip header (generated)
```

## What Payhip needs first

Payhip only allows Embed Code sections (and header/footer code) on stores with a **custom domain** connected (e.g. `sillygooseaudio.com`). See Payhip help: *Embed code on your Payhip store* and *Custom domain*.

## Setup, once

1. **Images and honks are hosted on GitHub Pages.** This folder is the public repo [joshwilk17-sudo/sga-website](https://github.com/joshwilk17-sudo/sga-website), served at `https://joshwilk17-sudo.github.io/sga-website/`. When you add or change anything in `images/` or `audio/`, commit and push it, and the live site picks it up within about a minute.
2. **Edit `config.json`:**
   - `assets_base`: already set to the GitHub Pages URL above.
   - `pages`: the real URLs of your Payhip pages once you create them (Shop, FAQ, Contact).
   - `email`: your support address (currently a placeholder, `hello@sillygooseaudio.com`).
3. Run `python3 build.py`.

## Put it into Payhip

1. In Payhip, open **Store → Store Builder**.
2. **Store style:** set the background to near-black (`#0d0d0d`) and accent/links to amber (`#f59e0b`) so Payhip's header and cart match.
3. **Home page:** remove the default sections you don't want, add section → **Embed Code**, paste all of `dist/payhip/home.html`, publish.
4. **Add pages:** create custom pages **Shop**, **FAQ**, **Contact**. On each one, add an **Embed Code** section and paste the matching `dist/payhip/<page>.html`.
5. **Header navigation:** set the links to Home · Shop · FAQ · Contact. You can deep-link the shop tabs:
   - `/Store#originals`: Original Plugins
   - `/Store#sister`: Sister Plugins
   - `/Store#all`: All Plugins (this is the default)
   Leave the cart and account icons alone.
6. **Product pages:** go to **Change store style → Advanced → Header code injection** and paste `dist/payhip/header-code.html` (three lines). Every product page (`/b/<code>`) then gets the box art, styled title and buttons, the slogan strip, "More from the flock" and the footer. Payhip's price box, Add to Cart, Buy Now, reviews and checkout are untouched.
7. **Checkout page:** Payhip allows CSS (not JavaScript) on checkout. Open any product, click **Buy Now**, click the gear icon to open **Customize Page**, and paste all of `dist/payhip/checkout.css` into its custom CSS box. In the same menu, set the **Buy Now button colour** to `#f59e0b` and the banner colour to `#0d0d0d`, and upload `images/sga-logo.png` as the logo. Card and PayPal fields come from the payment provider and keep their own look.
8. Payhip can't preview embed code inside the builder, so check the live site after you publish.

Every "Buy" or "Get it free" button links to the product's own Payhip page (`sillygooseaudio.com/b/<code>`), so add-to-cart, checkout, license keys and downloads all still run through Payhip.

## Adding a new plugin

1. Render its box art (`BOX-ART/render.sh`), then make the web copy:
   `sips -Z 720 BOX-ART/renders/<id>_box.png --out /tmp/<id>.png && cwebp -q 82 -alpha_q 90 /tmp/<id>.png -o WEBSITE/images/box/<id>.webp`
2. Add an entry to `PRODUCTS` in `build.py` with its Payhip code, price, category and tagline. Set `id=None` for a "hatching soon" teaser.
3. Run `python3 build.py`, commit and push (`git add -A && git commit -m "Add <plugin>" && git push`), then re-paste the Home and Shop blocks. Product pages update by themselves (the header code loads `dist/site/product.js` from GitHub Pages; allow about 10 minutes for caches).

## Preview locally

From the `WEBSITE` folder, run `python3 -m http.server 8765`, then open <http://localhost:8765/dist/preview/home.html>.
