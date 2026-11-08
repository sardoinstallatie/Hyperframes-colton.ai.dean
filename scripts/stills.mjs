#!/usr/bin/env node
// Snelle stills van een Hyperframes-compositie zonder volledige render.
// Gebruik: node ../../scripts/stills.mjs <projectdir> <t1> <t2> ... [--out work/stills]
// Laadt index.html via een lokale static server, seekt de GSAP-timeline (window.__timelines)
// én elke <video> naar het juiste moment en maakt een 1080×1920 screenshot per tijdstip.
import { chromium } from "playwright";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";

const args = process.argv.slice(2);
const dir = path.resolve(args[0]);
let out = path.join(dir, "work", "stills");
const times = [];
for (let i = 1; i < args.length; i++) {
  if (args[i] === "--out") { out = path.resolve(args[++i]); continue; }
  times.push(parseFloat(args[i]));
}
fs.mkdirSync(out, { recursive: true });

const mime = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".mp4": "video/mp4",
  ".png": "image/png", ".jpg": "image/jpeg", ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf", ".json": "application/json" };
const server = http.createServer((req, res) => {
  const p = path.join(dir, decodeURIComponent(req.url.split("?")[0]));
  if (!p.startsWith(dir) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  const stat = fs.statSync(p); const type = mime[path.extname(p)] || "application/octet-stream";
  const range = req.headers.range;
  if (range) {
    const [s, e] = range.replace("bytes=", "").split("-"); const start = +s; const end = e ? +e : stat.size - 1;
    res.writeHead(206, { "Content-Range": `bytes ${start}-${end}/${stat.size}`, "Accept-Ranges": "bytes", "Content-Length": end - start + 1, "Content-Type": type });
    fs.createReadStream(p, { start, end }).pipe(res);
  } else { res.writeHead(200, { "Content-Length": stat.size, "Content-Type": type, "Accept-Ranges": "bytes" }); fs.createReadStream(p).pipe(res); }
});
await new Promise((r) => server.listen(0, r));
const port = server.address().port;

const exe = process.env.HYPERFRAMES_BROWSER_PATH;
const browser = await chromium.launch({ executablePath: exe || undefined, args: ["--autoplay-policy=no-user-gesture-required", "--mute-audio"] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.on("pageerror", (e) => console.error("pageerror:", e.message));
await page.goto(`http://127.0.0.1:${port}/index.html`, { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
await page.waitForFunction(() => window.__timelines && Object.keys(window.__timelines).length > 0);

for (const t of times) {
  await page.evaluate(async (t) => {
    for (const tl of Object.values(window.__timelines)) tl.pause().seek(t, false);
    const media = [...document.querySelectorAll("video")];
    await Promise.all(media.map((v) => new Promise((res) => {
      const start = parseFloat(v.dataset.start || "0"); const dur = parseFloat(v.dataset.duration || "1e9");
      const local = t - start;
      if (local < 0 || local > dur) { v.style.visibility = "hidden"; return res(); }
      v.style.visibility = "";
      const done = () => { v.removeEventListener("seeked", done); res(); };
      v.addEventListener("seeked", done);
      if (v.readyState < 1) v.addEventListener("loadedmetadata", () => { v.currentTime = local; }, { once: true });
      else v.currentTime = local;
      setTimeout(res, 4000);
    })));
  }, t);
  await page.waitForTimeout(150);
  const file = path.join(out, `still-${t.toFixed(2).replace(".", "_")}.png`);
  await page.screenshot({ path: file });
  console.log(file);
}
await browser.close(); server.close();
