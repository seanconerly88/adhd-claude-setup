# GHL custom code block rules (learned the hard way)

- Output is a fragment: **no `<html>`, `<head>`, `<body>`**. The builder mangles them.
- **CSS is injected by script** (a JS template literal), never a `<style>` tag. A plain `<style>` block rendered as unstyled text with the CSS dumped on the page. Never put a backtick or `${` in CSS (build.py checks).
- All CSS is scoped under `.aah`. Content wrapper starts `opacity:0` and the script reveals it; if the script is blocked the page stays blank, so tell Sean to move the code to the page's footer code area or a Custom JS/HTML element.
- Fonts via `@import` at the start of the injected CSS.
- Nav is `position:absolute` (not fixed) to coexist with GHL.
- **Calendar iframe: 1400px tall desktop, 1250px mobile, scrolling ON.** The first build used 780px with scrolling off and cut off the calendar.
- Calendar src is set by script: `<calendar_url>?source_url=<page URL without hash>`. Same calendar for every partner of a spa; Sean routes on the Source URL field.
- GHL section settings Sean applies: full-width section, zero padding/margin, column 100%, GHL header/footer off, page background = ink color.
- `https://link.msgsndr.com/js/form_embed.js` stays at the end (auto-resizes the calendar).
- No chat widget on partner pages unless Sean asks.
