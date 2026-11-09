// Screenshots Meta ad preview iframes. Usage: node screenshot_previews.mjs <jobs.json>
// jobs.json: [{"url": "...preview_iframe.php?...", "out": "/abs/path.png"}, ...]
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { execSync } from "node:child_process";

const require = createRequire(import.meta.url);
const { chromium } = require(`${execSync("npm root -g").toString().trim()}/playwright`);

const jobs = JSON.parse(readFileSync(process.argv[2], "utf8"));
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 540, height: 1400 }, deviceScaleFactor: 2 });
for (const job of jobs) {
  try {
    await page.goto(job.url, { waitUntil: "networkidle", timeout: 60000 });
    await page.waitForTimeout(1500);
    if (job.poster) {
      // The video cannot play here: put its cover frame where the player shows an error.
      await page.evaluate((src) => {
        const err = [...document.querySelectorAll("body *")].find(el =>
          el.children.length === 0 && /trouble playing/i.test(el.textContent));
        let box = err;
        while (box && box.getBoundingClientRect().height < 300) box = box.parentElement;
        if (box) box.innerHTML = `<img src="${src}" style="width:100%;height:100%;object-fit:cover;display:block">`;
      }, job.poster);
      await page.waitForLoadState("networkidle");
      await page.waitForTimeout(800);
    }
    // Crop to the whole ad card: the smallest block holding the media and the Like/Comment/Share bar.
    const box = await page.evaluate(() => {
      let best = null;
      for (const el of document.querySelectorAll("body *")) {
        const r = el.getBoundingClientRect();
        if (r.width < 300 || !el.querySelector("img, video") || !/Like/.test(el.innerText || "")) continue;
        if (!best || r.width * r.height < best.w * best.h) best = { x: r.x, y: r.y, w: r.width, h: r.height };
      }
      return best;
    });
    const clip = box ? { x: Math.max(0, box.x), y: Math.max(0, box.y), width: box.w, height: box.h } : undefined;
    await page.screenshot({ path: job.out, clip, fullPage: !clip });
    console.log("ok", job.out);
  } catch (e) {
    console.log("fail", job.out, String(e).slice(0, 200));
  }
}
await browser.close();
