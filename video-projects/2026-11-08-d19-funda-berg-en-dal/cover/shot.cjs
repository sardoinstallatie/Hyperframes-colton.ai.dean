const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: process.env.HYPERFRAMES_BROWSER_PATH || '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + __dirname + '/cover.html');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await p.screenshot({ path: __dirname + '/2026-11-08-D19-funda-berg-en-dal-cover.png' });
  await b.close();
})();
