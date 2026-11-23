# Copy rules

What the partner JSON copy fields must do. The shape is in `library/partners/antiaging-health/shelby-neubauer.json`.

1. **About them, not us.** The hero speaks to the follower's life and standards, reached through the partner. Lead with the audience, then the offer.
2. **Match the audience exactly.** Wrong audience was the biggest miss on the first build (assumed medspa/Botox clients for a lifestyle audience). Do not mention medspa services (Botox, fillers, Morpheus8, B12) unless the intake says that audience wants them. `build.py` warns on these.
3. **Mixed-gender audience:** no gendered language ("the woman who..."). Pair interests: what you wear / how you train / who you trust.
4. **Bio section** is the partner's own words. Light trimming only. The pull quote must be a line from or faithful to the bio, never invented.
5. **No claims the partner did not make.** Do not say they vetted, use, recommend or are a patient of the spa unless they told Sean so. "Sent you here for a reason" is the safe bridge.
6. **No outcome claims** for peptides/HRT. Allowed framing: "support", "guided by a physician", "your physician explains the options and risks". Banned (build fails): guarantee, cure, reverse aging, look younger, clinically proven, weight loss, FDA approved.
7. **Hero structure:** headline in two short balanced lines (`h1_line1`, `h1_line2`); `hero_lead` = one line about their standards, then the offer in plain words, ending "Your part is one <N>-minute consult." N must equal the spa's consult length.
8. **Three audience cards** (`cards`): three short "what changes" areas (e.g. Skin / Energy / Recovery), each with a one-line text that uses "support", not promises. Pick the ones that match this audience.
9. Tight and punchy. No filler, no exclamation points.
10. Process steps, comparison, FAQ, stats are fixed template content. Do not edit them per partner.
