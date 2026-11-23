#!/usr/bin/env python3
"""Build a spa x partner landing page for a GHL custom code block.

  build.py --spa antiaging-health --partner shelby-neubauer [--preview] [--local-hero PATH] [--local-body PATH]

Reads library/spas/<spa>.json + library/partners/<spa>/<partner>.json, fills assets/body.html and
assets/style.css, writes library/pages/<spa>/<partner>.html and a .seo.md next to it, runs checks.
--preview writes <partner>.preview.html with local images (never paste that one into GHL).
"""
import argparse, html, json, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

def rgb(h):
    h = h.lstrip('#'); return ','.join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))

def esc(s): return html.escape(s, quote=False)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spa', required=True); ap.add_argument('--partner', required=True)
    ap.add_argument('--preview', action='store_true')
    ap.add_argument('--local-hero'); ap.add_argument('--local-body')
    a = ap.parse_args()
    spa = json.load(open(f'{ROOT}/library/spas/{a.spa}.json'))
    p = json.load(open(f'{ROOT}/library/partners/{a.spa}/{a.partner}.json'))
    c, f = spa['colors'], spa['fonts']
    n = spa['consult_min']

    hero_img, body_img = p['hero_img'], p.get('body_img') or ''
    body_mirror = p.get('body_mirror', False)
    body_zoom = p.get('body_zoom')
    if not body_img:   # single-photo partner: reuse the hero shot, flipped the other way and cropped tighter
        body_img = hero_img
        body_mirror = not p.get('hero_mirror', False)
        body_zoom = body_zoom or 1.25
    if a.preview:
        hero_img = ('file://' + a.local_hero) if a.local_hero else hero_img
        if a.local_body: body_img = 'file://' + a.local_body
        elif a.local_hero and not p.get('body_img'): body_img = hero_img
    bt = ' '.join(x for x in [('scaleX(-1)' if body_mirror else ''), (f'scale({body_zoom})' if body_zoom else '')] if x) or 'none'

    t = {
      'BRAND_A': spa['brand_a'], 'BRAND_B': spa['brand_b'], 'SPA_NAME': spa['spa_name'], 'CITY': spa['city'],
      'PHONE_DISPLAY': spa['phone_display'], 'PHONE_TEL': spa['phone_tel'], 'CALENDAR_URL': spa['calendar_url'],
      'CONSULT_MIN': str(n), 'STAT3_NUM': spa['stat3_num'], 'STAT3_LABEL': spa['stat3_label'], 'STEP3_TEXT': spa['step3_text'],
      'DISCLOSURE': p.get('disclosure') or spa['disclosure_template'].format(partner=p['partner_name'], spa=spa['spa_name']),
      'PARTNER_NAME': p['partner_name'], 'IG_HANDLE': p['ig_handle'], 'IG_URL': p['ig_url'],
      'H1_LINE1': p['h1_line1'], 'H1_LINE2': p['h1_line2'], 'HERO_LEAD': p['hero_lead'],
      'NEXT_EYEBROW': p['next_eyebrow'], 'NEXT_H2': p['next_h2'], 'BIO_H2': p['bio_h2'], 'PULL': p['pull'],
      'HERO_IMG': hero_img, 'BODY_IMG': body_img,
    }
    for i, card in enumerate(p['cards'], 1):
        t[f'CARD{i}_SMALL'], t[f'CARD{i}_TITLE'], t[f'CARD{i}_TEXT'] = card['small'], card['title'], card['text']
    t = {k: esc(v) for k, v in t.items()}
    t['BIO_PARAGRAPHS'] = '\n      '.join(f'<p>{esc(x)}</p>' for x in p['bio_paragraphs'])
    # raw (CSS) tokens
    css_t = {k.upper(): v for k, v in c.items()}
    css_t.update({'INK_RGB': rgb(c['ink']), 'CREAM_RGB': rgb(c['cream']), 'TAUPE_RGB': rgb(c['taupe']),
      'FONT_HEAD': f['head'], 'FONT_BODY': f['body'],
      'HERO_POS': p.get('hero_pos', '50% 22%'), 'HERO_POS_MOBILE': p.get('hero_pos_mobile', '50% 20%'),
      'HERO_TRANSFORM': 'scaleX(-1)' if p.get('hero_mirror', True) else 'none',
      'BODY_POS': p.get('body_pos', '50% 18%'), 'BODY_TRANSFORM': bt,
      'BODY_RATIO': p.get('body_ratio', '4/5'), 'BODY_FIT': p.get('body_fit', 'cover'), 'BODY_BG': p.get('body_bg', 'transparent'), 'BODY_PAD': p.get('body_pad', '0'),
      'BODY_FRAME': p.get('body_frame', f"rgba({rgb(c['cream'])},.7)")})

    def fill(s, m):
        return re.sub(r'\{\{(\w+)\}\}', lambda x: m[x.group(1)] if x.group(1) in m else x.group(0), s)
    body = fill(open(f'{ROOT}/assets/body.html').read(), t)
    css = fill(open(f'{ROOT}/assets/style.css').read(), {**t, **css_t})
    css = f"@import url('{f['url']}');" + re.sub(r'\s+', ' ', css)
    left = re.findall(r'\{\{\w+\}\}', body + css)
    errs = []
    if left: errs.append(f'unfilled placeholders: {sorted(set(left))}')
    if '`' in css or '${' in css: errs.append('CSS contains a backtick or ${ which breaks the JS injection')

    out = f'''{body}
<script>
(function(){{
  var st=document.createElement('style');
  st.textContent=`{css}`;
  document.head.appendChild(st);
  var root=document.querySelector('.aah');
  var cal='{spa['calendar_url']}'+'?{spa['source_url_field']}='+encodeURIComponent(window.location.href.split('#')[0]);
  document.getElementById('aah-calendar').src=cal;
  document.getElementById('aah-cal-link').href=cal;
  root.classList.add('js');
  document.getElementById('aah-yr').textContent=new Date().getFullYear();
  if(!('IntersectionObserver' in window)){{root.classList.remove('js');return;}}
  var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target);}}}});}},{{threshold:.1}});
  root.querySelectorAll('.rv').forEach(function(el){{io.observe(el);}});
}})();
</script>
<script src="https://link.msgsndr.com/js/form_embed.js" type="text/javascript"></script>
'''
    # ---- checks on the visible text
    visible = re.sub(r'<script.*?</script>', '', out, flags=re.S)
    mins = set(re.findall(r'(\d+)[- ]min', visible))
    if mins - {str(n)}: errs.append(f'consult length mismatch: page mentions {sorted(mins)}, spa profile says {n}')
    for w in ['guarantee', 'cure', 'reverse aging', 'reverse your age', 'look younger', 'anti-aging results', 'fda approved', 'clinically proven', 'lose weight', 'weight loss']:
        if w in visible.lower(): errs.append(f'risky claim wording: "{w}"')
    if 'Paid partnership' not in visible: errs.append('disclosure line missing')
    other = [s for s in ['Botox', 'Morpheus', 'B12'] if s.lower() in visible.lower()]
    if other: errs.append(f'medspa-only service mentioned (check audience): {other}')
    if p['partner_name'] not in visible: errs.append('partner name missing')
    # ---- SEO
    loc = spa['seo']['locations']; sl = p['slug']
    title = f"{p['partner_name']} x {spa['spa_name']} | Peptides & HRT"
    desc = f"Welcomed by {p['partner_name']}. {spa['seo']['offer_phrase']} from {spa['spa_name']}, delivered to your door. Start with a free {n}-minute consult."
    if len(desc) > 160:   # long partner names: drop the delivery phrase
        desc = f"Welcomed by {p['partner_name']}. {spa['seo']['offer_phrase']} from {spa['spa_name']}. Start with a free {n}-minute consult."
    share_desc = f"{p['partner_first']} sent you. {spa['seo']['offer_phrase']}, delivered to your door. Your part is one free {n}-minute consult."
    kw = ', '.join([f'peptide therapy {l}' for l in loc[:2]] + [f'hormone replacement therapy {loc[0]}', 'physician-guided peptides', spa['spa_name'], p['partner_name']])
    if len(title) > 60: errs.append(f'SEO title is {len(title)} chars (>60)')
    if len(desc) > 160: errs.append(f'SEO description is {len(desc)} chars (>160)')
    seo = f'''# SEO: {p['partner_name']} x {spa['spa_name']}

| Field | Copy |
|---|---|
| URL slug | `/{sl}` |
| SEO title ({len(title)} chars) | {title} |
| Meta description ({len(desc)} chars) | {desc} |
| Keywords | {kw} |
| Author | {spa['spa_name']} |

**Social share preview**

| Field | Copy |
|---|---|
| Share title | {p['h1_line1']} {p['h1_line2']} |
| Share description | {share_desc} |
| Share image | {p['hero_img']} |

**Image alt text**

- Hero: {p['partner_name']}
- Body: {p['partner_name']}

**Recommendations**

- Keep this page out of search (noindex). Its process, comparison and FAQ copy is shared with the spa's own peptides page and would compete with it. Traffic comes from {p['partner_first']}'s link.
- Workflow: appointment-booked trigger, then If/Else on contact field Source URL *contains* `/{sl}`.
'''
    d = f"{ROOT}/library/pages/{a.spa}"; os.makedirs(d, exist_ok=True)
    name = a.partner + ('.preview' if a.preview else '')
    open(f'{d}/{name}.html', 'w').write(out)
    if not a.preview: open(f'{d}/{a.partner}.seo.md', 'w').write(seo)
    print(f'wrote {d}/{name}.html ({len(out)} bytes)')
    if errs:
        print('CHECKS FAILED:'); [print(' -', e) for e in errs]; sys.exit(1)
    print('checks passed')

main()
