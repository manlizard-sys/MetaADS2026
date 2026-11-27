// Technical SEO crawl of orchidpros.com (read only).
// Usage: node scripts/seo/crawl.mjs
// Output: seo/audit/crawl.json, seo/audit/urls.csv, seo/audit/links_not_in_sitemap.csv
import { mkdirSync, writeFileSync } from 'node:fs';
import { attr, countWords, csvRow, decode, fetchChain, metaContent, normalize, removeBlocks, schemaTypes, sleep, stripTags, UA } from './lib.mjs';

const SITE = 'https://orchidpros.com/';
const HOST = 'orchidpros.com';
const OUT = 'seo/audit';
mkdirSync(OUT, { recursive: true });

async function getText(url) {
  const r = await fetch(url, { headers: { 'User-Agent': UA } });
  return { status: r.status, text: await r.text(), headers: r.headers };
}

const locs = (xml) => [...xml.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)].map((m) => decode(m[1]));

// 1) Sitemap URLs
const index = await getText(`${SITE}sitemap_index.xml`);
const sitemaps = locs(index.text);
const sitemapUrls = new Map(); // url -> sitemap
for (const sm of sitemaps) {
  const x = await getText(sm);
  for (const u of locs(x.text)) sitemapUrls.set(normalize(u), sm.split('/').pop());
}

// 2) Published content from the public WP REST API
async function wpAll(type) {
  const out = [];
  for (let page = 1; page < 20; page++) {
    const r = await fetch(`${SITE}wp-json/wp/v2/${type}?per_page=100&page=${page}&_fields=id,link,slug,status,modified,title,parent`, { headers: { 'User-Agent': UA } });
    if (!r.ok) break;
    const arr = await r.json();
    out.push(...arr);
    if (arr.length < 100) break;
  }
  return out;
}
const wpPages = await wpAll('pages');
const wpPosts = await wpAll('posts');
const wpByUrl = new Map();
for (const p of wpPages) wpByUrl.set(normalize(p.link), { type: 'page', id: p.id, modified: p.modified, title: stripTags(p.title?.rendered || '') });
for (const p of wpPosts) wpByUrl.set(normalize(p.link), { type: 'post', id: p.id, modified: p.modified, title: stripTags(p.title?.rendered || '') });

// 3) Crawl every sitemap URL + every published WP URL
const targets = [...new Set([...sitemapUrls.keys(), ...wpByUrl.keys()])];
const results = [];
for (const url of targets) {
  const { chain, final } = await fetchChain(url);
  const row = {
    url,
    in_sitemap: sitemapUrls.has(url) ? sitemapUrls.get(url) : '',
    wp_type: wpByUrl.get(url)?.type || '',
    wp_modified: wpByUrl.get(url)?.modified || '',
    status: final?.status ?? chain.at(-1)?.status,
    redirect_chain: chain.length > 1 ? chain.map((c) => `${c.status} ${c.url}`).join(' -> ') : '',
    final_url: final?.url || '',
    response_ms: chain.at(-1)?.ms ?? '',
  };
  if (final && /text\/html/.test(final.headers['content-type'] || '')) {
    const html = final.body;
    const head = html.split(/<\/head>/i)[0];
    const canonTag = (head.match(/<link\b[^>]*rel\s*=\s*["']canonical["'][^>]*>/i) || [])[0];
    row.canonical = canonTag ? attr(canonTag, 'href') : '';
    row.canonical_self = row.canonical ? normalize(row.canonical) === normalize(final.url) : false;
    row.meta_robots = metaContent(head, 'robots') || '';
    row.x_robots_tag = final.headers['x-robots-tag'] || '';
    row.noindex = /noindex/i.test(row.meta_robots + ' ' + row.x_robots_tag);
    row.title = stripTags((head.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || '');
    row.title_len = row.title.length;
    row.meta_description = metaContent(head, 'description') || '';
    row.meta_description_len = row.meta_description.length;
    row.og_title = metaContent(head, 'og:title', 'property') || '';
    row.og_image = metaContent(head, 'og:image', 'property') ? 'yes' : 'no';
    row.lang = attr((html.match(/<html\b[^>]*>/i) || [''])[0], 'lang') || '';
    const body = html.slice(html.search(/<body\b/i));
    const h1s = [...body.matchAll(/<h1\b[^>]*>([\s\S]*?)<\/h1>/gi)].map((m) => stripTags(m[1])).filter(Boolean);
    row.h1_count = h1s.length;
    row.h1 = h1s.join(' | ');
    row.h2_count = (body.match(/<h2\b/gi) || []).length;
    // Main content = body minus the site header (first <header>…</header>) and the site footer.
    let main = body.replace(/<header\b[\s\S]*?<\/header>/i, ' ');
    main = main.replace(/<footer\b[\s\S]*<\/footer>/i, ' ');
    main = removeBlocks(main, ['nav']);
    row.word_count = countWords(body);
    row.word_count_main = countWords(main);
    const linksOf = (frag) => {
      const set = new Set();
      for (const m of frag.matchAll(/<a\b[^>]*>/gi)) {
        const href = attr(m[0], 'href');
        if (!href || /^(mailto:|tel:|javascript:|#)/i.test(href)) continue;
        const n = normalize(href, final.url);
        if (n && new URL(n).hostname.replace(/^www\./, '') === HOST && !/\/wp-content\/|\/wp-json\//.test(n)) set.add(n.split('?')[0]);
      }
      return set;
    };
    const allLinks = linksOf(body);
    const contentLinks = linksOf(main);
    allLinks.delete(url); contentLinks.delete(url);
    row._links_all = [...allLinks];
    row._links_content = [...contentLinks];
    row.internal_links_out = allLinks.size;
    row.internal_links_out_content = contentLinks.size;
    const ext = new Set();
    for (const m of body.matchAll(/<a\b[^>]*>/gi)) {
      const href = attr(m[0], 'href');
      try { const h = new URL(href, final.url).hostname; if (/^https?:/.test(new URL(href, final.url).protocol) && h.replace(/^www\./, '') !== HOST) ext.add(h); } catch {}
    }
    row.external_hosts = [...ext].sort().join(' ');
    const imgs = body.match(/<img\b[^>]*>/gi) || [];
    row.images = imgs.length;
    row.images_no_alt = imgs.filter((t) => attr(t, 'alt') === null).length;
    row.images_empty_alt = imgs.filter((t) => attr(t, 'alt') === '').length;
    row._img_missing = imgs.filter((t) => !attr(t, 'alt')).map((t) => attr(t, 'src') || attr(t, 'data-src') || '').slice(0, 30);
    const s = schemaTypes(html);
    row.schema_types = s.types.join(' ');
    row.schema_invalid_blocks = s.invalid;
    row.html_kb = Math.round(html.length / 1024);
  }
  results.push(row);
  await sleep(300);
}

// 4) Inbound links (all and from main content only)
const byUrl = new Map(results.map((r) => [r.url, r]));
for (const r of results) { r.inbound_links = 0; r.inbound_links_content = 0; }
for (const r of results) {
  for (const l of r._links_all || []) if (byUrl.has(l)) byUrl.get(l).inbound_links++;
  for (const l of r._links_content || []) if (byUrl.has(l)) byUrl.get(l).inbound_links_content++;
}

// 5) Internal links that point outside the crawled set (possible 404s / redirects / pages missing in sitemap)
const extra = new Map();
for (const r of results) for (const l of r._links_all || []) if (!byUrl.has(l)) {
  if (!extra.has(l)) extra.set(l, new Set());
  extra.get(l).add(r.url);
}
const extraRows = [];
for (const [l, from] of extra) {
  const { chain, final } = await fetchChain(l);
  const noindex = final?.body ? /noindex/i.test(metaContent(final.body.split(/<\/head>/i)[0], 'robots') || '') : '';
  extraRows.push({ url: l, status: final?.status ?? chain.at(-1)?.status, redirect_chain: chain.length > 1 ? chain.map((c) => `${c.status} ${c.url}`).join(' -> ') : '', noindex, linked_from: [...from].join(' ') });
  await sleep(200);
}

// 6) Site-level checks
const variants = ['http://orchidpros.com/', 'http://www.orchidpros.com/', 'https://www.orchidpros.com/', 'https://orchidpros.com/index.php', 'https://orchidpros.com/about', 'https://orchidpros.com/this-page-should-not-exist-xyz/'];
const siteChecks = [];
for (const v of variants) {
  const { chain, final } = await fetchChain(v);
  siteChecks.push({ url: v, chain: chain.map((c) => `${c.status} ${c.url}`).join(' -> '), final_status: final?.status ?? chain.at(-1)?.status });
}
const robots = await getText(`${SITE}robots.txt`);
const llms = await getText(`${SITE}llms.txt`).catch(() => ({ status: 'ERR' }));
const authorSitemap = await getText(`${SITE}author-sitemap.xml`).catch(() => ({ status: 'ERR' }));

// Write outputs
const cols = ['url', 'status', 'redirect_chain', 'in_sitemap', 'wp_type', 'wp_modified', 'canonical', 'canonical_self', 'meta_robots', 'x_robots_tag', 'noindex', 'title', 'title_len', 'meta_description', 'meta_description_len', 'og_image', 'lang', 'h1_count', 'h1', 'h2_count', 'word_count', 'word_count_main', 'internal_links_out', 'internal_links_out_content', 'inbound_links', 'inbound_links_content', 'images', 'images_no_alt', 'images_empty_alt', 'schema_types', 'schema_invalid_blocks', 'external_hosts', 'html_kb', 'response_ms'];
writeFileSync(`${OUT}/urls.csv`, '﻿' + [csvRow(cols), ...results.map((r) => csvRow(cols.map((c) => r[c])))].join('\n'));
const ecols = ['url', 'status', 'redirect_chain', 'noindex', 'linked_from'];
writeFileSync(`${OUT}/links_not_in_sitemap.csv`, '﻿' + [csvRow(ecols), ...extraRows.map((r) => csvRow(ecols.map((c) => r[c])))].join('\n'));
writeFileSync(`${OUT}/crawl.json`, JSON.stringify({
  crawled_at: new Date().toISOString(),
  sitemaps, sitemap_url_count: sitemapUrls.size,
  wp_pages: wpPages.length, wp_posts: wpPosts.length,
  wp_published_not_in_sitemap: [...wpByUrl.keys()].filter((u) => !sitemapUrls.has(u)),
  sitemap_not_in_wp: [...sitemapUrls.keys()].filter((u) => !wpByUrl.has(u)),
  robots_txt: robots.text, llms_txt_status: llms.status, author_sitemap_status: authorSitemap.status,
  site_checks: siteChecks, pages: results, links_not_in_sitemap: extraRows,
}, null, 2));
console.log(`Crawled ${results.length} URLs (${sitemapUrls.size} in sitemap, ${wpPages.length} WP pages, ${wpPosts.length} posts); ${extraRows.length} linked URLs outside the set.`);
