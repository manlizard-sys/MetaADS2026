// PageSpeed Insights (mobile + desktop) for the key pages. Read only.
// Key: env PAGESPEED_API_KEY or a PAGESPEED_API_KEY= line in .env (optional; never printed or saved). Without it the public quota is used and often fails with 429.
// Usage: node scripts/seo/pagespeed.mjs [url ...]   Output: seo/audit/pagespeed.csv, seo/audit/pagespeed.json
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { csvRow, sleep } from './lib.mjs';

const OUT = 'seo/audit';
mkdirSync(OUT, { recursive: true });
// Key from the environment, or from the repo's .env file (ignored by git): PAGESPEED_API_KEY=...
function keyFromDotenv() {
  try {
    const line = readFileSync('.env', 'utf8').split(/\r?\n/).find((l) => /^\s*PAGESPEED_API_KEY\s*=/.test(l));
    return line ? line.split('=').slice(1).join('=').trim().replace(/^["']|["']$/g, '') : '';
  } catch { return ''; }
}
const KEY = process.env.PAGESPEED_API_KEY || keyFromDotenv();
console.log(KEY ? 'PageSpeed key: found' : 'PageSpeed key: not found (public quota)');
const redact = (s) => (KEY ? String(s).split(KEY).join('[REDACTED]') : String(s));

const DEFAULT = [
  'https://orchidpros.com/',
  'https://orchidpros.com/solutions/healthcare/',
  'https://orchidpros.com/law-firm/',
  'https://orchidpros.com/other-professionals/',
  'https://orchidpros.com/real-estate/',
  'https://orchidpros.com/about/',
];
const urls = process.argv.slice(2).length ? process.argv.slice(2) : DEFAULT;

// Keep earlier successful results so re-runs only fill gaps.
const prev = existsSync(`${OUT}/pagespeed.json`) ? JSON.parse(readFileSync(`${OUT}/pagespeed.json`, 'utf8')) : { results: [] };
const results = [];

for (const url of urls) {
  for (const strategy of ['mobile', 'desktop']) {
    const old = prev.results.find((r) => r.url === url && r.strategy === strategy && r.performance != null);
    const q = new URLSearchParams({ url, strategy });
    ['performance', 'accessibility', 'best-practices', 'seo'].forEach((c) => q.append('category', c));
    if (KEY) q.set('key', KEY);
    let row = { url, strategy, tested_at: new Date().toISOString(), with_key: Boolean(KEY) };
    try {
      let res, j;
      for (let attempt = 0; attempt < 3; attempt++) {
        res = await fetch(`https://www.googleapis.com/pagespeedonline/v5/runPagespeed?${q}`);
        j = await res.json();
        if (res.status !== 500 && res.status !== 503) break;
        await sleep(5000);
      }
      if (!res.ok) throw new Error(`HTTP ${res.status}: ${j?.error?.message || ''}`);
      const lh = j.lighthouseResult;
      const a = lh.audits;
      const cat = (k) => (lh.categories[k]?.score != null ? Math.round(lh.categories[k].score * 100) : null);
      const fe = j.loadingExperience?.metrics || {};
      const field = (k) => fe[k]?.percentile ?? null;
      row = {
        ...row,
        performance: cat('performance'), accessibility: cat('accessibility'), best_practices: cat('best-practices'), seo: cat('seo'),
        lab_lcp_s: +(a['largest-contentful-paint'].numericValue / 1000).toFixed(2),
        lab_cls: +a['cumulative-layout-shift'].numericValue.toFixed(3),
        lab_tbt_ms: Math.round(a['total-blocking-time'].numericValue),
        lab_fcp_s: +(a['first-contentful-paint'].numericValue / 1000).toFixed(2),
        lab_si_s: +(a['speed-index'].numericValue / 1000).toFixed(2),
        page_weight_kb: Math.round((a['total-byte-weight']?.numericValue || 0) / 1024),
        field_overall: j.loadingExperience?.overall_category || 'sin datos de campo (CrUX)',
        field_lcp_ms: field('LARGEST_CONTENTFUL_PAINT_MS'), field_inp_ms: field('INTERACTION_TO_NEXT_PAINT'),
        field_cls: fe.CUMULATIVE_LAYOUT_SHIFT_SCORE ? fe.CUMULATIVE_LAYOUT_SHIFT_SCORE.percentile / 100 : null,
        top_opportunities: Object.values(a)
          .filter((x) => x.details?.type === 'opportunity' && (x.details.overallSavingsMs || 0) > 150)
          .sort((x, y) => y.details.overallSavingsMs - x.details.overallSavingsMs)
          .slice(0, 5).map((x) => `${x.title} (~${Math.round(x.details.overallSavingsMs)} ms)`).join('; '),
      };
    } catch (e) {
      row.error = redact(e.message).slice(0, 300);
      if (old) row = { ...old, note: `re-run failed (${row.error.slice(0, 80)}); kept result from ${old.tested_at}` };
    }
    results.push(row);
    console.log(`${strategy.padEnd(7)} ${url} -> ${row.performance ?? 'ERROR'}${row.error ? ' ' + row.error.slice(0, 120) : ''}`);
    await sleep(KEY ? 1000 : 4000);
  }
}

const cols = ['url', 'strategy', 'performance', 'accessibility', 'best_practices', 'seo', 'lab_lcp_s', 'lab_cls', 'lab_tbt_ms', 'lab_fcp_s', 'lab_si_s', 'page_weight_kb', 'field_overall', 'field_lcp_ms', 'field_inp_ms', 'field_cls', 'top_opportunities', 'error', 'note', 'tested_at', 'with_key'];
writeFileSync(`${OUT}/pagespeed.csv`, '﻿' + [csvRow(cols), ...results.map((r) => csvRow(cols.map((c) => r[c])))].join('\n'));
writeFileSync(`${OUT}/pagespeed.json`, JSON.stringify({ results }, null, 2));
