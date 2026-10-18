// Screenshot an animated SVG at chosen seconds of its SMIL clock.
// usage: node snap.cjs <file.svg> <out-prefix> <t1> [t2 ...]   → <out-prefix>-<t>.png
// Playwright comes from PLAYWRIGHT (a path to node_modules/playwright) or the normal resolution.
const path = require('path');
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
(async () => {
  const [file, out, ...times] = process.argv.slice(2);
  if (!file || !out || !times.length) {
    console.error('usage: node snap.cjs <file.svg> <out-prefix> <t1> [t2 ...]');
    process.exit(2);
  }
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--disable-gpu'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  await p.goto('file://' + path.resolve(file));
  for (const t of times) {
    await p.evaluate((t) => { const s = document.documentElement; s.pauseAnimations(); s.setCurrentTime(+t); }, t);
    await p.waitForTimeout(150);
    await (await p.$('svg')).screenshot({ path: `${out}-${t}.png` });
  }
  await b.close();
})();
