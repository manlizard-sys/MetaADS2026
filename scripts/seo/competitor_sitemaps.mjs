// Reads competitors' public XML sitemaps and classifies their URLs by page type (pricing, alternatives, vs, calculators, industry guides...).
// Read only; respects a small delay between requests. Source of every number = the competitor's own sitemap on the run date.
// Usage: node scripts/seo/competitor_sitemaps.mjs   Output: seo/keywords/competencia_paginas.csv, seo/keywords/competencia_paginas.json
import { mkdirSync, writeFileSync } from 'node:fs';
import { csvRow, decode, sleep, UA } from './lib.mjs';

const OUT = 'seo/keywords';
mkdirSync(OUT, { recursive: true });

// Domains from build/research/competencia/Competencia_Orchid_2026-11-24.pdf
const COMPETITORS = {
  'Wing Assistant': 'https://wingassistant.com', Wishup: 'https://www.wishup.co', HelloRache: 'https://hellorache.com',
  MedVA: 'https://www.medva.com', Portiva: 'https://portiva.com', HelpSquad: 'https://helpsquad.com', Pineapple: 'https://trypineapple.com',
  Virtustant: 'https://www.virtustant.com', 'Virtual Latinos': 'https://www.virtuallatinos.com', CallForce: 'https://callforce.global',
  'Rose Talent': 'https://rosetalentsolutions.io', 'VA Masters': 'https://vamasters.com', 'Hire Overseas': 'https://www.hireoverseas.com',
  'Stealth Agents': 'https://stealthagents.com', Athena: 'https://www.athena.com', BELAY: 'https://belaysolutions.com', Boldly: 'https://boldly.com',
  Prialto: 'https://www.prialto.com', MyOutDesk: 'https://www.myoutdesk.com', 'Time etc': 'https://www.timeetc.com', Somewhere: 'https://somewhere.com',
  South: 'https://www.hireinsouth.com', 'Persona Talent': 'https://www.personatalent.com',
};

const CATS = {
  pricing: /pric|\/cost|-cost|rates?\b|how-much/,
  alternatives: /alternative/,
  versus: /-vs-|\/vs\/|versus|compar/,
  calculator: /calculator|savings|roi/,
  healthcare: /medical|dental|dentist|health|chiropract|physical-therap|physiotherap|clinic|patient|hipaa|scribe|optometr|veterinar|therapy|mental|billing|insurance-verif|prior-auth/,
  legal: /\blaw\b|law-|lawyer|legal|attorney|paralegal|immigration/,
  accounting: /accounting|accountant|bookkeep|\bcpa\b|cpa-|\btax\b|tax-|finance|financial/,
  real_estate: /real-estate|realtor|realestate|property|mortgage|\bisa\b|transaction-coord/,
  small_business: /small-business|entrepreneur|startup|founder|ecommerce|e-commerce/,
  country_region: /colombia|philippin|latin|latam|mexic|argentin|brazil|nearshore|offshore|south-africa|india/,
  bilingual: /bilingual|spanish|espanol/,
  guide_blog: /\/blog\/|\/resources?\/|\/guide|\/learn\/|\/articles?\//,
};

async function get(url) {
  try {
    const r = await fetch(url, { headers: { 'User-Agent': UA }, redirect: 'follow', signal: AbortSignal.timeout(20000) });
    if (!r.ok) return null;
    const t = await r.text();
    return /<(urlset|sitemapindex)/i.test(t) ? t : null;
  } catch { return null; }
}
const locs = (xml) => [...xml.matchAll(/<loc>\s*(?:<!\[CDATA\[)?\s*([^<\s\]]+)/g)].map((m) => decode(m[1]));

async function sitemapUrls(base) {
  const seeds = [];
  try {
    const r = await fetch(`${base}/robots.txt`, { headers: { 'User-Agent': UA }, signal: AbortSignal.timeout(15000) });
    if (r.ok) for (const m of (await r.text()).matchAll(/^\s*sitemap:\s*(\S+)/gim)) seeds.push(m[1]);
  } catch {}
  seeds.push(`${base}/sitemap_index.xml`, `${base}/sitemap.xml`);
  const seen = new Set();
  const urls = new Set();
  const queue = [...new Set(seeds)];
  let fetched = 0;
  const used = [];
  while (queue.length && fetched < 60 && urls.size < 30000) {
    const sm = queue.shift();
    if (seen.has(sm)) continue;
    seen.add(sm);
    const xml = await get(sm);
    fetched++;
    if (!xml) continue;
    used.push(sm);
    if (/<sitemapindex/i.test(xml)) queue.push(...locs(xml).filter((u) => !/\.gz$/.test(u)));
    else locs(xml).forEach((u) => urls.add(u));
    if (urls.size && seeds.indexOf(sm) >= 0 && seeds.indexOf(sm) < seeds.length - 2 && queue.length === 0) break;
    await sleep(250);
  }
  return { urls: [...urls], sitemaps_used: used };
}

const results = [];
for (const [name, base] of Object.entries(COMPETITORS)) {
  const { urls, sitemaps_used } = await sitemapUrls(base);
  const row = { competitor: name, domain: new URL(base).hostname, total_urls: urls.length, sitemaps_found: sitemaps_used.length, examples: {} };
  for (const [cat, re] of Object.entries(CATS)) {
    const hits = urls.filter((u) => { try { return re.test(new URL(u).pathname.toLowerCase()); } catch { return false; } });
    row[cat] = hits.length;
    row.examples[cat] = hits.slice(0, 8).map((u) => new URL(u).pathname);
  }
  results.push(row);
  console.log(`${name.padEnd(16)} ${String(urls.length).padStart(6)} URLs  pricing ${row.pricing}  alt ${row.alternatives}  vs ${row.versus}  calc ${row.calculator}  health ${row.healthcare}  legal ${row.legal}`);
}

const cols = ['competitor', 'domain', 'total_urls', ...Object.keys(CATS)];
writeFileSync(`${OUT}/competencia_paginas.csv`, '﻿' + [csvRow(cols), ...results.map((r) => csvRow(cols.map((c) => r[c])))].join('\n'));
writeFileSync(`${OUT}/competencia_paginas.json`, JSON.stringify({ fetched_at: new Date().toISOString(), note: 'Conteos por patrón en la ruta de la URL; una URL puede caer en varias categorías. 0 URLs = sitemap no encontrado o bloqueado.', results }, null, 2));
