// Checks that search and AI crawlers get the same page as a browser (user-agent test, read only).
// Limit: it cannot detect blocks by IP range (some firewalls verify the real crawler IP); for that use the
// live URL tests in Google Search Console and Bing Webmaster Tools.
// Usage: node scripts/seo/bot_access.mjs   Output: seo/audit/bot_access.csv
import { mkdirSync, writeFileSync } from 'node:fs';
import { csvRow } from './lib.mjs';

const URLS = ['https://orchidpros.com/', 'https://orchidpros.com/solutions/healthcare/', 'https://orchidpros.com/robots.txt', 'https://orchidpros.com/llms.txt'];
const AGENTS = {
  browser: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36',
  Googlebot: 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
  Bingbot: 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) Chrome/131.0 Safari/537.36',
  'OAI-SearchBot': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot',
  'ChatGPT-User': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot',
  GPTBot: 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.1; +https://openai.com/gptbot',
  PerplexityBot: 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)',
  ClaudeBot: 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)',
};

const rows = [];
for (const url of URLS) {
  let base = null;
  for (const [name, ua] of Object.entries(AGENTS)) {
    try {
      const r = await fetch(url, { headers: { 'User-Agent': ua }, redirect: 'manual' });
      const body = await r.text();
      const title = (body.match(/<title[^>]*>([^<]*)/i) || [])[1] || '';
      if (name === 'browser') base = body.length;
      const same = base ? Math.abs(body.length - base) / base < 0.05 : '';
      rows.push({ url, agent: name, status: r.status, bytes: body.length, same_as_browser: same, title: title.trim().slice(0, 70) });
    } catch (e) {
      rows.push({ url, agent: name, status: 'ERR', bytes: 0, same_as_browser: false, title: String(e.message).slice(0, 70) });
    }
  }
}
mkdirSync('seo/audit', { recursive: true });
const cols = ['url', 'agent', 'status', 'bytes', 'same_as_browser', 'title'];
writeFileSync('seo/audit/bot_access.csv', '﻿' + [csvRow(cols), ...rows.map((r) => csvRow(cols.map((c) => r[c])))].join('\n'));
const bad = rows.filter((r) => r.status !== 200 || r.same_as_browser === false);
console.log(`${rows.length} checks, ${bad.length} different from the browser`);
bad.forEach((r) => console.log(`  ${r.agent} ${r.url} -> ${r.status} (${r.bytes} bytes)`));
