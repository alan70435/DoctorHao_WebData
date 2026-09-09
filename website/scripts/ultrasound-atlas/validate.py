#!/usr/bin/env python3
"""Technical QA only. A passing report never changes clinical-review status."""
from __future__ import annotations
import argparse, hashlib, json, re, struct, tempfile, xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image, ImageFont
import trimesh
from catalog import ITEMS
from publish import BEGIN, END, replace_block, PAGE

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'website/public/medical-visuals/ultrasound'
NS={'s':'http://www.w3.org/2000/svg'}


def check(condition,message):
    if not condition: raise AssertionError(message)


def glb_json(path):
    b=path.read_bytes();magic,version,length=struct.unpack_from('<4sII',b)
    check(magic==b'glTF' and version==2 and length==len(b),str(path)+' invalid GLB header')
    size,kind=struct.unpack_from('<I4s',b,12);check(kind==b'JSON','Missing GLB JSON chunk')
    j=json.loads(b[20:20+size]);check(j['asset']['version']=='2.0','Wrong glTF version')
    check(all('uri' not in buf for buf in j.get('buffers',[])),'GLB must be self-contained')
    return j


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--integration',action='store_true');args=parser.parse_args()
    manifest=json.loads((OUT/'manifest.json').read_text())
    check(manifest['clinicalReview']=={'status':'needs-clinician-review','reviewedBy':None},'Do not fabricate clinical approval')
    check(manifest['containsPatientData'] is False and manifest['containsSyntheticSonograms'] is False,'Unexpected image provenance')
    check([x['id'] for x in manifest['items']]==[x['id'] for x in ITEMS],'Missing, extra, or reordered regions')
    check(sum(len(x['windows']) for x in manifest['items'])==24,'Unexpected reading-route count')
    check(len(list(OUT.glob('*.glb')))==12,'Expected twelve axis variants')
    # Check the primary landmark lies within the long-axis probe's modeled footprint.
    # This is a geometric alignment check, not a clinical anatomy validation.
    for item in ITEMS:
        n=np.asarray(item['normal'],float);n/=np.linalg.norm(n)
        u=np.asarray(item['axis_vector'],float);u/=np.linalg.norm(u)
        v=np.cross(n,u);v/=np.linalg.norm(v)
        delta=np.asarray(item['points'][0])-np.asarray(item['contact'])
        check(abs(float(delta@v))<=.095,'Long-axis probe misses primary target: '+item['id'])
        check(abs(float(delta@u))<=.43,'Primary target beyond active probe length: '+item['id'])
        check(0<float(delta@(-n))<.92,'Primary target outside illustrative depth: '+item['id'])
    results=[]
    font_path=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
    for entry in manifest['items']:
        for record in entry['files']:
            p=OUT/record['path'];check(p.is_file(),'Missing '+str(p))
            check(hashlib.sha256(p.read_bytes()).hexdigest()==record['sha256'],'Digest mismatch '+str(p))
            check(p.stat().st_size==record['bytes'],'Size mismatch '+str(p))
        svg=ET.parse(OUT/entry['svg']).getroot()
        check(svg.attrib.get('viewBox')=='0 0 1800 1200','Unexpected SVG dimensions')
        check(svg.find('s:title',NS) is not None and svg.find('s:desc',NS) is not None,'Missing accessible title/description')
        check(not svg.findall('.//s:script',NS),'Script in SVG')
        for img in svg.findall('.//s:image',NS):
            check(img.attrib.get('href','').startswith('data:image/png;base64,'),'External reference in SVG')
        for t in svg.findall('.//s:text',NS):
            content=''.join(t.itertext());x=float(t.attrib['x']);y=float(t.attrib['y']);size=int(t.attrib['font-size'])
            check(0<=x<=1800 and 0<=y<=1200,'Text anchor outside SVG')
            if font_path.exists():
                f=ImageFont.truetype(str(font_path),size)
                check(x+f.getlength(content)<=1790,'Text overflow: '+content)
        with Image.open(OUT/entry['png']) as im:
            check(im.size==(1800,1200),'Wrong PNG dimensions')
            pixels=np.asarray(im.convert('RGB'));check(float(pixels.std())>15,'Blank/near-blank rendering')
        with Image.open(OUT/entry['image']) as im:check(im.size==(1800,1200),'Wrong WebP dimensions')
        for mode in ['long','short']:
            p=OUT/entry['models'][mode];data=glb_json(p)
            model=trimesh.load(p,force='scene',process=False)
            check(len(model.geometry)>=12,'Incomplete geometry '+entry['id'])
            for mesh in model.geometry.values():
                check(len(mesh.vertices)>0 and len(mesh.faces)>0,'Empty mesh')
                check(np.isfinite(mesh.vertices).all(),'Non-finite mesh coordinates')
                check(np.isfinite(mesh.vertex_normals).all(),'Non-finite normals')
                check(mesh.faces.min()>=0 and mesh.faces.max()<len(mesh.vertices),'Invalid triangle indices')
            names=[n.get('name','') for n in data['nodes']]
            check('Orientation marker - chosen display convention' in names,'Missing probe marker')
            check('Transducer acoustic face' in names,'Missing acoustic contact face')
            check('Illustrative imaging plane - not a simulated sonogram' in names,'Missing scan plane')
            if entry['id']=='wrist':
                check(sum(n.startswith('FDS tendon ') for n in names)==4,'FDS count')
                check(sum(n.startswith('FDP tendon ') for n in names)==4,'FDP count')
                check(names.count('FPL tendon')==1 and names.count('Median nerve')==1,'Wrist compartment contents')
            with Image.open(OUT/f'{entry["id"]}-{mode}-poster.webp') as im:check(im.size==(1100,825),'Wrong model-poster dimensions')
        check((OUT/entry['models']['long']).read_bytes()!=(OUT/entry['models']['short']).read_bytes(),'Axis variants are identical')
        copy=ROOT/'website_blog/medical_3d_assets/ultrasound'/entry['svg']
        check(copy.read_bytes()==(OUT/entry['svg']).read_bytes(),'Archive/public SVG drift')
        results.append({'region':entry['id'],'svg':'pass','raster':'pass','glbLong':'pass','glbShort':'pass','sha256':'pass','probeTargetGeometry':'pass','clinicalReview':'needs-clinician-review'})
    # These fixtures verify preservation and idempotence independently of live article content.
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'article.md';original='---\ntitle: unchanged\n---\n\n原文\n\n## 影片資源\n既有網址與內容\n'
        p.write_text(original);replace_block(p,'新增區塊',anchor='## 影片資源');first=p.read_bytes();replace_block(p,'新增區塊',anchor='## 影片資源')
        check(p.read_bytes()==first,'Insertion must be idempotent')
        recovered=re.sub(re.escape(BEGIN)+r'.*?'+re.escape(END)+r'\n\n','',p.read_text(),flags=re.S)
        check(recovered==original,'Insertion changed original article')
        p.write_text(original);replace_block(p,'追加圖卡');check(p.read_text().startswith(original),'Archive original bytes changed')
    if args.integration:
        article=ROOT/'website/src/content/articles/msk-ultrasound-self-study.md'
        archive=ROOT/'website_blog/posts/2023-04-blog-post_30.md'
        for p in [article,archive]:
            s=p.read_text(encoding='utf-8');check(s.count(BEGIN)==1 and s.count(END)==1,'Bad article markers')
            for entry in manifest['items']:check(entry['id']+'-anatomy-probe' in s,'Missing article illustration')
        s=article.read_text();check('forProfessionals: true' in s,'Professional-audience flag lost')
        check(s.count('<figure>')>=6 and s.count('loading="lazy"')>=6,'Missing lazy-loading article figures')
        page=ROOT/'website/src/pages/ultrasound-atlas.astro';check(page.read_text()==PAGE,'Generated atlas page drift')
        check('import MedicalModel' in page.read_text(),'Interactive component missing')
    report={'status':'pass','checks':'file integrity, image dimensions, XML, glTF, text bounds, archive synchronization, insertion idempotence','integrationChecked':args.integration,'clinicalReview':'needs-clinician-review','note':'Technical QA is not clinical validation.','regions':results}
    (OUT/'validation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'technicalQA':'pass','regions':6,'glbVariants':12,'clinicalReview':'needs-clinician-review','integrationChecked':args.integration},ensure_ascii=False))

if __name__=='__main__':main()
