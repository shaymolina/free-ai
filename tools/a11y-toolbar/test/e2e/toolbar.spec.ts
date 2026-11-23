import AxeBuilder from '@axe-core/playwright';
import { type Page, expect, test } from '@playwright/test';

const FIXTURE = '/__a11y-toolbar-fixture';

/** A small host page served only inside the tests, so no route is added to the site. */
function fixtureHtml(lang: 'he' | 'en'): string {
  const dir = lang === 'he' ? 'rtl' : 'ltr';
  return `<!doctype html><html lang="${lang}" dir="${dir}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Fixture</title>
<style>
  body { font: 16px/1.4 Georgia, serif; margin: 0; padding: 24px; }
  .big { font-size: 24px; }
  .spin { animation: spin 2s linear infinite; width: 20px; height: 20px; background: #c00; }
  .fade { transition: opacity 3s; }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>
<script src="/assets/js/a11y-toolbar.js" data-language="${lang}" async></script></head>
<body><main>
  <h1 id="h">Heading</h1>
  <p id="p">Plain paragraph text with several words in it.</p>
  <p class="big" id="big">Big text</p>
  <a id="link" href="#x">A link</a>
  <img id="img" alt="Cat" width="40" height="40" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40'/%3E">
  <a href="#y" id="img-link"><img id="img-in-link" alt="Logo" width="20" height="20" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20'/%3E"></a>
  <div class="spin" id="spin"></div><div class="fade" id="fade">fade</div>
  <input id="field" aria-label="Field"><button id="host-button" type="button">Host</button>
</main></body></html>`;
}

async function openFixture(page: Page, lang: 'he' | 'en' = 'en'): Promise<void> {
  await page.route(`**${FIXTURE}*`, (route) => route.fulfill({ contentType: 'text/html; charset=utf-8', body: fixtureHtml(lang) }));
  await page.goto(`${FIXTURE}?lang=${lang}`);
  await expect(page.locator('#a11y-toolbar-trigger')).toBeVisible();
}

const css = (page: Page, selector: string, prop: string): Promise<string> =>
  page.locator(selector).evaluate((el, p) => getComputedStyle(el).getPropertyValue(p), prop);

const control = (page: Page, name: string) => page.locator(`[data-a11y-toolbar-control="${name}"]`);

async function openPanel(page: Page): Promise<void> {
  await page.locator('#a11y-toolbar-trigger').click();
  await expect(page.locator('#a11y-panel')).toBeVisible();
  await page.locator('#a11y-panel').evaluate((el) => Promise.all(el.getAnimations().map((a) => a.finished)));
}

/** Contrast radios are visually hidden inputs; users click their visible labels. */
const pickContrast = (page: Page, mode: string) =>
  page.locator('label.a11y-toolbar-radio', { has: control(page, `contrast-${mode}`) }).click();

test.describe('floating button', () => {
  test('is a blue circle with a white icon, 56px on desktop', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await openFixture(page);
    const button = page.locator('#a11y-toolbar-trigger');
    await expect(button).toHaveAttribute('aria-label', 'Accessibility options');
    expect(await css(page, '#a11y-toolbar-trigger', 'background-color')).toBe('rgb(11, 127, 179)');
    expect(await css(page, '#a11y-toolbar-trigger svg', 'color')).toBe('rgb(255, 255, 255)');
    expect(await css(page, '#a11y-toolbar-trigger', 'border-radius')).toBe('9999px');
    const box = await button.boundingBox();
    expect(box?.width).toBe(56);
    expect(box?.height).toBe(56);
    expect(Math.round((box?.x ?? 0) + (box?.width ?? 0))).toBe(1280 - 16);
    expect(Math.round((box?.y ?? 0) + (box?.height ?? 0))).toBe(800 - 16);
    const icon = await page.locator('#a11y-toolbar-trigger svg').boundingBox();
    expect(icon?.width).toBe(28);
  });

  test('is 48px with a 24px icon on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 700 });
    await openFixture(page);
    const box = await page.locator('#a11y-toolbar-trigger').boundingBox();
    expect(box?.width).toBe(48);
    expect((await page.locator('#a11y-toolbar-trigger svg').boundingBox())?.width).toBe(24);
  });

  test('shows a visible focus ring from the keyboard', async ({ page }) => {
    await openFixture(page);
    await page.locator('#host-button').focus();
    await page.keyboard.press('Tab');
    await expect(page.locator('#a11y-toolbar-trigger')).toBeFocused();
    expect(await css(page, '#a11y-toolbar-trigger', 'outline-style')).toBe('solid');
    expect(await css(page, '#a11y-toolbar-trigger', 'outline-width')).toBe('3px');
  });
});

test.describe('keyboard', () => {
  test('Enter opens, focus moves to the title, Escape closes and returns focus', async ({ page }) => {
    await openFixture(page);
    await page.locator('#a11y-toolbar-trigger').focus();
    await page.keyboard.press('Enter');
    await expect(page.locator('#a11y-toolbar-trigger')).toHaveAttribute('aria-expanded', 'true');
    await expect(page.locator('#a11y-panel h2')).toBeFocused();
    await page.keyboard.press('Tab');
    await expect(control(page, 'close')).toBeFocused();
    await page.keyboard.press('Tab');
    await page.keyboard.press('Escape');
    await expect(page.locator('#a11y-panel')).toBeHidden();
    await expect(page.locator('#a11y-toolbar-trigger')).toBeFocused();
    await expect(page.locator('#a11y-toolbar-trigger')).toHaveAttribute('aria-expanded', 'false');
  });

  test('Space opens and activates toggles; radios follow arrow keys', async ({ page }) => {
    await openFixture(page);
    await page.locator('#a11y-toolbar-trigger').focus();
    await page.keyboard.press('Space');
    await expect(page.locator('#a11y-panel')).toBeVisible();
    await control(page, 'readableFont').focus();
    await page.keyboard.press('Space');
    await expect(control(page, 'readableFont')).toHaveAttribute('aria-pressed', 'true');
    await control(page, 'contrast-none').focus();
    await page.keyboard.press('ArrowDown');
    await expect(control(page, 'contrast-highContrast')).toBeChecked();
    expect(await page.evaluate(() => document.documentElement.hasAttribute('data-a11y-toolbar-high-contrast'))).toBe(true);
  });

  test('focus is not trapped: Tab leaves the panel to the page', async ({ page }) => {
    await openFixture(page);
    await openPanel(page);
    await control(page, 'reset').focus();
    await page.keyboard.press('Tab');
    const inside = await page.evaluate(() => document.activeElement?.closest('.a11y-toolbar-root') !== null);
    expect(inside).toBe(false);
  });
});

test.describe('visual preferences', () => {
  test('text size scales host text but not the toolbar', async ({ page }) => {
    await openFixture(page);
    await openPanel(page);
    const toolbarSize = await css(page, '.a11y-toolbar-title', 'font-size');
    for (let i = 0; i < 2; i += 1) await control(page, 'textScale-increase').click();
    await expect(page.locator('#p')).toHaveCSS('font-size', '19.2px');
    await expect(page.locator('#big')).toHaveCSS('font-size', '28.8px');
    expect(await css(page, '.a11y-toolbar-title', 'font-size')).toBe(toolbarSize);
    await control(page, 'textScale-decrease').click();
    await expect(page.locator('#p')).toHaveCSS('font-size', '17.6px');
    await control(page, 'textScale-reset').click();
    await expect(page.locator('#p')).toHaveCSS('font-size', '16px');
    expect(await page.evaluate(() => document.body.style.transform + document.documentElement.style.zoom)).toBe('');
  });

  test('readable font, spacing and line height', async ({ page }) => {
    await openFixture(page);
    await openPanel(page);
    await control(page, 'readableFont').click();
    expect(await css(page, '#p', 'font-family')).toContain('Arial');
    expect(await css(page, '.a11y-toolbar-title', 'font-family')).not.toMatch(/^Arial/);
    await control(page, 'letterSpacing-increase').click();
    await expect(page.locator('#p')).toHaveCSS('letter-spacing', '0.8px');
    await control(page, 'wordSpacing-increase').click();
    await expect(page.locator('#p')).toHaveCSS('word-spacing', '1.6px');
    await control(page, 'lineHeight-increase').click();
    await expect(page.locator('#p')).toHaveCSS('line-height', '24px');
  });

  test('contrast modes, invert and grayscale', async ({ page }) => {
    await openFixture(page);
    await openPanel(page);
    await pickContrast(page, 'darkContrast');
    await expect(page.locator('#p')).toHaveCSS('color', 'rgb(242, 242, 242)');
    await expect(page.locator('body')).toHaveCSS('background-color', 'rgb(18, 18, 18)');
    await pickContrast(page, 'lightContrast');
    await expect(page.locator('#p')).toHaveCSS('color', 'rgb(0, 0, 0)');
    await pickContrast(page, 'highContrast');
    await expect(page.locator('#link')).toHaveCSS('color', 'rgb(255, 235, 59)');
    // The toolbar keeps its own colors.
    await page.mouse.move(5, 5);
    await expect(page.locator('#a11y-toolbar-trigger')).toHaveCSS('background-color', 'rgb(11, 127, 179)');
    await expect(page.locator('.a11y-toolbar-toggle').first()).toHaveCSS('background-color', 'rgb(255, 255, 255)');
    await pickContrast(page, 'invertColors');
    await expect(page.locator('html')).toHaveCSS('filter', 'invert(1) hue-rotate(180deg)');
    await expect(page.locator('#img')).toHaveCSS('filter', 'invert(1) hue-rotate(180deg)');
    await expect(page.locator('.a11y-toolbar-root')).toHaveCSS('filter', 'invert(1) hue-rotate(180deg)');
    expect(await page.evaluate(() => document.documentElement.hasAttribute('data-a11y-toolbar-high-contrast'))).toBe(false);
    await control(page, 'grayscale').click();
    await expect(page.locator('#a11y-toolbar-grayscale-layer')).toHaveCSS('backdrop-filter', 'grayscale(1)');
    await control(page, 'grayscale').click();
    await expect(page.locator('#a11y-toolbar-grayscale-layer')).toHaveCount(0);
  });

  test('pause animations and reduce motion', async ({ page }) => {
    await openFixture(page);
    await openPanel(page);
    await control(page, 'pauseAnimations').click();
    await expect(page.locator('#spin')).toHaveCSS('animation-play-state', 'paused');
    await expect(page.locator('#fade')).toHaveCSS('transition-duration', '1e-05s');
    await control(page, 'pauseAnimations').click();
    await expect(page.locator('#spin')).toHaveCSS('animation-play-state', 'running');
    await control(page, 'reduceMotion').click();
    await expect(page.locator('#spin')).toHaveCSS('animation-iteration-count', '1');
    await expect(page.locator('#a11y-toolbar-trigger')).toHaveCSS('transition-duration', '0s');
  });

  test('link and heading highlighting', async ({ page }) => {
    await openFixture(page);
    await openPanel(page);
    await control(page, 'highlightLinks').click();
    await expect(page.locator('#link')).toHaveCSS('text-decoration-thickness', '3px');
    await control(page, 'highlightHeadings').click();
    await expect(page.locator('#h')).toHaveCSS('outline-style', 'dashed');
    await expect(page.locator('#h')).toHaveText('Heading');
  });

  test('reading guide follows the pointer and never blocks clicks', async ({ page }) => {
    await openFixture(page);
    await openPanel(page);
    await control(page, 'readingGuide').click();
    await control(page, 'close').click();
    const guide = page.locator('#a11y-toolbar-reading-guide');
    await expect(guide).toHaveAttribute('aria-hidden', 'true');
    await expect(guide).toHaveCSS('pointer-events', 'none');
    const link = await page.locator('#link').boundingBox();
    if (!link) throw new Error('no link');
    await page.mouse.move(link.x + 5, link.y + link.height / 2);
    await expect.poll(async () => Math.round((await guide.boundingBox())?.y ?? 0)).toBe(Math.round(link.y + link.height / 2 - 2));
    await page.mouse.click(link.x + 5, link.y + link.height / 2);
    await expect(page).toHaveURL(/#x$/);
  });

  test('reading mask darkens above and below the reading band', async ({ page }) => {
    await page.setViewportSize({ width: 1000, height: 800 });
    await openFixture(page);
    await openPanel(page);
    await control(page, 'readingMask').click();
    await page.mouse.move(100, 400);
    const top = page.locator('#a11y-toolbar-reading-mask-top');
    const bottom = page.locator('#a11y-toolbar-reading-mask-bottom');
    await expect.poll(async () => (await top.boundingBox())?.height).toBe(340);
    expect((await bottom.boundingBox())?.y).toBe(460);
    await expect(top).toHaveCSS('pointer-events', 'none');
  });

  test('large cursor keeps the text caret in fields', async ({ page }) => {
    await openFixture(page);
    await openPanel(page);
    await control(page, 'largeCursor').click();
    expect(await css(page, '#p', 'cursor')).toContain('url("data:image/svg+xml');
    expect(await css(page, '#link', 'cursor')).toContain('url("data:image/svg+xml');
    expect(await css(page, '#field', 'cursor')).not.toContain('url(');
  });

  test('focus highlight adds an outline to focused elements only', async ({ page }) => {
    await openFixture(page);
    await openPanel(page);
    await control(page, 'focusHighlight').click();
    await page.locator('#host-button').focus();
    await page.keyboard.press('Shift+Tab');
    await page.keyboard.press('Tab');
    await expect(page.locator('#host-button')).toHaveCSS('outline-width', '3px');
    expect(await css(page, '#p', 'outline-style')).toBe('none');
  });

  test('hide images keeps layout, alt text and images inside links', async ({ page }) => {
    await openFixture(page);
    await openPanel(page);
    const before = await page.locator('#img').boundingBox();
    await control(page, 'hideImages').click();
    await expect(page.locator('#img')).toHaveCSS('visibility', 'hidden');
    await expect(page.locator('#img')).toHaveAttribute('alt', 'Cat');
    await expect(page.locator('#img-in-link')).toHaveCSS('visibility', 'visible');
    expect(await page.locator('#img').boundingBox()).toEqual(before);
    await control(page, 'hideImages').click();
    await expect(page.locator('#img')).toHaveCSS('visibility', 'visible');
  });
});

test.describe('state', () => {
  test('persists after reload and resets everything', async ({ page }) => {
    await openFixture(page);
    await openPanel(page);
    await control(page, 'highlightLinks').click();
    await control(page, 'textScale-increase').click();
    await page.reload();
    await expect(page.locator('html')).toHaveAttribute('data-a11y-toolbar-highlight-links', '');
    await expect(page.locator('html')).toHaveAttribute('data-a11y-toolbar-text-scale', '1.1');
    await openPanel(page);
    await expect(control(page, 'highlightLinks')).toHaveAttribute('aria-pressed', 'true');
    await control(page, 'reset').click();
    await expect(control(page, 'reset')).toBeFocused();
    await expect(page.locator('#a11y-panel')).toBeVisible();
    await expect(page.locator('[role="status"]')).toHaveText('Settings have been reset');
    const leftovers = await page.evaluate(() => [
      ...Array.from(document.documentElement.attributes).map((a) => a.name).filter((n) => n.startsWith('data-a11y-toolbar')),
      ...(localStorage.getItem('a11y-toolbar-preferences-v1') ? ['storage'] : []),
      ...(document.getElementById('a11y-toolbar-text-scale-styles') ? ['scale-sheet'] : []),
    ]);
    expect(leftovers).toEqual([]);
  });

  test('synchronizes between tabs, including reset', async ({ context }) => {
    const a = await context.newPage();
    const b = await context.newPage();
    await openFixture(a);
    await openFixture(b);
    await openPanel(a);
    await control(a, 'hideImages').click();
    await expect(b.locator('html')).toHaveAttribute('data-a11y-toolbar-hide-images', '');
    await control(a, 'reset').click();
    await expect(b.locator('html')).not.toHaveAttribute('data-a11y-toolbar-hide-images', '');
  });

  test('works when localStorage and BroadcastChannel are unavailable', async ({ page }) => {
    await page.addInitScript(() => {
      Object.defineProperty(window, 'localStorage', { get() { throw new Error('blocked'); } });
      Object.defineProperty(window, 'BroadcastChannel', { value: undefined });
    });
    const errors: string[] = [];
    page.on('pageerror', (e) => errors.push(e.message));
    await openFixture(page);
    await openPanel(page);
    await control(page, 'readableFont').click();
    await expect(page.locator('html')).toHaveAttribute('data-a11y-toolbar-readable-font', '');
    expect(errors).toEqual([]);
  });
});

test.describe('layout and language', () => {
  test('Hebrew is RTL with Hebrew labels', async ({ page }) => {
    await openFixture(page, 'he');
    await expect(page.locator('#a11y-toolbar-trigger')).toHaveAttribute('aria-label', 'אפשרויות נגישות');
    await expect(page.locator('.a11y-toolbar-root')).toHaveAttribute('dir', 'rtl');
    await openPanel(page);
    await expect(page.locator('#a11y-panel h2')).toHaveText('תפריט נגישות');
    expect(await css(page, '#a11y-panel h2', 'direction')).toBe('rtl');
  });

  test('desktop popover opens above the button and stays inside the viewport', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await openFixture(page);
    await openPanel(page);
    const panel = await page.locator('#a11y-panel').boundingBox();
    const button = await page.locator('#a11y-toolbar-trigger').boundingBox();
    if (!panel || !button) throw new Error('missing');
    expect(panel.y + panel.height).toBeLessThanOrEqual(button.y);
    expect(panel.x + panel.width).toBeLessThanOrEqual(1280);
    expect(panel.y).toBeGreaterThanOrEqual(0);
    expect(panel.width).toBeLessThan(1280 / 2);
  });

  for (const width of [320, 375]) {
    test(`mobile bottom sheet at ${width}px has no horizontal scrolling`, async ({ page }) => {
      await page.setViewportSize({ width, height: 640 });
      await openFixture(page, 'he');
      await openPanel(page);
      await expect(page.locator('.a11y-toolbar-root')).toHaveAttribute('data-a11y-toolbar-layout', 'sheet');
      const panel = await page.locator('#a11y-panel').boundingBox();
      expect(panel?.x).toBe(0);
      expect(panel?.width).toBe(width);
      expect(Math.round((panel?.y ?? 0) + (panel?.height ?? 0))).toBe(640);
      const overflow = await page.locator('.a11y-toolbar-body').evaluate((el) => el.scrollWidth - el.clientWidth);
      expect(overflow).toBeLessThanOrEqual(0);
      await control(page, 'reset').scrollIntoViewIfNeeded();
      await expect(control(page, 'reset')).toBeInViewport();
    });
  }

  test('respects prefers-reduced-motion for the toolbar itself', async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await openFixture(page);
    await expect(page.locator('#a11y-toolbar-trigger')).toHaveCSS('transition-duration', '0s');
    await openPanel(page);
    await expect(page.locator('#a11y-panel')).toHaveCSS('animation-name', 'none');
  });
});

test.describe('accessibility of the toolbar', () => {
  for (const lang of ['he', 'en'] as const) {
    test(`axe finds no serious or critical violations inside the toolbar (${lang})`, async ({ page }) => {
      await openFixture(page, lang);
      await openPanel(page);
      await control(page, 'readableFont').click();
      const results = await new AxeBuilder({ page }).include('.a11y-toolbar-root').analyze();
      const serious = results.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical');
      expect(serious.map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(' ')).join(', ')}`)).toEqual([]);
    });
  }

  test('dark theme also passes axe', async ({ page }) => {
    await page.route(`**${FIXTURE}*`, (route) => route.fulfill({
      contentType: 'text/html; charset=utf-8',
      body: fixtureHtml('en').replace('data-language="en"', 'data-language="en" data-theme="dark"'),
    }));
    await page.goto(FIXTURE);
    await openPanel(page);
    const results = await new AxeBuilder({ page }).include('.a11y-toolbar-root').analyze();
    expect(results.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical')).toEqual([]);
  });

  test('contains no scanner, inspector, checker, audit, issues or score UI', async ({ page }) => {
    await openFixture(page);
    await openPanel(page);
    const text = (await page.locator('.a11y-toolbar-root').innerText()).toLowerCase();
    for (const word of ['scanner', 'inspector', 'checker', 'audit', 'issues', 'score', 'compliance', 'violation']) {
      expect(text).not.toContain(word);
    }
    await expect(page.locator('.a11y-toolbar-root [role="tab"]')).toHaveCount(0);
  });
});

test.describe('site integration', () => {
  for (const path of ['/', '/privacy', '/terms', '/articles', '/guide-1']) {
    test(`toolbar is present on ${path} without page errors`, async ({ page }) => {
      const errors: string[] = [];
      page.on('pageerror', (e) => errors.push(e.message));
      await page.goto(path);
      await expect(page.locator('#a11y-toolbar-trigger')).toBeVisible();
      await expect(page.locator('#a11y-toolbar-trigger')).toHaveAttribute('aria-label', 'אפשרויות נגישות');
      await page.locator('#a11y-toolbar-trigger').click();
      await expect(page.locator('#a11y-panel')).toBeVisible();
      expect(errors).toEqual([]);
    });
  }
});
