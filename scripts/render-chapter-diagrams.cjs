// Render selected chapter diagrams without generating PDFs.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const {chromium} = require('playwright');
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
(async () => {
  const [mermaidPath, outputPath, ...inputs] = process.argv.slice(2);
  if (!mermaidPath || !outputPath || !inputs.length) throw new Error('Usage: node render-chapter-diagrams.cjs mermaid.min.js output-dir chapter.md [...]');
  fs.mkdirSync(outputPath, {recursive:true});
  const browser = await chromium.launch({channel:'msedge', headless:true});
  const report = [];
  try {
    const page = await browser.newPage({viewport:{width:1200,height:1000}, deviceScaleFactor:1});
    await page.setContent('<html><meta charset="utf-8"><body style="margin:20px;background:white"></body></html>');
    await page.addScriptTag({path:mermaidPath});
    await page.evaluate(() => mermaid.initialize({startOnLoad:false, securityLevel:'strict', theme:'base', themeVariables:{fontFamily:'Meiryo, sans-serif',primaryColor:'#eef4ff',primaryTextColor:'#20364f',lineColor:'#536781'}}));
    for (const input of inputs) {
      const bytes = fs.readFileSync(input);
      const diagrams = [...bytes.toString('utf8').matchAll(/```mermaid\r?\n([\s\S]*?)```/g)];
      const item = {file:input,sha256:hash(bytes),diagrams:[]};
      for (let i=0; i<diagrams.length; i++) {
        const code=diagrams[i][1], stem=path.basename(input,'.md')+'-'+(i+1);
        const svg=await page.evaluate(async ({code,id})=>{const result=await mermaid.render(id,code);document.body.innerHTML=result.svg;return result.svg;},{code,id:'diagram'+report.length+'n'+i});
        fs.writeFileSync(path.join(outputPath,stem+'.svg'),svg);
        await page.locator('svg').screenshot({path:path.join(outputPath,stem+'.png')});
        item.diagrams.push({codeSha256:hash(code),svg:stem+'.svg',png:stem+'.png'});
      }
      report.push(item);
    }
  } finally { await browser.close(); }
  fs.writeFileSync(path.join(outputPath,'render-check.json'),JSON.stringify({renderer:'Edge headless',mermaid:'11.12.0',files:report},null,2)+'\n');
  console.log(JSON.stringify(report.map(item=>({file:item.file,diagrams:item.diagrams.length}))));
})().catch(error=>{console.error(error);process.exitCode=1;});
