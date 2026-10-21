// Run after build-book.py. Requires Playwright and an installed Edge browser.
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '../tmp/book');
const evidence = path.resolve(__dirname, '../tmp/book-browser');
const prefix = '/learn-knowledge-graph/';
const mime = {'.html':'text/html; charset=utf-8', '.js':'text/javascript',
  '.css':'text/css', '.svg':'image/svg+xml', '.woff2':'font/woff2', '.png':'image/png'};

(async () => {
  fs.mkdirSync(evidence, {recursive:true});
  const server = http.createServer((req, res) => {
    const url = new URL(req.url, 'http://localhost');
    if (!url.pathname.startsWith(prefix)) { res.writeHead(404).end(); return; }
    let file = path.resolve(root, decodeURIComponent(url.pathname.slice(prefix.length)) || 'index.html');
    if (!file.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    if (!fs.existsSync(file)) { res.writeHead(404).end(); return; }
    res.writeHead(200, {'Content-Type':mime[path.extname(file)] || 'application/octet-stream'});
    fs.createReadStream(file).pipe(res);
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = process.env.BOOK_BASE_URL || `http://127.0.0.1:${server.address().port}${prefix}`;
  let browser;
  const failures = [];
  const pages = [];
  const search = [];
  try {
    browser = await chromium.launch({channel:'msedge', headless:true});
    const page = await browser.newPage({viewport:{width:1365, height:950}});
    page.on('pageerror', error => failures.push(String(error)));
    page.on('console', message => { if (message.type() === 'error') failures.push(message.text()); });
    const summary = fs.readFileSync(path.resolve(__dirname, '../tmp/book-src/SUMMARY.md'), 'utf8');
    const paths = [...summary.matchAll(/\]\(([^)]+)\.md\)/g)].map(m => m[1] + '.html');
    for (const name of paths) {
      const response = await page.goto(base + name);
      if (!response.ok()) throw new Error(`${name}: HTTP ${response.status()}`);
      await page.waitForFunction(() => [...document.querySelectorAll('.mermaid')]
        .every(element => element.querySelector('svg')));
      const count = await page.locator('.mermaid svg').count();
      pages.push({path:name, diagrams:count});
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 2);
      if (overflow) failures.push(`${name}: desktop body overflow`);
    }

    await page.goto(base + 'docs/chapters/04-ontologies.html');
    await page.waitForSelector('.mermaid svg');
    await page.screenshot({path:path.join(evidence, 'desktop.png')});
    await page.locator('.mermaid').first().screenshot({path:path.join(evidence, 'diagram.png')});
    await page.locator('#mdbook-theme-toggle').click();
    await page.locator('#mdbook-theme-navy').click();
    await page.waitForFunction(() => document.documentElement.classList.contains('navy'));
    await page.waitForTimeout(600);
    await page.screenshot({path:path.join(evidence, 'dark.png')});

    for (const query of ['オントロジー', '借り手', 'トレーサビリティ', 'SHACL']) {
      await page.goto(base + '?search=' + encodeURIComponent(query));
      await page.waitForFunction(() => {
        const text = document.querySelector('#mdbook-searchresults-header').textContent;
        return text.length > 0 && text !== '検索中…';
      });
      const count = await page.locator('#mdbook-searchresults li').count();
      search.push({query, results:count});
      if (!count) failures.push(`No search results: ${query}`);
    }
    await page.screenshot({path:path.join(evidence, 'search.png')});
    await page.locator('#mdbook-searchbar').fill('ナレッジグラフ オントロジー');
    await page.waitForFunction(() => document.querySelector('#mdbook-searchresults-header').textContent.includes('「ナレッジグラフ オントロジー」'));
    if (!await page.locator('#mdbook-searchresults li').count()) failures.push('Multiple-term search returned no results');
    await page.locator('#mdbook-searchbar').fill('存在しない検索語qzx123');
    await page.waitForFunction(() => document.querySelector('#mdbook-searchresults-header').textContent.includes('見つかりませんでした'));
    if (await page.locator('#mdbook-searchresults li').count()) failures.push('Unexpected search results');
    await page.locator('#mdbook-searchbar').fill('オントロジー');
    await page.waitForFunction(() => document.querySelector('#mdbook-searchresults-header').textContent.startsWith('「オントロジー」'));
    await page.locator('#mdbook-searchresults li a').first().click();
    await page.waitForLoadState('domcontentloaded');
    if (!await page.locator(':target').count()) failures.push('Search result did not reach its heading');
    await page.keyboard.press('/');
    if (!await page.locator('#mdbook-searchbar').evaluate(el => document.activeElement === el)) failures.push('Search keyboard shortcut failed');
    await page.keyboard.press('Escape');
    if (!await page.locator('#mdbook-search-wrapper').evaluate(el => el.classList.contains('hidden'))) failures.push('Search Escape shortcut failed');

    await page.setViewportSize({width:390,height:844});
    await page.goto(base + 'docs/chapters/03-knowledge-graphs.html');
    await page.waitForSelector('.mermaid svg');
    await page.screenshot({path:path.join(evidence, 'mobile.png')});
    await page.locator('.mermaid').first().scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(evidence, 'mobile-diagram.png')});
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 2);
    if (overflow) failures.push('Mobile body overflow');
    await page.locator('#mdbook-sidebar-toggle').click();
    await page.screenshot({path:path.join(evidence, 'mobile-menu.png')});
    await page.locator('.sidebar a[href$="04-ontologies.html"]').click();
    await page.waitForURL('**/04-ontologies.html');
    const report = {base, browser:'Microsoft Edge via Playwright', viewport:{desktop:[1365,950],mobile:[390,844]},
      pages, search, failures};
    fs.writeFileSync(path.join(evidence,'report.json'),JSON.stringify(report,null,2)+'\n');
    console.log(JSON.stringify({pages:pages.length, diagrams:pages.reduce((n,p)=>n+p.diagrams,0), search, failures},null,2));
    if (failures.length) process.exitCode = 1;
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
