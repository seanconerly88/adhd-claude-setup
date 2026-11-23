// node preview.js <preview.html> <outdir>   -> d-hero.png, d-p0..N.png (desktop 1440), m-hero.png, m-p0..N.png (mobile 390)
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [file, out] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  for (const [n, w, h, step] of [['d', 1440, 900, 1000], ['m', 390, 844, 1500]]) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto('file://' + require('path').resolve(file));
    await p.waitForTimeout(1500);
    await p.screenshot({ path: `${out}/${n}-hero.png` });
    await p.evaluate(() => document.querySelectorAll('.rv').forEach(e => e.classList.add('in')));
    await p.waitForTimeout(1300);
    const H = await p.evaluate(() => document.documentElement.scrollHeight);
    let i = 0;
    for (let y = 0; y < H; y += step) await p.screenshot({ path: `${out}/${n}-p${i++}.png`, fullPage: true, clip: { x: 0, y, width: w, height: Math.min(step, H - y) } });
    console.log(n, 'height', H, 'parts', i, errs.length ? 'JS ERRORS: ' + errs : 'no js errors');
  }
  await b.close();
})();
