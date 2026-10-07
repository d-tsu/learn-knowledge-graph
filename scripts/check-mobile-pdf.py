from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json,re
import pdfplumber
from pypdf import PdfReader
root=Path(__file__).resolve().parents[1];pages=sorted((root/'tmp/pdfs').glob('page-*.png'))
for j in range(0,len(pages),6):
 sheet=Image.new('RGB',(1470,1670),'#e8edf3');draw=ImageDraw.Draw(sheet)
 for k,p in enumerate(pages[j:j+6]):
  im=Image.open(p).convert('RGB');im.thumbnail((470,795))
  x=10+(k%3)*490;y=25+(k//3)*830
  sheet.paste(im,(x,y));draw.text((x,y-17),p.stem,fill='#20364f')
 sheet.save(root/'tmp/pdfs'/f'contact-{j//6+1}.png')
report=[]
for p in sorted((root/'output/pdf').glob('*.pdf')):
 reader=PdfReader(p);issues=[];texts=[];body_texts=[]
 with pdfplumber.open(p) as pdf:
  for n,page in enumerate(pdf.pages,1):
   text=page.extract_text() or '';texts.append(text)
   body_texts.append(page.crop((0,17*72/25.4,page.width,page.height-15*72/25.4)).extract_text() or '')
   for c in page.chars:
    if c['x0'] < -0.5 or c['x1'] > page.width+0.5 or c['top'] < -0.5 or c['bottom'] > page.height+0.5:issues.append(f'outside page {n}')
   if '\u25a0' in text:issues.append(f'black square page {n}')
 def norm(s):return re.sub(r'\s+','',s)
 pdf_text=norm(''.join(body_texts))
 sources=list((root/'docs/chapters').glob('*.md')) if p.name.startswith('knowledge-graph') else [root/'docs/chapters'/p.name.replace('-mobile.pdf','.md')]
 missing=[];checked=0
 for source in sources:
  in_code=False
  for line in source.read_text(encoding='utf-8-sig').splitlines():
   if line.startswith('```'):in_code=not in_code;continue
   if in_code or not line.strip():continue
   parts=line.strip().strip('|').split('|') if line.startswith('|') else [line]
   for part in parts:
    if re.fullmatch(r'\s*:?-+:?\s*',part):continue
    part=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',part)
    part=re.sub(r'^(?:#{1,3}\s+|>\s+|-\s+|\d+\.\s+)', '',part.strip())
    part=part.replace('**','').replace('`','')
    checked+=1
    if norm(part) not in pdf_text:missing.append({'source':source.name,'text':part})
 if missing:issues.append({'missing_source_text':missing})
 report.append({'file':p.name,'pages':len(reader.pages),'outlines':len(reader.outline),'links':sum(len(page.get('/Annots',[])) for page in reader.pages),'characters':sum(map(len,texts)),'source_chunks_checked':checked,'issues':issues})
 (root/'tmp/pdfs'/f'{p.stem}-text.txt').write_text('\n\n'.join(texts),encoding='utf-8')
(root/'tmp/pdfs'/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
