from pathlib import Path
import re, html, json, hashlib
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether, Image, HRFlowable
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf'
OUT.mkdir(parents=True,exist_ok=True)
W,H=108*mm,180*mm
M=10*mm
CW=W-2*M
BLUE=colors.HexColor('#244a73')
INK=colors.HexColor('#23364a')
MUTED=colors.HexColor('#677889')
LIGHT=colors.HexColor('#f2f6fb')
pdfmetrics.registerFont(TTFont('Meiryo','C:/Windows/Fonts/meiryo.ttc',subfontIndex=0))
pdfmetrics.registerFont(TTFont('MeiryoBold','C:/Windows/Fonts/meiryob.ttc',subfontIndex=0))
pdfmetrics.registerFontFamily('Meiryo',normal='Meiryo',bold='MeiryoBold',italic='Meiryo',boldItalic='MeiryoBold')
S={}
S['body']=ParagraphStyle('body',fontName='Meiryo',fontSize=10.7,leading=17.3,textColor=INK,wordWrap='CJK',spaceAfter=9,allowWidows=0,allowOrphans=0)
S['h1']=ParagraphStyle('h1',parent=S['body'],fontName='MeiryoBold',fontSize=18,leading=27,textColor=BLUE,spaceBefore=5,spaceAfter=15,keepWithNext=True)
S['h2']=ParagraphStyle('h2',parent=S['body'],fontName='MeiryoBold',fontSize=13.2,leading=21,textColor=BLUE,spaceBefore=15,spaceAfter=9,keepWithNext=True)
S['h3']=ParagraphStyle('h3',parent=S['body'],fontName='MeiryoBold',fontSize=11.4,leading=18,spaceBefore=10,spaceAfter=7,keepWithNext=True)
S['small']=ParagraphStyle('small',parent=S['body'],fontSize=8.7,leading=14,textColor=MUTED,spaceAfter=8)
S['cardtitle']=ParagraphStyle('cardtitle',parent=S['body'],fontName='MeiryoBold',fontSize=11.4,leading=18,textColor=BLUE,spaceAfter=4)
S['card']=ParagraphStyle('card',parent=S['body'],fontSize=10.4,leading=16.5,spaceAfter=2)
S['bullet']=ParagraphStyle('bullet',parent=S['body'],leftIndent=12,firstLineIndent=0,bulletIndent=0,bulletFontName='Meiryo',bulletFontSize=10.7,spaceAfter=7)
S['quote']=ParagraphStyle('quote',parent=S['body'],fontSize=10.4,leading=17,textColor=INK)

FILES=list(sorted((ROOT/'docs/chapters').glob('*.md')))
BOOKMARKS={p.name:'chapter'+p.name[:2] for p in FILES}

class Doc(BaseDocTemplate):
 def __init__(self,file,label,**kw):
  self.label=label;self.section='';self.heading_counter=0
  super().__init__(str(file),pagesize=(W,H),leftMargin=M,rightMargin=M,topMargin=17*mm,bottomMargin=15*mm,title=label,author='learn-knowledge-graph',**kw)
  frame=Frame(M,15*mm,CW,H-32*mm,id='body',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
  self.addPageTemplates(PageTemplate(id='mobile',frames=frame,onPage=self.decorate))
 def decorate(self,c,doc):
  c.saveState();c.setFillColor(BLUE);c.rect(0,H-3*mm,W,3*mm,fill=1,stroke=0)
  c.setFont('Meiryo',7.1);c.setFillColor(MUTED);c.drawString(M,H-10*mm,'ナレッジグラフ・オントロジー学習ノート')
  c.setStrokeColor(colors.HexColor('#d9e2ec'));c.line(M,11*mm,W-M,11*mm)
  c.setFont('Meiryo',7);c.drawString(M,6.7*mm,'スマホ読書版 | 2026-10-01')
  c.drawRightString(W-M,6.7*mm,str(doc.page));c.restoreState()
 def afterFlowable(self,f):
  if isinstance(f,Paragraph) and hasattr(f,'bookmark'):
   self.canv.bookmarkPage(f.bookmark)
   self.canv.addOutlineEntry(f.getPlainText(),f.bookmark,level=f.outline_level,closed=False)


def inline(text,combined=False):
 refs=[]
 def stash(m):
  label=m.group(1);url=m.group(2)
  tag=html.escape(label)
  if url.startswith(('https://','http://')):
   tag='<link href="'+html.escape(url,quote=True)+'" color="#1e6b82">'+tag+'</link>'
  elif combined and Path(url.split('#')[0]).name in BOOKMARKS:
   tag='<link href="#'+BOOKMARKS[Path(url.split('#')[0]).name]+'" color="#1e6b82">'+tag+'</link>'
  refs.append(tag);return 'ZZREF'+str(len(refs)-1)+'ZZ'
 text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',stash,text)
 text=html.escape(text)
 text=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',text)
 text=re.sub(r'`([^`]+)`',r'<font color="#1e6b82">\1</font>',text)
 for n,ref in enumerate(refs):text=text.replace('ZZREF'+str(n)+'ZZ',ref)
 return text


def para(text,style='body',combined=False):return Paragraph(inline(text,combined),S[style])

def card(headers,row,combined):
 cells=[]
 for i,(head,value) in enumerate(zip(headers,row)):
  if i==0:
   value='<font size="8.5" color="#677889">'+html.escape(head)+'</font><br/>'+inline(value,combined)
   cells.append([Paragraph(value,S['cardtitle'])])
  else:
   value='<b>'+html.escape(head)+'</b><br/>'+inline(value,combined)
   cells.append([Paragraph(value,S['card'])])
 t=Table(cells,colWidths=[CW],hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('BOX',(0,0),(-1,-1),0.45,colors.HexColor('#d9e3ef')),('LINEBEFORE',(0,0),(0,-1),2,colors.HexColor('#7e9dc8')),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,0),7),('BOTTOMPADDING',(0,-1),(-1,-1),8),('TOPPADDING',(0,1),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-2),3)]))
 return t


def chapter(p,combined=False):
 lines=p.read_text(encoding='utf-8-sig').splitlines();flow=[];i=0;fig=0;heading_num=0
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line.startswith('```'):
   code=[];lang=line[3:];i+=1
   while i<len(lines) and not lines[i].strip().startswith('```'):code.append(lines[i]);i+=1
   if lang=='mermaid':
    fig+=1;img=ROOT/'tmp/pdfs'/f'{p.stem}-{fig}.png'
    from PIL import Image as PILImage
    with PILImage.open(img) as im:iw,ih=im.size
    scale=min(CW/iw,(H-65*mm)/ih)
    picture=Image(str(img),width=iw*scale,height=ih*scale)
    caption=para('図 '+str(fig)+'　本文の関係を縦向きに配置','small',combined)
    flow.append(KeepTogether([Spacer(1,4),picture,Spacer(1,7),caption]))
   else:
    flow.append(para('\n'.join(code),'small',combined))
   i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    row=[x.strip() for x in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r':?-+:?',x) for x in row):rows.append(row)
    i+=1
   for n,row in enumerate(rows[1:]):
    group=[card(rows[0],row,combined),Spacer(1,8)]
    if n==0 and flow and isinstance(flow[-1],Paragraph) and flow[-1].style.name in ('h2','h3'):
     group.insert(0,flow.pop())
    flow.append(KeepTogether(group))
   continue
  m=re.match(r'^(#{1,3})\s+(.+)$',line)
  if m:
   level=len(m[1]);heading=para(m[2],'h'+str(level),combined)
   if level==1:heading.bookmark=BOOKMARKS[p.name];heading.outline_level=0
   elif level==2:
    heading_num+=1;heading.bookmark=BOOKMARKS[p.name]+'-section'+str(heading_num);heading.outline_level=1
   flow.append(heading);i+=1;continue
  if line.startswith('> '):
   text=[]
   while i<len(lines) and lines[i].strip().startswith('> '):text.append(lines[i].strip()[2:]);i+=1
   t=Table([[para(' '.join(text),'quote',combined)]],colWidths=[CW]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBEFORE',(0,0),(0,0),2,BLUE)]));flow.extend([t,Spacer(1,9)]);continue
  m=re.match(r'^(?:- |(\d+)\. )(.+)$',line)
  if m:
   bullet=(m[1]+'.') if m[1] else '・'
   flow.append(Paragraph(inline(m[2],combined),S['bullet'],bulletText=bullet));i+=1;continue
  text=[line];i+=1
  while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||```|> |- |\d+\. )',lines[i].strip()):text.append(lines[i].strip());i+=1
  content=' '.join(text)
  style='small' if content.startswith('更新日：') else 'body'
  if content.startswith('解答例：'):
   flow.append(Spacer(1,3));flow.append(HRFlowable(width='100%',thickness=.45,color=colors.HexColor('#d9e3ef')));flow.append(Spacer(1,5))
  flow.append(para(content,style,combined))
 return flow

manifest={'generated':'2026-10-01','format':'108x180mm / Meiryo embedded / cards for table rows','sources':{},'outputs':[]}
for p in FILES:
 manifest['sources'][str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
 label=p.read_text(encoding='utf-8-sig').splitlines()[0].lstrip('# ')
 target=OUT/f'{p.stem}-mobile.pdf'
 Doc(target,label).build(chapter(p))
 r=PdfReader(target)
 manifest['outputs'].append({'file':target.name,'pages':len(r.pages),'bytes':target.stat().st_size})
 print(json.dumps(manifest['outputs'][-1],ensure_ascii=False))
combined=OUT/'knowledge-graph-chapters-00-02-mobile.pdf'
story=[Paragraph('ナレッジグラフ・<br/>オントロジー<br/>学習ノート',S['h1']),para('序章・第1章・第2章','h2'),para('スマホ読書版','body'),para('2026-10-01 改稿・独立レビュー済みの本文を収録。本文は省略せず、表を項目ごとのカード形式にして、図を縦向きに配置しました。','body'),Spacer(1,12)]
for p in FILES:
 label=p.read_text(encoding='utf-8-sig').splitlines()[0].lstrip('# ')
 story.append(Paragraph('<link href="#'+BOOKMARKS[p.name]+'" color="#1e6b82">'+html.escape(label)+'</link>',S['body']))
story.extend([Spacer(1,10),para('章名をタップするか、PDFのしおりで移動できます。外部の出典リンクはタップで開けます。元の資料はMarkdownで管理しています。','small')])
for p in FILES:story.append(PageBreak());story+=chapter(p,True)
Doc(combined,'ナレッジグラフ・オントロジー学習ノート - 序章から第2章').build(story)
r=PdfReader(combined)
manifest['outputs'].append({'file':combined.name,'pages':len(r.pages),'bytes':combined.stat().st_size})
(OUT/'mobile-export-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest['outputs'][-1],ensure_ascii=False))
