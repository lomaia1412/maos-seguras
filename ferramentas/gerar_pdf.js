// Gera cartaz.pdf (A4 retrato) a partir de cartaz.html usando Chromium headless (Playwright).
// Uso:  npm i -D playwright && npx playwright install chromium   (só na 1ª vez)
//       node ferramentas/gerar_pdf.js
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const raiz = path.resolve(__dirname, '..');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(raiz, 'cartaz.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: path.join(raiz, 'cartaz.pdf'),
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true, // usa @page { size: A4; margin: 8mm } definido no cartaz.html
  });
  await browser.close();
  console.log('ok: cartaz.pdf gerado');
})();
