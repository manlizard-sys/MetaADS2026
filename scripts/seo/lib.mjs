// Shared helpers for the SEO audit scripts (no external dependencies; Node 18+).
export const UA = 'Mozilla/5.0 (compatible; OrchidSEOAudit/1.0)';

export function decode(s = '') {
  return s
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#0?39;|&apos;|&#8217;|&rsquo;/g, "'")
    .replace(/&#8216;|&lsquo;/g, "'")
    .replace(/&#8220;|&#8221;|&ldquo;|&rdquo;/g, '"')
    .replace(/&#8211;|&ndash;/g, '–')
    .replace(/&#8212;|&mdash;/g, '—')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)))
    .replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16)));
}

export const stripTags = (s = '') => decode(s.replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();

export function attr(tag, name) {
  const m = tag.match(new RegExp(`\\s${name}\\s*=\\s*("([^"]*)"|'([^']*)'|([^\\s>]+))`, 'i'));
  return m ? decode(m[2] ?? m[3] ?? m[4] ?? '') : null;
}

export function metaContent(html, key, by = 'name') {
  for (const tag of html.match(/<meta\b[^>]*>/gi) || []) {
    const v = attr(tag, by);
    if (v && v.toLowerCase() === key.toLowerCase()) return attr(tag, 'content');
  }
  return null;
}

export function removeBlocks(html, tags) {
  let out = html;
  for (const t of tags) out = out.replace(new RegExp(`<${t}\\b[\\s\\S]*?<\\/${t}>`, 'gi'), ' ');
  return out;
}

export function countWords(html) {
  const text = stripTags(removeBlocks(html, ['script', 'style', 'noscript', 'svg', 'template']));
  return text ? text.split(' ').filter((w) => /[A-Za-z0-9À-ÿ]/.test(w)).length : 0;
}

export function schemaTypes(html) {
  const types = new Set();
  const walk = (n) => {
    if (Array.isArray(n)) return n.forEach(walk);
    if (n && typeof n === 'object') {
      if (n['@type']) [].concat(n['@type']).forEach((t) => types.add(String(t)));
      Object.values(n).forEach(walk);
    }
  };
  let invalid = 0;
  for (const m of html.matchAll(/<script\b[^>]*type\s*=\s*["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)) {
    try { walk(JSON.parse(m[1])); } catch { invalid++; }
  }
  for (const m of html.matchAll(/itemtype\s*=\s*["']https?:\/\/schema\.org\/([A-Za-z]+)/gi)) types.add(`${m[1]} (microdata)`);
  return { types: [...types].sort(), invalid };
}

export function normalize(u, base) {
  try {
    const url = new URL(u, base);
    url.hash = '';
    if (url.pathname !== '/' && !url.pathname.endsWith('/') && !/\.[a-z0-9]{2,5}$/i.test(url.pathname)) url.pathname += '/';
    return url.toString();
  } catch { return null; }
}

export async function fetchChain(url, max = 10) {
  const chain = [];
  let cur = url;
  for (let i = 0; i < max; i++) {
    const t0 = Date.now();
    let res;
    try {
      res = await fetch(cur, { redirect: 'manual', headers: { 'User-Agent': UA, Accept: 'text/html,*/*' } });
    } catch (e) {
      chain.push({ url: cur, status: 'ERR', error: String(e.cause?.code || e.message) });
      return { chain, final: null };
    }
    const loc = res.headers.get('location');
    chain.push({ url: cur, status: res.status, ms: Date.now() - t0 });
    if (res.status >= 300 && res.status < 400 && loc) { cur = new URL(loc, cur).toString(); continue; }
    const body = await res.text();
    return { chain, final: { url: cur, status: res.status, headers: Object.fromEntries(res.headers), body } };
  }
  return { chain, final: null };
}

export function csvRow(values) {
  return values.map((v) => {
    const s = v == null ? '' : String(v);
    return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  }).join(',');
}

export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
