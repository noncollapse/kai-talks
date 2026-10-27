"""Generate the editable FigureSpec files and SVGs used by TabularTimeline.vue.

Usage: python3 make_timeline.py --renderer /path/to/figure_renderer.py
The diagram follows the user's survey figure; bibliographic corrections and
individual paper links are retained in specs/tabular-timeline-data.json.
"""
import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CATALOG = json.loads((HERE / 'specs/survey-catalog.json').read_text())
COLORS = {'feature': '#B95136', 'sample': '#A5770E', 'objective': '#26798C', 'transfer': '#8055A0', 'general': '#607E13'}
FILLS = {'specialized': '#FCF6F3', 'transfer': '#F5F0FA', 'general': '#F1F6E8'}
# year, displayed name, venue, category, optional catalog lookup name/title fragment
DATA = [
(2017,'SNN','NeurIPS','feature'),
(2018,'RLNs','NeurIPS','objective'),
(2019,'AutoInt','CIKM','feature'),(2019,'ANP','ICLR','sample'),
(2020,'GrowNet','Preprint','feature'),(2020,'NODE','ICLR','feature'),(2020,'TabTransformer','Preprint','feature'),
(2021,'FT-Transformer','NeurIPS','feature'),(2021,'TabNet','AAAI','feature'),(2021,'DCN v2','WWW','feature','DCNv2'),(2021,'NPT','NeurIPS','sample'),(2021,'Kadra et al.','NeurIPS','objective','Well-tuned simple nets'),
(2022,'MLP-PLR / RTDL','NeurIPS','feature','MLP-PLR'),(2022,'DANet','AAAI','feature','DANets'),(2022,'SAINT','NeurIPS WS','sample'),(2022,'DNNR','ICML','sample'),(2022,'Hopular','Preprint','sample'),
(2023,'TabToken','Preprint','feature'),(2023,'Beyazit et al.','NeurIPS','feature','An inductive bias'),(2023,'Trompt','ICML','sample'),(2023,'TANGOS','ICLR','objective'),
(2024,'RealMLP','NeurIPS','feature'),(2024,'ExcelFormer','KDD','feature'),(2024,'GRANDE','ICLR','feature'),(2024,'AMFormer','AAAI','feature'),(2024,'BiSHop','ICML','feature'),(2024,'TabR','ICLR','sample'),(2024,'SwitchTab','AAAI','feature'),(2024,'PTaRL','ICLR','objective'),
(2025,'TabM','ICLR','feature'),(2025,'ModernNCA','ICLR','sample'),
(2019,'DeepInsight','Scientific Reports','transfer'),(2019,'Super-TML','CVPR WS','transfer'),
(2020,'VIME','NeurIPS','transfer'),(2020,'Iwata et al.','NeurIPS','transfer','Meta-learning from tasks'),(2020,'REFINED','Nature Communications','transfer'),(2020,'TAC','bioRxiv','transfer'),
(2021,'SubTab','NeurIPS','transfer'),(2021,'DACL+','ICML','transfer','DACL'),(2021,'IGTD','Scientific Reports','transfer'),
(2022,'Revisiting pretraining','Preprint','transfer','Revisiting pretraining objectives'),(2022,'SEFS','ICLR','transfer'),(2022,'MET','Preprint','transfer'),(2022,'SCARF','ICLR','transfer'),(2022,'Stab','NeurIPS WS','transfer'),(2022,'DEN','TMLR','transfer'),(2022,'TransTab','NeurIPS','transfer'),(2022,'PTab','Preprint','transfer','Ptab'),(2022,'LIFT','NeurIPS','transfer'),
(2023,'DoRA','CIKM','transfer'),(2023,'Binder','ICLR','transfer'),(2023,'Levin et al.','ICLR','transfer','Transfer learning with deep tabular'),(2023,'CAAFE','NeurIPS','transfer'),(2023,'ReConTab','Preprint','transfer'),(2023,'TaPTaP','EMNLP','transfer'),(2023,'TabRet','Preprint','transfer'),(2023,'TabLLM','AISTATS','transfer'),(2023,'ORCA','ICML','transfer'),(2023,'UniPredict','Preprint','transfer'),(2023,'XTab','ICML','transfer','Xtab'),(2023,'TablEye','Preprint','transfer'),(2023,'Meta-Transformer','Preprint','transfer'),(2023,'TabToken','Preprint','transfer'),
(2024,'LFR','ICLR','transfer'),(2024,'LM-IGTD','Preprint','transfer'),(2024,'UniTabE','ICLR','transfer'),(2024,'CM2','WWW','transfer'),(2024,'TP-BERTa','ICLR','transfer'),(2024,'CARTE','ICML','transfer'),(2024,'FeatLLM','ICML','transfer'),
(2025,'Tab2Visual','Preprint','transfer'),
(2023,'TabPFN','ICLR','general'),(2023,'TabPTM','Preprint','general'),
(2024,'HyperFast','AAAI','general'),(2024,'TabuLa-8B','NeurIPS','general'),(2024,'GTL','KDD','general'),(2024,'MediTab','IJCAI','general'),
(2025,'TabPFN v2','Nature','general'),(2025,'TabICL','ICML','general'),(2025,'MotherNet','ICLR','general'),
]
EXTRA_URLS = {
 'ANP': 'https://arxiv.org/abs/1901.05761',
 'DeepInsight': 'https://www.nature.com/articles/s41598-019-47765-6',
 'REFINED': 'https://www.nature.com/articles/s41467-020-18197-y',
 'TabICL': 'https://proceedings.mlr.press/v267/qu25d.html',
}

def entries():
    result = []
    for i, row in enumerate(DATA):
        year, name, venue, category = row[:4]
        lookup = row[4] if len(row) == 5 else name
        found = next((p for p in CATALOG['papers'] if p['name'].lower() == lookup.lower()), None)
        if not found:
            found = next((p for p in CATALOG['papers'] if lookup.lower() in p['title'].lower()), None)
        url = EXTRA_URLS.get(name) or (found or {}).get('url')
        if not url:
            raise ValueError(f'Missing primary paper source for {name}')
        result.append(dict(id=f'method-{i}', year=year, name=name, venue=venue, category=category,
                           lane=category if category in ('transfer','general') else 'specialized', url=url))
    return result

FOUNDATIONS = [
 ('Early statistics', 'Linear regression\nLogistic regression'),
 ('1950s–1960s', 'kNN · Perceptron / MLP\nAdaLine'),
 ('1960s–1990s', 'SVM · Kernel SVM\nDecision trees / CART'),
 ('1990s–2000s', 'AdaBoost · GBDT\nRandom forests (2001)'),
 ('2004', 'NCA'),
 ('2016–2018', 'XGBoost · LightGBM\nCatBoost'),
]

def label(spec, text, x, y, size=22, color='#64748B', anchor='start'):
    spec['labels'].append(dict(text=text,x=x,y=y,font_size=size,color=color,anchor=anchor))

def node(spec, id, text, x, y, w, h, color='#17233E', fill='#FFFFFF', stroke='#DCE4F2', size=22, sub=None):
    item=dict(id=id,label=text,x=x,y=y,width=w,height=h,shape='rounded',font_size=size,text_color=color,fill=fill,stroke=stroke)
    if sub: item['sublabel']=sub
    spec['nodes'].append(item)

def make_spec(methods, mode):
    overview = mode == 'all'
    periods={'early':range(2017,2022),'middle':range(2022,2024),'late':range(2024,2026)}
    width, height = (2480,1080) if overview else (1800,820)
    spec=dict(title='A timeline of tabular learning — '+mode,canvas=dict(width=width,height=height),
              style=dict(font_family='Arial, Helvetica, sans-serif',font_size=22,bg_color='#FBFCFF',palette=list(COLORS.values())),nodes=[],edges=[],groups=[],labels=[])
    if mode=='classical':
        label(spec,'The classical foundations',40,47,34,'#17233E')
        label(spec,'A compact chronology of the method families in the reference figure',40,85,23)
        for i,(era,text) in enumerate(FOUNDATIONS):
            col,row=i%3,i//3
            x,y=310+590*col,260+320*row
            node(spec,f'era-{i}',era,x,y-72,510,52,size=27,fill='#EDF1FA',stroke='#EDF1FA')
            node(spec,f'foundation-{i}',text,x,y+38,510,150,size=29,fill='#FFFFFF',stroke='#DEE5F1')
            if col<2: spec['edges'].append({'from':f'era-{i}','to':f'era-{i+1}','color':'#A6B4CA'})
        label(spec,'Periods summarize broad families; they are not exact first-publication dates for every method.',40,780,21)
        return spec
    years=list(range(2017,2026)) if overview else list(periods[mode])
    left=290 if overview else 32
    available=width-left-24
    weights={2017:1,2018:1,2019:1.25,2020:1.4,2021:1.8,2022:2.6,2023:3.1,2024:2.9,2025:2.1} if overview else {y:1 for y in years}
    total=sum(weights[y] for y in years)
    positions={}; x=left
    for y in years:
        w=available*weights[y]/total
        positions[y]=(x,w);x+=w
    if overview:
        label(spec,'Traditional methods',22,46,24,'#17233E')
        label(spec,'Foundations and ensembles',22,78,17)
        for i,(era,text) in enumerate(FOUNDATIONS):
            y=167+i*142
            label(spec,era,28,y-27,19,'#4263EB')
            fs=min(18,int(220/(max(map(len,text.split('\n')))*.6)))
            node(spec,f'foundation-{i}',text,139,y+25,232,84,size=fs,fill='#F0F3F9',stroke='#F0F3F9')
    for i,y in enumerate(years):
        x,w=positions[y]
        node(spec,f'year-{y}',str(y),x+w/2,49,w-18,50,size=30 if overview else 34,fill='#EAF0FC',stroke='#EAF0FC',color='#304465')
        if i: spec['edges'].append({'from':f'year-{years[i-1]}','to':f'year-{y}','color':'#A6B4CA','thickness':2})
    if overview:
        bands=[('specialized',113,160,53),('transfer',447,494,52),('general',908,955,52)]
    elif mode=='early':
        bands=[('specialized',112,162,58),('transfer',500,550,58)]
    else:
        bands=[('specialized',112,164,64),('transfer',330,384,68),('general',690,743,56)]
    for lane,heading_y,first_y,dy in bands:
        titles={'specialized':'Specialized methods · fit to a target dataset','transfer':'Transferable methods · pretrain, then adapt','general':'General methods · reuse across datasets'}
        label(spec,titles[lane],left,heading_y,23 if overview else 26,'#17233E')
        for year in years:
            x,w=positions[year]
            items=[m for m in methods if m['year']==year and m['lane']==lane]
            if not items: continue
            if overview: cols=2 if year>=2022 else 1
            elif mode=='early': cols=1
            else: cols=4
            cols=min(cols,len(items))
            cell_width=(w-34)/cols
            ids=[]
            for i,m in enumerate(items):
                col,row=i%cols,i//cols
                cx=x+17+cell_width*(col+.5)
                cy=first_y+row*dy
                venue={'Scientific Reports':'Sci. Rep.','Nature Communications':'Nat. Commun.'}.get(m['venue'],m['venue'])
                font=min(21 if overview else 27,int((cell_width-12)/(max(len(m['name']),len(venue))*.58)))
                font=max(13 if overview else 18,font)
                sub=venue if overview else f"{venue} {year}"
                node(spec,m['id'],m['name'],cx,cy,cell_width-7,dy-5,color=COLORS[m['category']],fill=FILLS[lane],stroke=FILLS[lane],size=font,sub=sub)
                ids.append(m['id'])
            spec['groups'].append(dict(id=f'{lane}-{year}',node_ids=ids,padding=7,fill=FILLS[lane],stroke='#DDE4EE'))
    if mode=='early':
        label(spec,'General / foundation models enter this survey timeline in 2023.',left,798,22,'#607E13')
    if overview:
        for x,text,key in [(1510,'Feature aspect','feature'),(1790,'Sample aspect','sample'),(2080,'Objective aspect','objective')]:
            label(spec,text,x,113,19,COLORS[key])
        label(spec,'Adapted from Jiang et al., Representation Learning for Tabular Data: A Comprehensive Survey (TPAMI, 2026).  WS = workshop.',20,1062,18)
    return spec

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--renderer',required=True);args=parser.parse_args()
    module=importlib.util.spec_from_file_location('figure_renderer',args.renderer);renderer=importlib.util.module_from_spec(module);module.loader.exec_module(renderer)
    methods=entries()
    # Keep only catalog records referenced by this figure, not an unrelated full literature dump.
    data=dict(source='Jiang et al., Representation Learning for Tabular Data: A Comprehensive Survey, TPAMI 2026',source_url='https://doi.org/10.1109/TPAMI.2026.3657217',checked='2026-10-26',scope='The supplied 2017–2025 survey figure, not an exhaustive bibliography through 2026.',methods=methods,foundations=FOUNDATIONS,
        editorial_notes=['RTDL and MLP-PLR are grouped as one numerical-feature-embedding family (NeurIPS 2022), rather than counted as two independent papers.','TabToken is retained in both specialized and transferable roles, as in the reference.','Random forests: 2001 original paper, not 2002.','SAINT: NeurIPS workshop; Super-TML: CVPR workshop; TANGOS: ICLR 2023; TabICL: ICML 2025.','Classical dates are broad eras except where explicitly tied to an individual paper.'],
        additional_sources=['https://doi.org/10.1023/A:1010933404324','https://proceedings.mlr.press/v267/qu25d.html','https://openreview.net/forum?id=FiyUTAy4sB8','https://github.com/yandex-research/rtdl-num-embeddings'])
    (HERE/'specs/tabular-timeline-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    public=ROOT/'public/figs';public.mkdir(parents=True,exist_ok=True)
    for mode in ('all','classical','early','middle','late'):
        spec=make_spec(methods,mode)
        issues=renderer.validate_spec(spec)
        if issues: raise ValueError('\n'.join(issues))
        name='tabular-timeline' if mode=='all' else f'tabular-timeline-{mode}'
        (HERE/'specs'/f'{name}.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
        svg=renderer.render_svg(spec)
        (public/f'{name}.svg').write_text(svg)
        if mode=='all': (HERE/f'{name}.svg').write_text(svg)
        print(f'{mode}: {len(spec["nodes"])} nodes; validation passed')
    print(f'{len(methods)} method entries ({len(set(m["name"] for m in methods))} unique labels)')

if __name__=='__main__': main()
