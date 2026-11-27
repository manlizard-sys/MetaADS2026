// Checks which go.orchidpros.com (GoHighLevel) pages exist and whether they are indexable (read only).
// URL list = pages referenced in this repo + the GHL sitemap if it lists any.
// Usage: node scripts/seo/ghl_pages.mjs   Output: seo/audit/ghl_pages.csv, seo/audit/ghl_pages.json
import { mkdirSync, writeFileSync } from 'node:fs';
import { attr, countWords, csvRow, decode, fetchChain, metaContent, sleep, stripTags, UA } from './lib.mjs';

const OUT = 'seo/audit';
mkdirSync(OUT, { recursive: true });
const BASE = 'https://go.orchidpros.com';

const known = {
  '/hire': 'landing (Meta, octubre)',
  '/hire-form': 'landing solo formulario (prueba A)',
  '/hire-50off': 'landing oferta 50% (noviembre)',
  '/50off-form': 'landing solo formulario 50%',
  '/practices-free-month': 'landing BF salud',
  '/practices-free-month-page-865761': 'paso/variante de practices-free-month',
  '/practices-free-month-thanks': 'gracias salud',
  '/business-free-month': 'landing BF emprendedores',
  '/business-free-month-page': 'paso/variante de business-free-month',
  '/business-free-month-thanks': 'gracias emprendedores',
  '/book-a-call': 'agendar llamada',
  '/book-a-call-thanks': 'gracias agendar',
  '/brief': 'newsletter The Delegate Brief',
  '/brief-thanks': 'gracias newsletter (probable)',
  '/': 'raíz del subdominio',
};

const sm = await fetch(`${BASE}/sitemap.xml`, { headers: { 'User-Agent': UA } });
const smText = await sm.text();
const smLocs = [...smText.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)].map((m) => decode(m[1]));
const robots = await (await fetch(`${BASE}/robots.txt`, { headers: { 'User-Agent': UA } })).text();

const paths = new Set(Object.keys(known));
for (const u of smLocs) { try { const p = new URL(u); if (p.hostname === 'go.orchidpros.com') paths.add(p.pathname.replace(/\/$/, '') || '/'); } catch {} }

const rows = [];
for (const p of paths) {
  const url = BASE + p;
  const { chain, final } = await fetchChain(url);
  const r = { path: p, role: known[p] || 'en sitemap de GHL', in_ghl_sitemap: smLocs.some((u) => u.replace(/\/$/, '') === url.replace(/\/$/, '')) };
  r.status = final?.status ?? chain.at(-1)?.status;
  r.redirect_chain = chain.length > 1 ? chain.map((c) => `${c.status} ${c.url}`).join(' -> ') : '';
  if (final?.body) {
    const head = final.body.split(/<\/head>/i)[0];
    r.meta_robots = metaContent(head, 'robots') || '';
    r.x_robots_tag = final.headers['x-robots-tag'] || '';
    r.noindex = /noindex/i.test(r.meta_robots + ' ' + r.x_robots_tag);
    const canon = (head.match(/<link\b[^>]*rel\s*=\s*["']canonical["'][^>]*>/i) || [])[0];
    r.canonical = canon ? attr(canon, 'href') : '';
    r.title = stripTags((head.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || '');
    r.meta_description = metaContent(head, 'description') || '';
    r.word_count = countWords(final.body.slice(final.body.search(/<body\b/i)));
  }
  rows.push(r);
  await sleep(250);
}

const cols = ['path', 'role', 'status', 'redirect_chain', 'in_ghl_sitemap', 'noindex', 'meta_robots', 'x_robots_tag', 'canonical', 'title', 'meta_description', 'word_count'];
writeFileSync(`${OUT}/ghl_pages.csv`, '﻿' + [csvRow(cols), ...rows.map((r) => csvRow(cols.map((c) => r[c])))].join('\n'));
writeFileSync(`${OUT}/ghl_pages.json`, JSON.stringify({ checked_at: new Date().toISOString(), robots_txt: robots, sitemap_status: sm.status, sitemap_locs: smLocs, sitemap_raw_head: smText.slice(0, 1500), pages: rows }, null, 2));
console.table(rows.map(({ path, status, noindex, in_ghl_sitemap, title, word_count }) => ({ path, status, noindex, in_ghl_sitemap, title: (title || '').slice(0, 45), word_count })));
console.log('GHL sitemap status', sm.status, 'locs', smLocs.length);
