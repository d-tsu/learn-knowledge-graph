// Check links, code fences, and emphasis in the published chapters.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const {pathToFileURL} = require('url');
(async () => {
 const {marked} = await import(pathToFileURL(require.resolve('marked')).href);
 const root=path.resolve(__dirname,'..');
 const report=[];
 for(const name of fs.readdirSync(path.join(root,'docs/chapters')).filter(n=>n.endsWith('.md'))){
  const file=path.join(root,'docs/chapters',name);
  const bytes=fs.readFileSync(file), source=bytes.toString('utf8');
  const html=marked.parse(source,{gfm:true});
  const issues=[];
  const fences=[...source.matchAll(/^```/gm)].length;
  if(fences%2) issues.push('Unclosed code fence');
  const boldSource=[...source.matchAll(/\*\*([^*]+)\*\*/g)].map(m=>m[1]);
  const boldHtml=[...html.matchAll(/<strong>(.*?)<\/strong>/g)].map(m=>m[1]);
  if(JSON.stringify(boldSource)!==JSON.stringify(boldHtml)) issues.push('Emphasis was not parsed as intended');
  let localLinks=0;
  for(const m of source.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)){
   if(/^[a-z]+:/i.test(m[1]) || m[1].startsWith('#')) continue;
   localLinks++;
   if(!fs.existsSync(path.resolve(path.dirname(file),m[1].split('#')[0]))) issues.push('Missing link: '+m[1]);
  }
  report.push({file:'docs/chapters/'+name,sha256:crypto.createHash('sha256').update(bytes).digest('hex'),localLinks,emphasis:boldHtml.length,diagrams:[...source.matchAll(/```mermaid/g)].length,issues});
 }
 if(process.argv[2]) fs.writeFileSync(process.argv[2],JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify(report,null,2));
 if(report.some(r=>r.issues.length)) process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
