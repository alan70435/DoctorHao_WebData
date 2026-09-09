#!/usr/bin/env python3
"""Fail closed on missing article coverage, corrupt GLBs, altered Markdown or broken local paths."""
import hashlib, json, struct, sys, xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'public/medical-visuals'

def check_glb(path):
    data=path.read_bytes();magic,version,length=struct.unpack_from('<4sII',data)
    assert (magic,version,length)==(b'glTF',2,len(data)),path
    size,kind=struct.unpack_from('<I4s',data,12);assert kind==b'JSON'
    doc=json.loads(data[20:20+size]);off=20+size
    size,kind=struct.unpack_from('<I4s',data,off);assert kind==b'BIN\0'
    binary=data[off+8:off+8+size]
    assert doc['asset']['version']=='2.0' and doc['extras']['notForDiagnosis'] is True
    assert all('uri' not in b for b in doc['buffers'])
    arrays=[]
    for a in doc['accessors']:
        b=doc['bufferViews'][a['bufferView']];start=b.get('byteOffset',0)+a.get('byteOffset',0)
        count=a['count'];channels={'SCALAR':1,'VEC3':3,'VEC4':4}[a['type']]
        dtype={5126:'<f4',5125:'<u4'}[a['componentType']]
        assert 0<=start<=len(binary) and start+count*channels*4<=len(binary)
        arr=np.frombuffer(binary,dtype=dtype,count=count*channels,offset=start).reshape(count,channels)
        assert np.isfinite(arr).all(),(path,'nonfinite')
        arrays.append(arr)
    for mesh in doc['meshes']:
        for p in mesh['primitives']:
            v=arrays[p['attributes']['POSITION']];n=arrays[p['attributes']['NORMAL']];f=arrays[p['indices']]
            assert len(v)==len(n) and len(f)%3==0 and f.max()<len(v)
            assert np.allclose(np.linalg.norm(n,axis=1),1,atol=.002),(path,'invalid normals')
    if path.stem=='knee-motion':assert len(doc['animations'])==1
    return len(data)

def main():
    manifest=json.loads((OUT/'manifest.json').read_text())
    assert manifest==json.loads((ROOT/'src/data/medical-visuals.json').read_text())
    expected={p.stem for p in (ROOT/'src/content/articles').glob('*.md')}
    assert expected==set(manifest['articles']), 'Every article must have a deliberate brief.'
    sources=manifest['sources'];total=0
    for slug,item in manifest['articles'].items():
        assert slug==item['slug'] and item['reviewStatus']=='clinician-review-pending'
        assert len(item['points'])==3 and item['alt'] and item['caution'] and item['modelNotes']
        assert all(k in sources for k in item['sourceIds'])
        original=ROOT.parent/item['articlePath']
        assert hashlib.sha256(original.read_bytes()).hexdigest()==item['articleSha256'],original
        for key in ['cover','coverSmall','coverMedium','figure','figureRaster','og','model','poster']:
            url=item[key];assert url.startswith('/medical-visuals/') and '..' not in url
            assert (ROOT/'public'/url.lstrip('/')).is_file(),url
        folder=OUT/'articles'/slug
        for filename,sha in item['sha256'].items():
            assert hashlib.sha256((folder/filename).read_bytes()).hexdigest()==sha,filename
        sizes={'cover.webp':(1600,900),'cover-800.webp':(800,450),'cover-480.webp':(480,270),'explain.webp':(1600,1120),'og.jpg':(1200,630)}
        for filename,size in sizes.items():
            with Image.open(folder/filename) as image:assert image.size==size;image.load()
        svg=ET.parse(folder/'explain.svg').getroot()
        assert svg.find('{http://www.w3.org/2000/svg}title') is not None
        for el in svg.iter():
            assert not el.tag.endswith(('script','foreignObject'))
            assert all(not key.lower().startswith('on') for key in el.attrib)
            if 'href' in el.attrib:assert el.attrib['href'].startswith('data:image/webp;base64,')
    for key,model in manifest['models'].items():
        path=ROOT/'public'/model['src'].lstrip('/')
        assert hashlib.sha256(path.read_bytes()).hexdigest()==model['sha256']
        total+=check_glb(path)
    assert (OUT/'knee-flexion.mp4').stat().st_size>10000
    result={'status':'passed','articleCoverage':len(expected),'glbFiles':len(manifest['models']),'modelBytes':total,'markdownHashesUnchanged':True,'reviewStatus':'clinician-review-pending','checks':['exact article coverage','all local URLs','image decoding and dimensions','SVG safety/self-containment','SHA-256 integrity','GLB headers/accessors/indices/unit normals','motion track present']}
    (OUT/'validation-report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
