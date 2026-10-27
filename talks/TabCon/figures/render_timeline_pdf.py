"""Export the full FigureSpec timeline to a standalone vector PDF (ReportLab)."""
import json
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

here = Path(__file__).resolve().parent
spec = json.loads((here/'specs/tabular-timeline.json').read_text())
w,h = spec['canvas']['width'],spec['canvas']['height']
out=here/'tabular-timeline.pdf'
c=canvas.Canvas(str(out),pagesize=(w,h))
c.setTitle('A timeline of tabular learning')
c.setSubject('Adapted from Jiang et al., TPAMI 2026; selected methods from 2017–2025.')
c.setFillColor(HexColor(spec['style']['bg_color']));c.rect(0,0,w,h,stroke=0,fill=1)
nodes={n['id']:n for n in spec['nodes']}
def rectangle(x,y,width,height,fill,stroke,radius=8,line=1):
 c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke));c.setLineWidth(line)
 c.roundRect(x,h-y-height,width,height,radius,stroke=1,fill=1)
def text(value,x,y,size,color,bold=False,anchor='middle'):
 c.setFillColor(HexColor(color));c.setFont('Helvetica-Bold' if bold else 'Helvetica',size)
 draw={'start':c.drawString,'middle':c.drawCentredString,'end':c.drawRightString}[anchor]
 draw(x,h-y,value)
for g in spec['groups']:
 ns=[nodes[id] for id in g['node_ids']];p=g.get('padding',20)
 x=min(n['x']-n['width']/2 for n in ns)-p;y=min(n['y']-n['height']/2 for n in ns)-p
 r=max(n['x']+n['width']/2 for n in ns)+p;b=max(n['y']+n['height']/2 for n in ns)+p
 rectangle(x,y,r-x,b-y,g['fill'],g['stroke'])
for e in spec['edges']:
 a,b=nodes[e['from']],nodes[e['to']]
 # All timeline edges join consecutive horizontal year labels.
 assert a['y']==b['y']
 sx=a['x']+a['width']/2;ex=b['x']-b['width']/2;y=h-a['y']
 c.setStrokeColor(HexColor(e['color']));c.setLineWidth(e.get('thickness',2));c.line(sx,y,ex-4,y)
 c.setFillColor(HexColor('#555555'))
 p=c.beginPath();p.moveTo(ex,y);p.lineTo(ex-8,y+4);p.lineTo(ex-8,y-4);p.close();c.drawPath(p,fill=1,stroke=0)
for n in spec['nodes']:
 rectangle(n['x']-n['width']/2,n['y']-n['height']/2,n['width'],n['height'],n['fill'],n['stroke'],line=2)
 fs=n['font_size'];lines=n['label'].split('\n');count=len(lines)+bool(n.get('sublabel'));dy=fs+2
 start=n['y']-(count-1)*dy/2+fs*.35
 for i,line in enumerate(lines):text(line,n['x'],start+i*dy,fs,n['text_color'],True)
 if n.get('sublabel'):text(n['sublabel'],n['x'],start+len(lines)*dy,fs-3,'#888888')
for l in spec['labels']:text(l['text'],l['x'],l['y'],l['font_size'],l['color'],anchor=l.get('anchor','middle'))
c.save();print(out)
