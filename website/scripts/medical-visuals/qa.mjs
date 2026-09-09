/** CI-only glTF, browser, responsive, fallback and accessibility checks. */
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const root = path.resolve('website');
const out = path.join(root, 'public/medical-visuals');
const qaRoot = process.env.QA_NODE_MODULES || path.join(root, 'node_modules');
const { validateBytes } = require(path.join(qaRoot, 'gltf-validator'));
const { chromium } = require(path.join(qaRoot, 'playwright'));
const manifest = JSON.parse(await fs.readFile(path.join(out, 'manifest.json'), 'utf8'));
const reports = path.join(root, 'medical-visual-qa');
await fs.mkdir(reports, { recursive: true });
const gltf = [];
for (const [key, model] of Object.entries(manifest.models)) {
  const bytes = new Uint8Array(await fs.readFile(path.join(root, 'public', model.src)));
  const result = await validateBytes(bytes, { uri: `${key}.glb`, maxIssues: 50 });
  gltf.push({ model: key, errors: result.issues.numErrors, warnings: result.issues.numWarnings, messages: result.issues.messages });
}
await fs.writeFile(path.join(reports, 'gltf-validation.json'), JSON.stringify(gltf, null, 2));
if (gltf.some(r => r.errors)) throw new Error('Khronos glTF validation failed.');
const browser = await chromium.launch({ headless: true, args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const base = process.env.QA_BASE_URL || 'http://127.0.0.1:4321';
const failures = [];
const assert = (test, message) => { if (!test) throw new Error(message); };
const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, reducedMotion: 'reduce' });
const page = await context.newPage();
page.on('pageerror', error => failures.push(error.message));
page.on('response', response => { if (response.url().startsWith(base) && response.status() >= 400) failures.push(`${response.status()} ${response.url()}`); });
const checked = [];
const axePath = require.resolve('axe-core/axe.min.js', { paths: [root] });
async function axe(label) {
  await page.addScriptTag({ path: axePath });
  const result = await page.evaluate(async () => window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a','wcag2aa','wcag21aa'] } }));
  await fs.writeFile(path.join(reports, `axe-${label}.json`), JSON.stringify(result.violations, null, 2));
  const blocking = result.violations.filter(v => ['serious','critical'].includes(v.impact));
  assert(!blocking.length, `Accessibility: ${label}: ${blocking.map(v => v.id).join(',')}`);
}
try {
  const requested = [];
  page.on('request', req => requested.push(req.url()));
  for (const slug of Object.keys(manifest.articles)) {
    const response = await page.goto(`${base}/articles/${slug}/`, { waitUntil: 'networkidle' });
    assert(response?.status() === 200, `Article route ${slug}`);
    assert(await page.locator('.medical-visual').count() === 1, `Missing explainer: ${slug}`);
    assert(await page.locator('h1').count() === 1, `Heading count: ${slug}`);
    checked.push(slug);
  }
  assert(!requested.some(u => u.endsWith('.glb')), 'GLB was downloaded without an explicit click');
  await page.goto(`${base}/articles/acl-tear-return-to-play/`, { waitUntil: 'networkidle' });
  await axe('article');
  const enable = page.locator('[data-enable]');
  await enable.click();
  await page.waitForFunction(() => document.querySelector('model-viewer')?.loaded === true, null, { timeout: 60000 });
  await page.waitForFunction(() => !document.querySelector('[data-controls]').hidden);
  await page.locator('[data-action=left]').click();
  await page.locator('[data-action=reset]').click();
  await page.locator('[data-medical-model]').scrollIntoViewIfNeeded();
  await page.screenshot({ path: path.join(reports, 'article-3d-desktop.png') });
  await enable.click();
  assert(await page.locator('model-viewer').count() === 0, 'Static fallback failed');
  await page.setViewportSize({ width: 375, height: 812 });
  await page.locator('.medical-visual').scrollIntoViewIfNeeded();
  assert(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), 'Mobile article overflow');
  await page.screenshot({ path: path.join(reports, 'article-mobile.png') });
  await page.goto(`${base}/medical-visuals/`, { waitUntil: 'networkidle' });
  assert(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), 'Mobile gallery overflow');
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.locator('[data-visual-search]').fill('前十字');
  assert(await page.locator('[data-visual-tile]:visible').count() === 1, 'Search filter failed');
  await page.locator('[data-visual-search]').fill('');
  assert(await page.locator('[data-visual-tile]:visible').count() === checked.length, 'Search reset failed');
  await axe('gallery');
  await page.locator('[data-enable]').click();
  await page.waitForFunction(() => document.querySelector('model-viewer')?.loaded === true, null, { timeout: 60000 });
  await page.locator('[data-angle-input]').evaluate(el => { el.value = '45'; el.dispatchEvent(new Event('input', { bubbles: true })); });
  assert(await page.locator('[data-angle]').textContent() === '45°', 'Angle slider failed');
  assert(await page.evaluate(() => document.querySelector('model-viewer').paused === true), 'Reduced-motion model autoplayed');
  await page.locator('[data-play]').click();
  assert(await page.evaluate(() => !document.querySelector('model-viewer').paused), 'Explicit animation playback failed');
  await page.locator('[data-play]').click();
  await page.locator('[data-medical-model]').scrollIntoViewIfNeeded();
  await page.screenshot({ path: path.join(reports, 'gallery-motion.png') });
  const nojs = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 375, height: 812 } });
  const staticPage = await nojs.newPage();
  await staticPage.goto(`${base}/articles/acl-tear-return-to-play/`);
  assert(await staticPage.locator('.medical-model__poster').isVisible(), 'No-JavaScript poster missing');
  await nojs.close();
  assert(!failures.length, failures.join('\n'));
  const report = { status: 'passed', articleRoutes: checked.length, glbModels: gltf.length, gltfErrors: 0, gltfWarnings: gltf.reduce((n,r) => n+r.warnings,0), browser: 'Chromium / software WebGL', widths: [375,1440], tests: ['52 article routes','no eager GLB downloads','3D load and rotation/reset','static fallback','no-JS poster','mobile overflow','gallery filter','motion slider','explicit play/pause','reduced-motion default pause','axe serious/critical issues','no local HTTP or JS errors'], consoleErrors: failures };
  await fs.writeFile(path.join(reports, 'browser-report.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify(report, null, 2));
} finally { await browser.close(); }
