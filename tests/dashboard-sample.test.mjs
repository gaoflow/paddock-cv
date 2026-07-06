// Regression suite for the public repo: runs against the FICTIONAL sample
// dataset (scripts/make_sample_data.py) and asserts structure, not real names.
//
//   python3 scripts/make_sample_data.py
//   F1E_DATA_DIR=data/sample python3 scripts/build_data.py
//   F1E_DATA_DIR=data/sample python3 scripts/seed_db.py
//   F1E_DATA_DIR=data/sample python3 server.py --port 8000 &
//   npm test
import { after, before, test } from "node:test";
import assert from "node:assert/strict";
import { chromium } from "playwright";

const BASE_URL = process.env.DASHBOARD_URL || "http://127.0.0.1:8000";

let browser;

before(async () => {
  browser = await launchBrowser();
});

after(async () => {
  await browser?.close();
});

test("health endpoint reports a seeded database", async () => {
  const health = await getJson("/api/health");
  assert.equal(health.ok, true);
  assert.ok(health.counts.series >= 1, "at least one series should be seeded");
  assert.ok(health.counts.teams >= 2, "teams should be seeded");
  assert.ok(health.counts.people >= 5, "people should be seeded");
  assert.ok(health.counts.assignments >= 5, "assignments should be seeded");
  assert.ok(health.counts.sources >= 1, "sources should be seeded");
});

test("roster board renders team cards and person rows", async () => {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  try {
    await page.goto(BASE_URL, { waitUntil: "domcontentloaded" });
    await page.locator(".personrow").first().waitFor();
    assert.ok(await page.locator("#rostersearch").isVisible(), "global search should be visible");
    assert.ok(await page.locator("#rosterboard .rostersection").count() >= 1, "at least one series section");
    assert.ok(await page.locator(".rosterteam").count() >= 2, "team cards should render");
    assert.ok(await page.locator(".personrow").count() >= 3, "person rows should render");
  } finally {
    await page.close();
  }
});

test("profile drawer opens from a person row and closes with Escape", async () => {
  const page = await browser.newPage({ viewport: { width: 1366, height: 900 } });
  try {
    await page.goto(BASE_URL, { waitUntil: "domcontentloaded" });
    const row = page.locator(".personrow").first();
    await row.waitFor();
    await row.scrollIntoViewIfNeeded();
    await row.click();
    await page.locator("#drawer.on").waitFor();
    assert.ok((await page.locator("#drawer").innerText()).length > 20, "drawer should show profile content");
    await page.keyboard.press("Escape");
    await page.locator("#drawer.on").waitFor({ state: "hidden" });
  } finally {
    await page.close();
  }
});

test("mobile layout does not overflow horizontally", async () => {
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  try {
    await page.goto(BASE_URL, { waitUntil: "domcontentloaded" });
    await page.locator(".personrow").first().waitFor();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    assert.ok(overflow <= 6, `mobile page should not horizontally overflow; got ${overflow}px`);
  } finally {
    await page.close();
  }
});

async function launchBrowser() {
  const channel = process.env.PLAYWRIGHT_CHANNEL || "chrome";
  try {
    return await chromium.launch({ channel, headless: true });
  } catch {
    return await chromium.launch({ headless: true });
  }
}

async function getJson(pathname) {
  const response = await fetch(new URL(pathname, BASE_URL));
  assert.ok(response.ok, `${pathname} returned HTTP ${response.status}`);
  return response.json();
}
