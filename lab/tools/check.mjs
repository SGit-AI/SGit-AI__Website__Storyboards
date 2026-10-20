// Open one lab page in Chromium with https://api.storyboards.sgit.ai/ routed to the API checkout beside this repository
// (so the pinned release is served with the right headers) and report every page error, console error and third-party
// request; SHOT=path saves a screenshot. node lab/tools/check.mjs lab/stage/index.html [--wait 2500] [--click selector]
import { createRequire } from 'node:module';
import { readFileSync, existsSync, statSync } from 'node:fs';
import { join, extname, resolve } from 'node:path';
const require = createRequire(import.meta.url);
const pw = require('/opt/node22/lib/node_modules/playwright');
const ROOT = resolve(new URL('../..', import.meta.url).pathname);
const API = process.env.STORYBOARDS_API || join(ROOT, '..', 'SGit-AI__Website__Storyboards__API');
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.woff2': 'font/woff2', '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml' };
const serve = (dir) => (route) => {
  let p = decodeURIComponent(new URL(route.request().url()).pathname);
  if (p.endsWith('/')) p += 'index.html';
  // the built site first (www/ holds the generated lab index and twins), then the source tree
  const f = dir === ROOT && existsSync(join(dir, 'www', p)) && !statSync(join(dir, 'www', p)).isDirectory() ? join(dir, 'www', p) : join(dir, p);
  if (!existsSync(f) || statSync(f).isDirectory()) return route.fulfill({ status: 404, body: 'not found' });
  return route.fulfill({ status: 200, body: readFileSync(f), headers: { 'content-type': TYPES[extname(f)] || 'application/octet-stream', 'access-control-allow-origin': '*' } });
};
const args = process.argv.slice(2);
const rel = args[0];
const wait = args.includes('--wait') ? +args[args.indexOf('--wait') + 1] : 2500;
const click = args.includes('--click') ? args[args.indexOf('--click') + 1] : null;
const b = await pw.chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
await ctx.route('https://storyboards.sgit.ai/**', serve(ROOT));
await ctx.route('https://api.storyboards.sgit.ai/**', serve(API));
await ctx.route(/^https:\/\/(?!(api\.)?storyboards\.sgit\.ai\/)/, (r) => r.fulfill({ status: 204, body: '' }));
const page = await ctx.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push('pageerror: ' + e));
page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
page.on('request', (r) => { const h = new URL(r.url()).hostname; if (/^https?:/.test(r.url()) && !['api.storyboards.sgit.ai', 'storyboards.sgit.ai'].includes(h)) errors.push('third-party request: ' + r.url()); });
await page.goto('https://storyboards.sgit.ai/' + rel);
await page.waitForLoadState('networkidle');
await page.waitForTimeout(wait);
if (click) { await page.click(click); await page.waitForTimeout(1500); }
const strokes = await page.locator('svg path, canvas').count();
if (process.env.SHOT) await page.screenshot({ path: process.env.SHOT, fullPage: !!process.env.FULL });
await b.close();
const uniq = [...new Set(errors.map((e) => e.slice(0, 160)))];
console.log(`${rel}: ${strokes} svg paths/canvases; ${errors.length ? errors.length + ' ERRORS (' + uniq.length + ' distinct):\n  ' + uniq.slice(0, 12).join('\n  ') : 'no errors'}`);
process.exit(errors.length ? 1 : 0);
