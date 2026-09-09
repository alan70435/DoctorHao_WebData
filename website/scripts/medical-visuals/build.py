#!/usr/bin/env python3
"""Rebuild original 3-D medical teaching assets and their article manifest.

Run from any directory: python scripts/medical-visuals/build.py
Dependencies are pinned in requirements.txt. Network access is never used by this script.
"""
import argparse, base64, hashlib, html, json, math, os, re, struct, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from catalog import SOURCES, REVIEW_DATE, briefs
from geometry import make_scene, normals, color_rgb, poly_mesh, TEAL, ORANGE, BONE

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'public/medical-visuals'
DATA=ROOT/'src/data/medical-visuals.json'
BG=(12,27,37)
FONT_PATH=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
FONT_BOLD=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def font(size,bold=False):
    p=FONT_BOLD if bold and FONT_BOLD.exists() else FONT_PATH
    if not p.exists():raise RuntimeError('Install fonts-noto-cjk for Traditional Chinese rendering; do not copy fonts into the repository.')
    return ImageFont.truetype(str(p),size,index=3)

def wrap(text,f,width):
    lines=[];line=''
    for ch in text:
        if ch=='\n' or (line and f.getlength(line+ch)>width):
            lines.append(line);line='' if ch=='\n' else ch
        else:line+=ch
    if line:lines.append(line)
    return lines

class Renderer:
    def __init__(self):
        self.r=vtk.vtkRenderer();self.r.SetBackground(0,0,0);self.r.SetBackgroundAlpha(0)
        self.r.SetUseFXAA(True)
        self.w=vtk.vtkRenderWindow();self.w.SetOffScreenRendering(1);self.w.SetAlphaBitPlanes(1);self.w.SetMultiSamples(0);self.w.AddRenderer(self.r)
    def image(self,scene,w=1100,h=1100,yaw=0,angle=0):
        self.r.RemoveAllViewProps();self.r.RemoveAllLights();self.w.SetSize(w,h)
        for part in scene.parts:
            poly=poly_mesh(part.vertices,part.faces)
            n=vtk.vtkPolyDataNormals();n.SetInputData(poly);n.SplittingOff();n.ConsistencyOn();n.AutoOrientNormalsOn()
            mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(n.GetOutputPort())
            actor=vtk.vtkActor();actor.SetMapper(mapper)
            p=actor.GetProperty();p.SetColor(*color_rgb(part.color));p.SetInterpolationToPhong();p.SetAmbient(.25);p.SetDiffuse(.68);p.SetSpecular(.15);p.SetSpecularPower(28)
            if part.group=='lower-leg' and angle:actor.RotateX(angle)
            self.r.AddActor(actor)
        bounds=scene.bounds();center=bounds.mean(0)
        camera=np.array(scene.camera,float);zrot=np.deg2rad(yaw);c,s=np.cos(zrot),np.sin(zrot);camera=np.array([[c,-s,0],[s,c,0],[0,0,1]])@camera
        forward=-camera/np.linalg.norm(camera);right=np.cross(forward,[0,0,1]);right/=np.linalg.norm(right);up=np.cross(right,forward)
        corners=np.array([[x,y,z] for x in bounds[:,0] for y in bounds[:,1] for z in bounds[:,2]])-center
        vertical=np.ptp(corners@up);horizontal=np.ptp(corners@right)
        span=max(vertical,horizontal*h/w)*.58
        if scene.name.startswith('knee-'):
            center=np.array([0,-.12,.18]);span=2.73  # Intentional close-up, shafts continue off-frame.
        cam=self.r.GetActiveCamera();cam.SetPosition(*(center+camera*2));cam.SetFocalPoint(*center);cam.SetViewUp(0,0,1);cam.ParallelProjectionOn();cam.SetParallelScale(span)
        for off,intensity in [((-5,-8,10),.78),((8,-4,3),.40),((2,7,9),.53)]:
            light=vtk.vtkLight();light.SetLightTypeToSceneLight();light.SetPosition(*(center+np.array(off)));light.SetFocalPoint(*center);light.SetIntensity(intensity);self.r.AddLight(light)
        self.r.ResetCameraClippingRange();self.w.Render()
        capture=vtk.vtkWindowToImageFilter();capture.SetInput(self.w);capture.SetInputBufferTypeToRGBA();capture.ReadFrontBufferOff();capture.Update()
        data=capture.GetOutput();arr=vtk_to_numpy(data.GetPointData().GetScalars()).reshape(h,w,4)
        return Image.fromarray(np.flipud(arr),'RGBA')
    def close(self):self.w.Finalize()

def backdrop(size):
    w,h=size;yy,xx=np.mgrid[0:h,0:w];v=np.exp(-(((xx-w*.54)/(w*.48))**2+((yy-h*.47)/(h*.78))**2))
    arr=np.zeros((h,w,3),np.uint8)
    for j,b in enumerate(BG):arr[:,:,j]=np.clip(b+v*(8,18,19)[j],0,255)
    im=Image.fromarray(arr,'RGB').convert('RGBA');d=ImageDraw.Draw(im)
    cx,cy=w*.53,h*.50
    for r in (.27,.39,.52):
        rr=min(w,h)*r;d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),outline=(57,96,106,80),width=1)
    d.line((w*.1,h*.83,w*.9,h*.83),fill=(41,66,77,100),width=1)
    return im

def composed(render,size,zoom=1):
    w,h=size;im=backdrop(size);ratio=min(w/render.width,h/render.height)*zoom
    obj=render.resize((int(render.width*ratio),int(render.height*ratio)),Image.Resampling.LANCZOS)
    im.alpha_composite(obj,((w-obj.width)//2,(h-obj.height)//2))
    return im.convert('RGB')

def export_glb(scene,path):
    """Self-contained glTF 2.0 with named groups, normals, PBR materials and optional animation."""
    chunks=bytearray();views=[];accessors=[]
    def acc(arr,kind,component,target=None):
        arr=np.ascontiguousarray(arr);padding=(-len(chunks))%4;chunks.extend(b'\0'*padding);off=len(chunks);raw=arr.tobytes();chunks.extend(raw)
        view={'buffer':0,'byteOffset':off,'byteLength':len(raw)}
        if target:view['target']=target
        views.append(view);a={'bufferView':len(views)-1,'componentType':component,'count':len(arr),'type':kind}
        if kind in ('VEC3','SCALAR'):
            a['min']=np.atleast_1d(arr.min(0)).tolist();a['max']=np.atleast_1d(arr.max(0)).tolist()
        accessors.append(a);return len(accessors)-1
    buckets={}
    for p in scene.parts:buckets.setdefault((p.color,p.group),[]).append(p)
    nodes=[{'name':'Original schematic / clinician review pending','children':[]}];meshes=[];materials=[];lower=[]
    C=np.array([[1,0,0],[0,0,1],[0,-1,0]],np.float32)
    for (color,group),parts in buckets.items():
        vv=[];nn=[];ff=[];count=0
        for p in parts:
            vv.append(p.vertices@C.T*.1);nn.append(normals(p.vertices,p.faces)@C.T);ff.append(p.faces+count);count+=len(p.vertices)
        v=np.concatenate(vv).astype('<f4');n=np.concatenate(nn).astype('<f4');f=np.concatenate(ff).astype('<u4').ravel()
        pos=acc(v,'VEC3',5126,34962);normal=acc(n,'VEC3',5126,34962);idx=acc(f,'SCALAR',5125,34963)
        mat=len(materials);materials.append({'name':color,'doubleSided':True,'pbrMetallicRoughness':{'baseColorFactor':[*color_rgb(color).tolist(),1],'metallicFactor':.02,'roughnessFactor':.45}})
        meshes.append({'name':group+' '+color,'primitives':[{'attributes':{'POSITION':pos,'NORMAL':normal},'indices':idx,'material':mat}], 'extras':{'anatomicalParts':[p.name for p in parts]}})
        nodes.append({'name':group+' '+color,'mesh':len(meshes)-1})
        (lower if group=='lower-leg' and scene.name=='knee-motion' else nodes[0]['children']).append(len(nodes)-1)
    animations=[]
    if lower:
        nodes.append({'name':'Lower leg schematic hinge','children':lower});motion_node=len(nodes)-1;nodes[0]['children'].append(motion_node)
        time=acc(np.array([0,2,4],dtype='<f4'),'SCALAR',5126)
        a=math.radians(72)/2;rot=acc(np.array([[0,0,0,1],[math.sin(a),0,0,math.cos(a)],[0,0,0,1]],dtype='<f4'),'VEC4',5126)
        animations=[{'name':'Schematic flexion 0–72 degrees, not biomechanics','samplers':[{'input':time,'output':rot,'interpolation':'LINEAR'}],'channels':[{'sampler':0,'target':{'node':motion_node,'path':'rotation'}}]}]
    gltf={'asset':{'version':'2.0','generator':'DoctorHao original parametric medical visuals v1'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':nodes,'meshes':meshes,'materials':materials,'buffers':[{'byteLength':len(chunks)}],'bufferViews':views,'accessors':accessors,'extras':{'reviewStatus':'clinician-review-pending','notForDiagnosis':True,'notes':scene.notes,'sourceGeometry':'original-parametric','anatomicalCompleteness':'simplified'}}
    if animations:gltf['animations']=animations
    js=json.dumps(gltf,ensure_ascii=False,separators=(',',':')).encode();js+=b' '*((-len(js))%4);chunks.extend(b'\0'*((-len(chunks))%4))
    body=struct.pack('<I4s',len(js),b'JSON')+js+struct.pack('<I4s',len(chunks),b'BIN\0')+chunks
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(struct.pack('<4sII',b'glTF',2,12+len(body))+body)
    return {'vertices':sum(len(p.vertices) for p in scene.parts),'triangles':sum(len(p.faces) for p in scene.parts),'parts':len(scene.parts),'bytes':path.stat().st_size}

def save_figure(item,scene,poster,path):
    w,h=1600,1120;im=Image.new('RGB',(w,h),'#f3f6f5');d=ImageDraw.Draw(im)
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc" lang="zh-Hant"><title id="title">{html.escape(item["title"])}</title><desc id="desc">{html.escape(item["alt"]+" "+item["caution"])}</desc><rect width="1600" height="1120" fill="#f3f6f5"/>']
    def rect(x,y,ww,hh,fill,r=0):
        d.rounded_rectangle((x,y,x+ww,y+hh),radius=r,fill=fill)
        svg.append(f'<rect x="{x}" y="{y}" width="{ww}" height="{hh}" rx="{r}" fill="{fill}"/>')
    def text(x,y,value,size=28,fill='#1b3440',bold=False,width=None,lh=None):
        f=font(size,bold);ls=wrap(value,f,width) if width else [value];lineh=lh or round(size*1.5)
        for j,line in enumerate(ls):
            yy=y+j*lineh;d.text((x,yy),line,font=f,fill=fill)
            svg.append(f'<text x="{x}" y="{yy+size+5}" font-family="Noto Sans TC, Noto Sans CJK TC, Microsoft JhengHei, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{fill}">{html.escape(line)}</text>')
        return y+len(ls)*lineh
    rect(0,0,w,12,'#329e99')
    text(65,43,'程皓醫師  /  醫學圖解',25,'#48727b',True)
    rect(1180,43,350,46,'#fff0dd',12);text(1200,44,'示意草稿・待醫師審閱',23,'#815324',True)
    end=text(62,101,item['title'],50,bold=True,width=1460,lh=68)
    text(65,end+8,'3D 結構與閱讀重點｜不是診斷影像，也不是個別治療處方',25,'#61727a')
    art=poster.resize((866,650),Image.Resampling.LANCZOS);im.paste(art,(60,270))
    import io
    b=io.BytesIO();art.save(b,format='WEBP',quality=87,method=5)
    svg.append('<image x="60" y="270" width="866" height="650" href="data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()+'"/>')
    for j,(label,col) in enumerate(scene.structures[:3]):
        y=805+j*34;d.ellipse((83,y+9,96,y+22),fill=col);svg.append(f'<circle cx="89" cy="{y+15}" r="7" fill="{col}"/>');text(110,y,label,21,'#e3eceb')
    for i,p in enumerate(item['points']):
        y=270+i*210
        rect(974,y,566,190,'#ffffff',18)
        rect(994,y+22,45,45,'#d9ece8',12);text(1005,y+23,str(i+1),26,'#237571',True)
        text(1056,y+21,p['heading'],29,bold=True,width=450)
        bottom=text(995,y+75,p['text'],26,width=512,lh=41)
        if bottom>y+190:raise ValueError('Callout overflow '+item['slug'])
    rect(60,941,1480,116,'#e6edeb',16)
    cy=text(81,953,item['caution'],24,'#344e56',width=1435,lh=37)
    if cy>1058:raise ValueError('Caution overflow '+item['slug'])
    names=' / '.join(SOURCES[k][0] for k in item['sourceIds'])
    text(63,1075,'參考：'+names+'　｜　完整來源與限制見素材索引',18,'#5c7278')
    svg.append('</svg>');path.write_text(''.join(svg),encoding='utf-8');im.save(path.with_suffix('.webp'),quality=90,method=5)
    return im

def save_og(item,render,path):
    im=backdrop((1200,630));obj=render.resize((680,680),Image.Resampling.LANCZOS);im.alpha_composite(obj,(550,-25));d=ImageDraw.Draw(im)
    d.text((52,48),'程皓醫師  /  好動人生',font=font(25,True),fill='#9dcacb')
    y=160
    for line in wrap(item['title'],font(44,True),575):d.text((50,y),line,font=font(44,True),fill='#f3eee3');y+=64
    d.text((54,min(y+34,440)),'醫學圖解  ·  3D 示意素材',font=font(22),fill='#8db5b6')
    d.rounded_rectangle((52,544,390,590),radius=11,fill='#263f48');d.text((68,551),'示意草稿・待醫師審閱',font=font(21),fill='#f5c28e')
    im.convert('RGB').save(path,quality=89,optimize=True)

def article_data():
    result={}
    for p in sorted((ROOT/'src/content/articles').glob('*.md')):
        content=p.read_text(encoding='utf-8')
        def value(k):
            m=re.search(r'^'+re.escape(k)+r':\s*(.+)$',content,re.M)
            return m.group(1).strip().strip('"\'') if m else ''
        result[p.stem]={'articleTitle':value('title'),'category':value('category'),'articlePath':p.relative_to(ROOT.parent).as_posix(),'articleSha256':digest(p)}
    return result

def motion_video(renderer,path):
    s=make_scene('knee-motion');frames=OUT/'_motion-frames';frames.mkdir(exist_ok=True)
    for i in range(73):
        a=36-36*math.cos(i*2*math.pi/72);im=composed(renderer.image(s,800,800,angle=a),(960,720),1.0)
        d=ImageDraw.Draw(im);d.text((34,23),'膝屈曲・剛性鉸鏈示意',font=font(26,True),fill='#dfebe7');d.text((34,65),f'{a:04.1f}°  示意角度・不是測量值',font=font(19),fill='#efb888')
        d.text((34,667),'省略韌帶與髕骨軌跡｜不代表真實關節滾滑｜待醫師審閱',font=font(18),fill='#bdcfce')
        im.save(frames/f'{i:04d}.png')
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','18','-i',str(frames/'%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart','-crf','22',str(path)],check=True)
    for p in frames.glob('*.png'):p.unlink()
    frames.rmdir()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true',help='Skip the MP4; useful for local visual iteration.');args=parser.parse_args()
    inventory=article_data();items=briefs()
    if set(inventory)!=set(i['slug'] for i in items):raise RuntimeError('Coverage drift: update the editorial briefs before generating assets.')
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'models').mkdir(exist_ok=True);(OUT/'articles').mkdir(exist_ok=True)
    renderer=Renderer();scenes={};renders={};models={}
    try:
        for key in sorted({i['scene'] for i in items}|{'knee-motion'}):
            scene=make_scene(key);scenes[key]=scene;renders[key]=renderer.image(scene)
            glb=OUT/'models'/f'{key}.glb';stats=export_glb(scene,glb)
            poster=composed(renders[key],(1100,825),1.03);pp=OUT/'models'/f'{key}.webp';poster.save(pp,quality=88,method=5)
            cam=np.array(scene.camera);models[key]={'src':f'/medical-visuals/models/{key}.glb','poster':f'/medical-visuals/models/{key}.webp','notes':scene.notes,'structures':scene.structures,'camera':[float(math.atan2(cam[0],-cam[1])),float(math.atan2(cam[2],np.linalg.norm(cam[:2])))], 'sha256':digest(glb),**stats}
            print('MODEL',key,stats,flush=True)
        contact=[]
        for index,item in enumerate(items):
            item.update(inventory[item['slug']]);key=item['scene'];scene=scenes[key];render=renders[key]
            item['alt']=item['title']+'的原創 3D 示意；'+ '、'.join(t[0] for t in scene.structures)+'。'+scene.notes
            base=OUT/'articles'/item['slug'];base.mkdir(exist_ok=True);public=f'/medical-visuals/articles/{item["slug"]}'
            # Each cover is a scene render, not a reused stock photo; article identity lives in OG and explanations.
            render_article=renderer.image(scene,1100,1100,yaw=(index%3-1)*8)
            cover=composed(render_article,(1600,900),1.09);cover.save(base/'cover.webp',quality=87,method=5)
            for width in (800,480):cover.resize((width,round(width*9/16)),Image.Resampling.LANCZOS).save(base/f'cover-{width}.webp',quality=85,method=5)
            item['cover']=public+'/cover.webp';item['coverSmall']=public+'/cover-480.webp';item['coverMedium']=public+'/cover-800.webp'
            item['figure']=public+'/explain.svg';item['figureRaster']=public+'/explain.webp';item['og']=public+'/og.jpg';item['model']=models[key]['src'];item['poster']=models[key]['poster'];item['modelNotes']=scene.notes;item['structures']=scene.structures;item['camera']=models[key]['camera']
            save_figure(item,scene,composed(render_article,(1100,825),1.03),base/'explain.svg');save_og(item,render_article,base/'og.jpg')
            item['sha256']={p.name:digest(p) for p in sorted(base.iterdir()) if p.is_file()}
            thumb=cover.resize((320,180));panel=Image.new('RGB',(320,244),'#edf2ef');panel.paste(thumb,(0,0));d=ImageDraw.Draw(panel)
            for j,line in enumerate(wrap(item['title'],font(15,True),304)[:2]):d.text((8,188+j*23),line,font=font(15,True),fill='#213d48')
            contact.append(panel);print('ARTICLE',item['slug'],flush=True)
        if not args.quick:motion_video(renderer,OUT/'knee-flexion.mp4')
        manifest={'schemaVersion':1,'generatedOn':REVIEW_DATE,'sourceRevision':os.environ.get('GITHUB_SHA','local-source-audit'),'reviewStatus':'clinician-review-pending','provenance':'Original parametric 3-D geometry and rendered teaching images. No source photographs, video pixels, third-party meshes or patient data were copied.','limitations':'Schematic geometry is not anatomically complete or dimensionally validated. Motion is not a biomechanical simulation. Clinical review is pending.','sources':{k:{'label':label,'url':url,'checkedOn':REVIEW_DATE} for k,(label,url) in SOURCES.items()},'models':models,'articles':{i['slug']:i for i in items}}
        dump(DATA,manifest);dump(OUT/'manifest.json',manifest)
        cols=4;sheet=Image.new('RGB',(cols*320,math.ceil(len(contact)/cols)*244),'#edf2ef')
        for i,p in enumerate(contact):sheet.paste(p,((i%cols)*320,(i//cols)*244))
        sheet.save(OUT/'contact-sheet.jpg',quality=88)
        audit={'articles':len(items),'models':len(models),'perArticleFormats':['cover.webp','cover-800.webp','cover-480.webp','explain.svg','explain.webp','og.jpg'],'reviewStatus':'clinician-review-pending','sourceMarkdownPreserved':all(digest(ROOT.parent/i['articlePath'])==i['articleSha256'] for i in items),'totalAssetBytes':sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())}
        dump(OUT/'build-report.json',audit);print(json.dumps(audit,ensure_ascii=False),flush=True)
    finally:renderer.close()

if __name__=='__main__':main()
