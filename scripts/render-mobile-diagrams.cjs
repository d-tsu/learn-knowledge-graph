const fs = require('fs');
const path = require('path');
const {chromium} = require('playwright');
(async () => {
 const root=path.resolve(__dirname,'..');fs.mkdirSync(path.join(root,'tmp/pdfs'),{recursive:true});
 const mermaidPath=process.argv[2];
 if(!mermaidPath) throw new Error('Pass the local Mermaid 11.12.0 UMD JavaScript path as the first argument.');
 const browser=await chromium.launch({channel:'msedge',headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1000,height:1500},deviceScaleFactor:3});
  await page.setContent('<html><meta charset="utf-8"><body style="margin:20px;background:white"></body></html>');
  await page.addScriptTag({path:mermaidPath});
  await page.evaluate(()=>mermaid.initialize({startOnLoad:false,theme:'base',themeVariables:{primaryColor:'#eef4ff',primaryBorderColor:'#7e9dc8',lineColor:'#536781',primaryTextColor:'#20364f',fontFamily:'Meiryo, sans-serif'},securityLevel:'strict'}));
  for(const f of fs.readdirSync(path.join(root,'docs/chapters')).filter(f=>f.endsWith('.md'))){
   const source=fs.readFileSync(path.join(root,'docs/chapters',f),'utf8');
   const diagrams=[...source.matchAll(/```mermaid\r?\n([\s\S]*?)```/g)];
   for(let i=0;i<diagrams.length;i++){
    const code=diagrams[i][1].replace('flowchart LR','flowchart TB');
    await page.evaluate(async({code,id})=>{const r=await mermaid.render(id,code);document.body.innerHTML=r.svg;},{code,id:'mobile'+f.slice(0,2)+i});
    const out=path.join(root,'tmp/pdfs',f.replace('.md','')+'-'+(i+1)+'.png');
    await page.locator('svg').screenshot({path:out});console.log(out);
   }
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
