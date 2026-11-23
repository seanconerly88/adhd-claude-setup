---
name: spa-lift-partners
description: Build a creator/influencer partner landing page for a med spa's sub-brand (e.g. AntiAging Health), as a paste-ready GHL custom code block that bridges the creator's Instagram audience to a booked 15-minute consult. Use when Sean says "spa lift partners", gives a spa name plus a partner/creator name, or asks for a new partner page, a partner swap, or onboarding a new spa. Known spas run from a stored profile and template; unknown spas get onboarded first and saved to the library.
---

# Spa Lift Partners

One fixed page template. Two things change: the **spa profile** (brand, calendar, claims) and the **partner swap** (face, audience copy, bio). The offer is always physician-guided peptide + HRT, 15-minute complimentary consult, physician visit, delivery. Never rebuild the layout from scratch.

## Library layout
- `assets/body.html`, `assets/style.css`: the template. `{{TOKENS}}` only; no spa or partner text hardcoded.
- `library/spas/<spa>.json`: one file per spa (colors, fonts, wordmark, phone, city, calendar, consult length, claims, `verified` notes).
- `library/partners/<spa>/<partner>.json`: every partner ever built (audience, images, crops, all copy). Rebuildable.
- `library/pages/<spa>/<partner>.html` + `.seo.md`: last build output.
- `scripts/build.py`: fills the template and runs checks. `scripts/preview.js`: desktop + mobile screenshots.

## Flow

1. **Identify the spa.** Look for `library/spas/<slug>.json`.
   - Found → known spa. Use it as-is. Do not ask about colors, calendar, consult length or offer.
   - Not found → read `references/spa-onboarding.md` and onboard it before anything else. Do not guess brand or claims.
2. **Partner intake.** Read `references/partner-intake.md`. Ask the **audience question first** (age, gender split, interests, what they are NOT into) before writing any copy. Never infer audience from the spa's other services.
3. **Write the copy** to `references/copy-rules.md`. Save as `library/partners/<spa>/<partner>.json` (copy an existing one as the shape).
4. **Hero images.** Look at the photos before choosing.
   - One photo of the partner: use the flip + crop trick. Mirror the hero if that puts the face on the right facing the copy, and the body section reuses the same photo flipped the other way and cropped tighter (`build.py` does this automatically when `body_img` is empty).
   - Several photos: creative freedom. Pick the hero (clear face, empty space on one side for text) and crop the rest, unless Sean names one.
   - Always render and look at desktop and mobile hero before delivering.
5. **Build.** `python3 scripts/build.py --spa <spa> --partner <partner>`. Fix everything under "CHECKS FAILED". For a visual check, build with `--preview --local-hero <path> [--local-body <path>]` (attached images live in the session images folder; remote GHL image URLs are not reachable from the sandbox), then `node scripts/preview.js <preview.html> <outdir>` and Read the PNGs. Never deliver the preview file.
6. **Deliver** (see `references/delivery.md`): the full code **pasted in chat in one html block** (the side panel will not open .html attachments), the SEO block from `<partner>.seo.md`, the GHL setup steps, and a short list of anything unverified. Commit and push the library changes.

## Hard rules
- Calendar is per spa and fixed: same calendar for every partner of that spa. The page passes its own URL as `source_url`; Sean routes on the Source URL contact field. Never ask which calendar for a known spa.
- Disclosure line goes in the footer ("Paid partnership: <partner> is a partner of <spa>."). Always.
- No forms, no data collection, no privacy policy or terms. The only capture is the calendar.
- Link back to the partner's Instagram on the page (already in the template).
- Use the spa's colors and fonts, never Nxt Apex gold.
- GHL build constraints are in `references/ghl-rules.md`. Do not change the injection approach.
