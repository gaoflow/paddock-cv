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

test("sample build exposes the expanded F1 role taxonomy", async () => {
  const data = await getJson("/data.json");
  const roles = data.f1_team_engineering?.role_templates || [];
  assert.equal(roles.length, 26, "the public sample should expose all 26 normalized F1 role families");
  assert.ok(roles.some((role) => role.key === "vehicle-dynamics-engineer"));
  assert.ok(roles.some((role) => role.key === "reliability-validation-engineer"));
  assert.ok(roles.some((role) => role.key === "tyre-modelling-engineer"));
  const alex = data.engineers.find((engineer) => engineer.id === "alex-example");
  assert.equal(alex.birth_year, 1990, "profiles should retain their sourced birth year");
  assert.equal(alex.age, new Date().getFullYear() - 1990, "age should be rebuilt from the current year");
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
    assert.equal(await page.locator("#drawer").getAttribute("role"), "dialog");
    assert.equal(await page.locator("#drawer").getAttribute("aria-modal"), "true");
    assert.equal(await page.locator("#drawer").getAttribute("aria-hidden"), "false");
    assert.equal(await page.locator("#dclose").evaluate((el) => el === document.activeElement), true);
    assert.equal(await page.locator("body").evaluate((el) => getComputedStyle(el).overflow), "hidden");
    assert.equal(await page.locator("header.top").evaluate((el) => el.inert), true);
    await page.keyboard.press("Shift+Tab");
    assert.equal(await page.locator("#drawer").evaluate((el) => el.contains(document.activeElement)), true);
    assert.ok((await page.locator("#drawer").innerText()).length > 20, "drawer should show profile content");
    assert.equal(await page.locator("#drawer .chips").count(), 0, "profile fact tags should not render");
    assert.equal(
      await page.locator("#drawer .sec .lab", { hasText: "Entry route" }).count(),
      0,
      "entry-route analysis should not be repeated in person details"
    );
    await page.keyboard.press("Escape");
    await page.locator("#drawer.on").waitFor({ state: "hidden" });
    assert.equal(await page.locator("#drawer").getAttribute("aria-hidden"), "true");
    assert.equal(await page.locator("header.top").evaluate((el) => el.inert), false);
    assert.equal(await row.evaluate((el) => el === document.activeElement), true);
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
    const row = page.locator(".personrow").first();
    await row.click();
    await page.locator("#drawer.on").waitFor();
    const modalBox = await page.locator("#drawer.on").boundingBox();
    assert.ok(modalBox, "mobile profile modal should have a layout box");
    assert.ok(modalBox.x >= 7 && modalBox.y >= 7, "mobile profile modal should retain viewport margins");
    assert.ok(modalBox.width <= 376 && modalBox.height <= 828, "mobile profile modal should fit inside the viewport");
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
