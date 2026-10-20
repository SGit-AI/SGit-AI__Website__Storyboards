// The site in a real browser: https://storyboards.sgit.ai/ routed to www/, https://api.storyboards.sgit.ai/ routed to the
// API checkout ($STORYBOARDS_API, default ../SGit-AI__Website__Storyboards__API), so every page loads the kit from the
// pinned path with its integrity string exactly as it will live. Every page is opened; none may report an error; the
// pages that draw must draw. SHOTS=dir saves a screenshot of each page visited by name.
import { createRequire } from 'node:module';
import { readFileSync, existsSync, statSync, readdirSync, mkdirSync } from 'node:fs';
import { join, extname, dirname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';

const require = createRequire(import.meta.url);
const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const WWW = join(ROOT, 'www');
const API = process.env.STORYBOARDS_API || join(ROOT, '..', 'SGit-AI__Website__Storyboards__API');
const SITE = 'https://storyboards.sgit.ai';
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8',
  '.md': 'text/markdown; charset=utf-8', '.txt': 'text/plain; charset=utf-8', '.woff2': 'font/woff2', '.jpg': 'image/jpeg', '.xml': 'application/xml' };
async function playwright() {
  try { return await import('playwright'); } catch (e) { /* a global install */ }
  for (const p of [process.env.PLAYWRIGHT_PATH, '/opt/node22/lib/node_modules/playwright'].filter(Boolean)) if (existsSync(p)) return require(p);
  throw new Error('playwright is not installed: npm install --no-save playwright@1.56.1');
}
const serve = (dir) => (route) => {
  let path = decodeURIComponent(new URL(route.request().url()).pathname);
  if (path.endsWith('/')) path += 'index.html';
  const file = join(dir, path);
  if (!existsSync(file) || statSync(file).isDirectory()) return route.fulfill({ status: 404, body: 'not found' });
  return route.fulfill({ status: 200, body: readFileSync(file), headers: { 'content-type': TYPES[extname(file)] || 'application/octet-stream', 'access-control-allow-origin': '*' } });
};

const pw = await playwright();
const opts = existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome') && !process.env.CI ? { executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' } : {};
const browser = await pw[process.env.BROWSER || 'chromium'].launch(opts);
const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
await ctx.route(`${SITE}/**`, serve(WWW));
await ctx.route('https://api.storyboards.sgit.ai/**', serve(API));
await ctx.route(/^https:\/\/(?!(api\.)?storyboards\.sgit\.ai\/)/, (r) => r.fulfill({ status: 204, body: '' })); // nothing else is fetched
const shots = process.env.SHOTS;
if (shots) mkdirSync(shots, { recursive: true });
let n = 0;
async function visit(rel, check, name) {
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('requestfailed', (r) => errors.push('failed: ' + r.url()));
  await page.goto(`${SITE}/${rel}`);
  await page.waitForLoadState('networkidle');
  if (check) await check(page);
  if (shots && name) await page.screenshot({ path: join(shots, name + '.png'), fullPage: !!process.env.FULL });
  assert.deepEqual(errors, [], `${rel}: ${errors.join('; ')}`);
  await page.close();
  n++;
}
const pages = [];
(function walk(d) { for (const f of readdirSync(d)) { const p = join(d, f); if (statSync(p).isDirectory()) walk(p); else if (f.endsWith('.html')) pages.push(relative(WWW, p)); } })(WWW);
try {
  await visit('index.html', async (p) => {
    await p.waitForSelector('.hero-panel sg-storyboard figure svg g', { timeout: 15000 });
    assert.equal(await p.locator('.card').count(), 23);
  }, 'home');
  await visit('pki/the-first-key/index.html', async (p) => {
    await p.waitForSelector('.sb-deck .sb-slide svg g');
    assert.equal(await p.locator('.sb-deck .sb-slide').count(), 9);
    const [dl] = await Promise.all([p.waitForEvent('download'), p.click('button[data-export="svg"]')]);
    assert.match(dl.suggestedFilename(), /^the-first-key__01\.svg$/);
    const [png] = await Promise.all([p.waitForEvent('download'), p.click('button[data-export="png"]')]);
    assert.match(png.suggestedFilename(), /\.png$/);
  }, 'board-pki');
  await visit('gen-z-developers/everything-is-connected/index.html?view=grid', async (p) => {
    await p.waitForSelector('.sb-grid .sb-cell svg g');
  }, 'board-genz-grid');
  await visit('gen-z-developers/index.html', async (p) => { await p.waitForSelector('svg.sbx-lineup g'); }, 'series-genz');
  await visit('pki/index.html', async (p) => { await p.waitForSelector('svg.sbx-lineup g'); }, 'series-pki');
  await visit('pki/model-sheet.html', async (p) => { await p.waitForSelector('.sb-sheet figure svg g'); }, 'model-sheet-pki');
  for (const rel of pages.filter((r) => !['index.html', 'pki/the-first-key/index.html', 'gen-z-developers/index.html', 'pki/index.html', 'pki/model-sheet.html'].includes(r))) {
    await visit(rel, null, rel.startsWith('articles/') || rel.startsWith('embed') || rel.startsWith('abp') ? rel.replace(/\W+/g, '_') : null);
  }
} finally {
  await browser.close();
}
console.log(`test_site: ${n} pages opened, no errors`);
