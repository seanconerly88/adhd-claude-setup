# Partner intake

Ask for everything in one message. Do not start writing until the audience answer is in.

| Field | Notes |
|---|---|
| Partner name, first name | |
| Instagram handle + URL | Linked on the page for return traffic |
| **Audience** (ASK FIRST) | Age range, gender split, what they care about, **what they are not into**. Get it from the partner if Sean can; if Sean only has it secondhand, say so |
| Bio in the partner's own words | Their own text. Use it nearly verbatim; do not embellish |
| Photos | Hero headshot URL (GHL-hosted) and optional body shot, or attached files. One photo is fine |
| Page slug | Becomes the URL path and the Source URL routing key, e.g. `shelby` |
| Any approved quote | Do not invent quotes. None given means no quotes |
| Words/claims to avoid | |

Note the audience in the partner JSON `audience` field verbatim so the copy can be reviewed against it later.

## Business partners (a studio, gym, brand instead of a person)
Built first with HOTWORX Goodlettsville. Same intake, plus:
- Which location/owner, and the display name (e.g. "HOTWORX Goodlettsville"; `partner_first` = the same).
- Hero = a studio/lifestyle photo (no face, so `hero_mirror: false`; never mirror photos that contain text or logos). Ask for a **high-res original (1600px+ wide)**; chat attachments are thumbnails and will look blurry in preview.
- Body section = the logo: set `body_fit: "contain"`, `body_bg: "#FFFFFF"`, `body_pad: "14%"`, `body_ratio: "1/1"`, `body_frame: "rgba(14,14,14,.16)"`, `body_pos: "50% 50%"`. Logos without transparency sit on the white card.
- Bio is the business's own about text in "we" voice. Replace "!" with "." (page tone), otherwise keep their words. Pull quote = their own closing line, removed from the paragraph so it is not repeated.
- Confirm they have OK'd the logo use, and whether "Paid partnership" is accurate for a business partner. If not, set `"disclosure"` in the partner JSON to override the spa's template.
- Audience may be neutral (no gender or age given). Write to their stated priorities, not assumed demographics.
- Optional: `partner_type: "business"` in the JSON (informational).
