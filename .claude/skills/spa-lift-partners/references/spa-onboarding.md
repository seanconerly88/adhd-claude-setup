# Onboarding a new spa

Run this only when `library/spas/<slug>.json` does not exist. Goal: a saved profile so the next partner for this spa skips all of it.

## Ask Sean for (all at once, defaults in brackets)
1. Spa name and the **partner-program brand name** (AntiAging Medspa became "AntiAging Health": same name, "Health" instead of "Medspa"). [spa name with Medspa/Spa swapped for Health; confirm]
2. Main website URL, and the page where the peptide/HRT offer lives if there is one. These are the brand source references.
3. Logo file or URL, and any brand guide. [text wordmark in the brand font if none]
4. Calendar booking URL for this spa (one calendar, used for every partner of this spa), and confirm the consult length. Offer is always peptides + HRT.
5. Phone number, city/state, and any claims the spa will stand behind (delivery time, etc.). Anything not confirmed gets marked unverified in `verified`.
6. Does the contact field Source URL exist and sit hidden on that calendar's form? [assume yes, same setup as AntiAging]

## Then
- Pull brand: `firecrawl_scrape` the site with `formats: ["branding","screenshot"]`, and Read the screenshot. Propose the palette with exact hex: `ink` (darkest), `char`, `cream` (page background), `sand`, `taupe`, `bronze` (accent), `text`, `alt` (alternate section background), plus head and body fonts and a Google Fonts URL. If the spa's real fonts are not on Google Fonts, pick the closest and say so.
- Check contrast: cream text on ink, ink text on cream, bronze eyebrow on cream must be readable.
- Show Sean the proposed palette and fonts. **Do not save until he approves.**
- Save `library/spas/<slug>.json` using `antiaging-health.json` as the shape. Fill `verified` honestly.
- Build a throwaway partner page and look at it. The template was designed on a dark hero with warm neutrals; a spa with a very light or saturated brand needs the hero gradient colors checked.
