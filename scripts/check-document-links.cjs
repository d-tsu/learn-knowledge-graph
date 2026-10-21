// Validate Markdown structure and local links in the current reader-facing files.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const {pathToFileURL} = require('url');
(async () => {
  const {marked} = await import(pathToFileURL(require.resolve('marked')).href);
  const root = path.resolve(__dirname, '..');
  const files = ['README.md','HANDOFF.md','OUTLINE.md','CONTRIBUTING.md','REVIEW_POLICY.md',
    'docs/EDITORIAL_PLAN.md','docs/CHANGELOG.md','docs/DIAGRAM_PROPOSALS.md',
    'reviews/README.md','scripts/README.md','site/README.md'];
  for (const dir of ['docs/chapters','docs/appendices','templates']) {
    for (const name of fs.readdirSync(path.join(root,dir)))
      if (name.endsWith('.md')) files.push(`${dir}/${name}`);
  }
  for (const dir of ['examples/rdf-practice','examples/screen-flow-constraints',
                     'examples/development-practice']) files.push(`${dir}/README.md`);
  const results = [];
  for (const name of files) {
    const full = path.join(root,name), bytes=fs.readFileSync(full);
    const source = bytes.toString('utf8'), issues=[];
    if ([...source.matchAll(/^```/gm)].length % 2) issues.push('Unclosed code fence');
    let links = 0;
    const tokens = marked.lexer(source,{gfm:true});
    marked.walkTokens(tokens, token => {
      if (!['link','image'].includes(token.type)) return;
      const target = token.href;
      if (!target || target.startsWith('#') || /^[a-z][a-z0-9+.-]*:/i.test(target)) return;
      links++;
      const local = decodeURIComponent(target.split('#')[0]);
      if (!fs.existsSync(path.resolve(path.dirname(full), local)))
        issues.push(`Missing local target: ${target}`);
    });
    results.push({file:name, sha256:crypto.createHash('sha256').update(bytes).digest('hex'),
                  localLinks:links, issues});
  }
  const report={files:results, issueCount:results.reduce((n,r)=>n+r.issues.length,0)};
  if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({files:files.length, issueCount:report.issueCount,
                            issues:results.filter(r=>r.issues.length)},null,2));
  if(report.issueCount)process.exitCode=1;
})().catch(error=>{console.error(error);process.exitCode=1;});
