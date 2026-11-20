const { chromium } = require('playwright');
const S = '/tmp/claude-0/-home-user-MetaADS2026/bf71e0df-652f-5f76-93c1-b26abc9f7914/scratchpad/v2';
const OUT = process.argv[2] || S + '/elec_out';
const LIC = process.argv[3] || '';
(async () => {
  require('fs').mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1450 }, deviceScaleFactor: 2 });
  await p.goto('file://' + S + '/elec.html' + (LIC ? '?lic=' + encodeURIComponent(LIC) : ''), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  for (const a of await p.$$('.ad')) await a.screenshot({ path: `${OUT}/${await a.getAttribute('id')}.png` });
  const p2 = await b.newPage({ viewport: { width: 1200, height: 1450 }, deviceScaleFactor: 1 });
  await p2.goto('file://' + S + '/elec.html' + (LIC ? '?lic=' + encodeURIComponent(LIC) : ''), { waitUntil: 'networkidle' });
  await p2.evaluate(() => document.fonts.ready);
  await p2.screenshot({ path: `${S}/elec_sheet.png`, fullPage: true });
  await b.close();
})();
