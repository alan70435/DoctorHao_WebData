#!/usr/bin/env python3
"""Build original, parametric adult MSK ultrasound teaching assets.

Not a simulator, diagnostic image generator, patient scan, or calibrated anatomy.
All images are rendered from the same meshes supplied as glTF 2.0 / GLB.
The generated assets never embed photographs or synthetic B-mode sonograms.
"""
from __future__ import annotations
import argparse, base64, hashlib, html, io, json, math, re, shutil
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk, vtk_to_numpy
import trimesh
from PIL import Image
import cairosvg
from catalog import ITEMS, DATE, ESSR, AIUM

BONE='#ede5d4'; MUSCLE='#bc7164'; TENDON='#9bd8cb'; TARGET='#f0b777'
NERVE='#ecd36f'; BLUE='#60c6de'; BACK='#102733'; RED='#cb6d70'; VEIN='#699abf'
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'website/public/medical-visuals/ultrasound'
ARCHIVE=ROOT/'website_blog/medical_3d_assets/ultrasound'
FONT='Noto Sans CJK TC, Noto Sans CJK SC, sans-serif'

@dataclass
class Part:
    name: str
    vertices: np.ndarray
    faces: np.ndarray
    color: str=BONE
    alpha: float=1.0


def unit(v):
    a=np.asarray(v,float); n=np.linalg.norm(a)
    if n<1e-9: raise ValueError('Zero-length axis')
    return a/n


def rgb(c): return tuple(int(c[i:i+2],16)/255 for i in (1,3,5))


def poly(v,f):
    p=vtk.vtkPolyData(); pts=vtk.vtkPoints()
    pts.SetData(numpy_to_vtk(np.asarray(v,np.float32),deep=True));p.SetPoints(pts)
    cells=vtk.vtkCellArray(); a=np.c_[np.full(len(f),3),f].astype(np.int64).ravel()
    cells.SetCells(len(f),numpy_to_vtk(a,deep=True,array_type=vtk.VTK_ID_TYPE));p.SetPolys(cells)
    return p


def clean(p):
    tri=vtk.vtkTriangleFilter();tri.SetInputData(p);tri.Update()
    weld=vtk.vtkCleanPolyData();weld.SetInputConnection(tri.GetOutputPort());weld.Update()
    n=vtk.vtkPolyDataNormals();n.SetInputConnection(weld.GetOutputPort());n.SplittingOff();n.ConsistencyOn();n.AutoOrientNormalsOn();n.Update()
    q=n.GetOutput()
    return vtk_to_numpy(q.GetPoints().GetData()).copy(),vtk_to_numpy(q.GetPolys().GetData()).reshape(-1,4)[:,1:].copy()


def sphere(c,r,axis=None):
    s=vtk.vtkSphereSource();s.SetRadius(1);s.SetThetaResolution(28);s.SetPhiResolution(20);s.Update()
    v,f=clean(s.GetOutput());v=v*np.asarray(r)
    if axis is not None:
        z=unit(axis);x=unit(np.cross(z,[0,1,0] if abs(z[1])<.9 else [1,0,0]));y=np.cross(z,x)
        v=v@np.array([x,y,z])
    return v+np.asarray(c),f


def tube(points,radius=.06):
    pts=vtk.vtkPoints()
    for p in points: pts.InsertNextPoint(*p)
    spline=vtk.vtkParametricSpline();spline.SetPoints(pts)
    source=vtk.vtkParametricFunctionSource();source.SetParametricFunction(spline);source.SetUResolution(max(16,len(points)*8));source.Update()
    t=vtk.vtkTubeFilter();t.SetInputConnection(source.GetOutputPort());t.SetRadius(radius);t.SetNumberOfSides(12);t.CappingOn();t.Update()
    return clean(t.GetOutput())


def organic(spec, cuts=()):
    """A smooth union of ellipsoids, used for original, simplified bone surfaces."""
    a=np.asarray(spec,float);lo=np.min(a[:,:3]-a[:,3:],0)-.12;hi=np.max(a[:,:3]+a[:,3:],0)+.12
    step=float(max(hi-lo)/74);dims=np.ceil((hi-lo)/step).astype(int)+1
    xyz=np.stack(np.meshgrid(*[lo[i]+np.arange(dims[i])*step for i in range(3)],indexing='ij'),-1)
    field=None
    for e in a:
        d=(np.linalg.norm((xyz-e[:3])/e[3:],axis=-1)-1)*min(e[3:])
        field=d if field is None else -.045*np.logaddexp(-field/.045,-d/.045)
    for e in cuts:
        e=np.array(e);d=(np.linalg.norm((xyz-e[:3])/e[3:],axis=-1)-1)*min(e[3:]);field=np.maximum(field,-d)
    image=vtk.vtkImageData();image.SetDimensions(*map(int,dims));image.SetOrigin(*lo);image.SetSpacing(step,step,step)
    image.GetPointData().SetScalars(numpy_to_vtk(field.astype(np.float32).ravel(order='F'),deep=True))
    contour=vtk.vtkFlyingEdges3D();contour.SetInputData(image);contour.SetValue(0,0);contour.Update()
    d=vtk.vtkDecimatePro();d.SetInputConnection(contour.GetOutputPort());d.SetTargetReduction(.65);d.PreserveTopologyOn();d.Update()
    s=vtk.vtkWindowedSincPolyDataFilter();s.SetInputConnection(d.GetOutputPort());s.SetNumberOfIterations(14);s.SetPassBand(.1);s.Update()
    return clean(s.GetOutput())


def box(c,size,basis=None):
    s=vtk.vtkCubeSource();s.SetXLength(size[0]);s.SetYLength(size[1]);s.SetZLength(size[2]);s.Update()
    v,f=clean(s.GetOutput())
    if basis is not None:v=v@np.asarray(basis)
    return v+np.asarray(c),f


def scene(key):
    parts=[]
    def add(name,mesh,color=BONE,alpha=1):
        v,f=mesh;parts.append(Part(name,np.asarray(v,np.float32),np.asarray(f,np.uint32),color,alpha))
    def bone(name,spec,cuts=()):add(name,organic(spec,cuts))
    def tendon(name,points,r=.06,color=TENDON):add(name,tube(points,r),color)
    def muscle(name,a,b,w=.2):
        a,b=np.array(a),np.array(b);add(name,sphere((a+b)/2,(w,w*.62,np.linalg.norm(b-a)/2),b-a),MUSCLE)
    if key=='shoulder':
        v=[[-1.55,.2,1.02],[-1.55,.32,-.86],[.01,.08,.36],[-1.5,.43,1.02],[-1.5,.51,-.86],[.03,.28,.36]]
        f=[[0,2,1],[3,4,5],[0,3,5],[0,5,2],[1,2,5],[1,5,4],[0,1,4],[0,4,3]]
        add('Scapular blade - simplified',(v,f));add('Glenoid surface',sphere((.03,.1,.37),(.12,.34,.4)),TENDON)
        bone('Humerus',[(.62,0,.38,.53,.49,.51),(.9,.04,-.24,.27,.26,.62),(.87,.03,-1.17,.23,.24,.94),(1.0,-.11,.34,.2,.22,.25),(.39,-.36,.23,.13,.17,.17)])
        tendon('Acromion',[(-1.22,.42,.86),(-.45,.23,1.21),(.4,.08,1.23),(.82,-.09,1.02)],.13,BONE)
        tendon('Clavicle - partial',[(-1.66,-.38,1.14),(-.82,-.44,1.25),(-.1,-.2,1.3),(.5,-.18,1.15)],.10,BONE)
        tendon('Supraspinatus tendon',[(-1.17,.12,.96),(-.26,.04,.95),(.54,-.02,.9),(.99,-.09,.52)],.10)
        tendon('Subscapularis tendon',[(-1.2,-.07,.23),(-.45,-.31,.36),(.22,-.48,.3),(.4,-.48,.23)],.13)
        tendon('Infraspinatus tendon',[(-1.17,.49,.2),(-.21,.49,.4),(.68,.52,.44),(.95,.38,.35)],.11)
        tendon('Teres minor tendon',[(-.91,.45,-.37),(-.1,.48,-.04),(.68,.47,.02)],.09)
        muscle('Subscapularis - partial',(-1.37,-.08,.0),(-.56,-.3,.3),.29)
        tendon('Long head of biceps tendon',[(.21,-.11,.85),(.53,-.43,.74),(.71,-.64,.27),(.73,-.66,-.22),(.82,-.44,-1.30)],.047,TARGET)
    elif key=='elbow':
        bone('Humerus',[(0,.06,1.42,.29,.29,1.03),(0,.03,.59,.38,.33,.49),(-.28,.06,.1,.32,.34,.28),(.41,.02,.15,.27,.30,.29),(.69,.01,.3,.16,.21,.19)])
        bone('Radius',[(.52,.0,-.43,.26,.26,.16),(.56,.04,-.70,.15,.15,.24),(.62,.08,-1.47,.13,.14,.69)])
        bone('Ulna',[(-.2,.2,-.45,.24,.25,.36),(-.2,.42,.02,.2,.23,.31),(-.25,.07,-1.33,.16,.17,.81)])
        tendon('Common extensor tendon',[(.69,-.11,.28),(.82,-.17,-.13),(.92,-.15,-.73),(.99,-.04,-1.40)],.095,TARGET)
        muscle('Extensor muscle mass - partial',(.99,-.01,-.68),(1.01,.0,-1.62),.24)
        tendon('Lateral collateral complex - simplified',[(.61,.11,.26),(.69,.19,-.39),(.43,.23,-.69)],.045)
        tendon('Common flexor tendon',[(-.54,-.04,.23),(-.60,-.15,-.37),(-.68,-.12,-1.24)],.09)
        tendon('Triceps tendon',[(0,.47,1.55),(-.05,.55,.60),(-.16,.47,.17)],.12)
        tendon('Ulnar nerve',[(-.54,.3,.96),(-.58,.38,.28),(-.53,.32,-.44),(-.6,.27,-1.1)],.03,NERVE)
    elif key=='wrist':
        bone('Distal radius',[(-.32,.05,1.18,.22,.2,.7),(-.38,.03,.44,.37,.25,.34)])
        bone('Distal ulna',[(.54,.06,1.14,.14,.14,.78),(.55,.03,.43,.2,.19,.23)])
        carpals=[('Scaphoid',(-.64,.0,-.24),(.25,.24,.29)),('Lunate',(-.14,.04,-.31),(.24,.24,.22)),('Triquetrum',(.33,.05,-.26),(.25,.22,.21)),('Pisiform',(.66,-.29,-.22),(.16,.15,.17)),('Trapezium',(-.76,-.01,-.8),(.22,.23,.24)),('Trapezoid',(-.34,.02,-.84),(.18,.22,.2)),('Capitate',(.04,.01,-.74),(.22,.23,.32)),('Hamate',(.47,.03,-.75),(.24,.22,.25))]
        for name,c,r in carpals:add(name,sphere(c,r))
        add('Hook of hamate',sphere((.53,-.26,-.76),(.08,.18,.13)))
        for i,x in enumerate([-.86,-.4,-.03,.32,.64]):tendon('Metacarpal '+str(i+1)+' - partial',[(x,0,-1.02),(x*1.2,0,-1.71)],.07,BONE)
        for layer,y in [('FDS',-.60),('FDP',-.40)]:
            for i,x in enumerate([-.34,-.1,.14,.38]):
                tendon(f'{layer} tendon {i+1}',[(x,y+.05,1.25),(x,y,-.26),(x*1.15,y+.04,-1.38)],.072)
        tendon('FPL tendon',[(-.6,-.50,1.16),(-.6,-.52,-.34),(-.8,-.43,-1.4)],.072)
        tendon('Median nerve',[(-.25,-.72,1.35),(-.25,-.78,-.25),(-.2,-.77,-.96)],.055,TARGET)
        # An open, translucent retinacular roof: nine flexor tendons + median nerve below it.
        v=[];f=[]
        for z in [-.15,-.65]:
            for x in np.linspace(-.72,.7,21):v.append([x,-.40-.60*(1-(x/.76)**2),z])
        for i in range(20):f.extend([[i,i+1,i+21],[i+1,i+22,i+21]])
        add('Flexor retinaculum - transparent teaching roof',(v,f),BLUE,.3)
    elif key=='hip':
        bone('Hemipelvis - partial', [(-.55,.22,1.11,.28,.65,.83),(-.50,.22,.43,.34,.42,.44),(-.7,.32,-.16,.21,.34,.47)],[(.03,.06,.4,.44,.5,.49)])
        bone('Femur',[(.13,.02,.38,.43,.42,.43),(.51,.07,.06,.47,.23,.26),(.98,.1,-.02,.24,.29,.3),(.89,.1,-.61,.23,.23,.49),(.84,.12,-1.33,.21,.22,.62),(.56,.3,-.52,.16,.2,.19)])
        # Anterior capsular bands depict a boundary, not fluid, and are not a solid extra bone.
        for i,x in enumerate(np.linspace(-.06,.89,8)):
            z=.51-.7*(x+.06)
            tendon('Anterior capsule band '+str(i+1),[(x,-.3,z+.07),(x,-.45,z-.03),(x+.05,-.4,z-.20)],.018,BLUE)
        muscle('Iliopsoas - partial',(-.26,-.51,1.6),(.04,-.65,.63),.25)
        tendon('Iliopsoas tendon',[(-.01,-.61,1.14),(.14,-.65,.57),(.35,-.57,.06),(.53,-.20,-.4),(.56,.22,-.54)],.072)
        for name,x,col in [('Femoral nerve',-.94,NERVE),('Femoral artery',-1.13,RED),('Femoral vein',-1.34,VEIN)]:
            tendon(name,[(x,-.46,1.25),(x-.02,-.55,.36),(x+.10,-.51,-.55)],.047 if 'nerve' in name else .067,col)
        muscle('Gluteus medius - partial',(-.47,.51,1.54),(.96,.29,.10),.3)
    elif key=='knee':
        bone('Femur',[(0,.05,1.91,.3,.31,1.04),(0,.06,.96,.48,.40,.53),(-.38,.08,.41,.37,.48,.37),(.38,.08,.41,.37,.48,.37)],[(0,.31,.24,.14,.45,.28)])
        bone('Tibia',[(0,.07,-1.49,.26,.26,.84),(0,.07,-.61,.45,.36,.36),(-.33,.04,-.32,.33,.41,.16),(.33,.04,-.32,.33,.41,.16),(0,-.4,-.95,.13,.15,.19)])
        bone('Fibula',[(.85,.19,-.65,.14,.17,.23),(.81,.18,-1.44,.08,.1,.66)])
        for x in [-.35,.35]:add('Tibial articular surface '+str(x),sphere((x,0,-.14),(.33,.4,.04)),TENDON)
        add('Patella - anatomical position',sphere((0,-.78,.47),(.29,.18,.36)))
        tendon('Quadriceps tendon',[(0,-.45,2.15),(0,-.64,1.5),(0,-.79,.81)],.14)
        tendon('Patellar tendon',[(0,-.80,.15),(0,-.77,-.34),(0,-.63,-.7),(0,-.47,-.96)],.12,TARGET)
        tendon('Medial collateral ligament',[(-.72,.01,.55),(-.83,.02,-.24),(-.61,-.04,-.99)],.065)
        tendon('Lateral collateral ligament',[(.69,.07,.49),(.84,.17,-.64)],.042)
    elif key=='ankle':
        bone('Tibia',[(0,.01,1.54,.26,.27,.94),(-.05,.01,.57,.34,.32,.31),(-.29,.0,.28,.14,.22,.25)])
        bone('Fibula',[(.56,.12,1.35,.10,.13,1.02),(.57,.08,.23,.15,.17,.26)])
        add('Talus',sphere((0,-.03,.12),(.36,.41,.25)))
        add('Calcaneus',sphere((0,.35,-.43),(.33,.58,.28)))
        for i in range(3):add('Midfoot bone '+str(i+1),sphere((-.28+i*.28,-.56,-.23),(.2,.28,.18)))
        for i in range(5):tendon('Metatarsal '+str(i+1)+' - partial',[(-.42+i*.21,-.7,-.24),(-.48+i*.24,-1.48,-.31)],.048,BONE)
        muscle('Soleus - partial',(0,.48,2.47),(0,.68,1.32),.30)
        tendon('Achilles tendon',[(0,.72,1.84),(0,.86,1.23),(0,.88,.64),(0,.8,.02),(0,.67,-.34)],.105,TARGET)
        tendon('Anterior talofibular ligament',[(.58,-.01,.22),(.35,-.33,.02)],.04)
        tendon('Calcaneofibular ligament',[(.59,.14,.22),(.3,.43,-.44)],.04)
    else:raise ValueError(key)
    return parts


def with_probe(parts,item,mode):
    parts=list(parts);n=unit(item['normal']);u=unit(item['axis_vector']);p=np.array(item['contact'])
    if mode=='short':
        u=unit({'shoulder':(1,0,0),'elbow':(0,-1,0),'wrist':(-1,0,0),'hip':(.6,0,.8),'knee':(1,0,0),'ankle':(1,0,0)}[item['id']])
    v=unit(np.cross(n,u));basis=[u,v,n]
    def add(name,mesh,c,a=1):parts.append(Part(name,*mesh,c,a))
    add('Local skin contact patch - surrounding skin omitted',box(p-.055*n,(1.15,.66,.09),basis),'#b28f83',.48)
    add('Transducer acoustic face',box(p+.02*n,(.91,.19,.04),basis),BLUE)
    add('Transducer head',box(p+.12*n,(.92,.23,.18),basis),'#e4ebeb')
    add('Transducer body',box(p+.35*n,(.65,.30,.31),basis),'#b9cbd0')
    add('Transducer grip',sphere(p+.62*n,(.23,.15,.30),n),'#dce6e8')
    add('Orientation marker - chosen display convention',sphere(p+.39*u+.15*n,(.055,.055,.055)),TARGET)
    add('Probe cable - schematic',tube([p+.88*n,p+1.12*n+.08*v,p+1.3*n+.3*v],.035),'#869da6')
    q=np.array([p-.43*u,p+.43*u,p+.43*u-.92*n,p-.43*u-.92*n])
    add('Illustrative imaging plane - not a simulated sonogram',(q,np.array([[0,1,2],[0,2,3]])),BLUE,.19)
    add('Imaging plane border',tube([q[0],q[1],q[2],q[3],q[0]],.006),BLUE,.8)
    return parts


def render(parts,item,size,focus=None,scale=None):
    renderer=vtk.vtkRenderer();renderer.SetBackground(*rgb(BACK));renderer.SetUseDepthPeeling(True)
    renderer.SetMaximumNumberOfPeels(80);renderer.SetOcclusionRatio(.1)
    win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetAlphaBitPlanes(1);win.SetMultiSamples(0);win.AddRenderer(renderer);win.SetSize(*size)
    for part in parts:
        normal=vtk.vtkPolyDataNormals();normal.SetInputData(poly(part.vertices,part.faces));normal.SplittingOff();normal.ConsistencyOn();normal.AutoOrientNormalsOn();normal.Update()
        mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(normal.GetOutputPort())
        actor=vtk.vtkActor();actor.SetMapper(mapper);prop=actor.GetProperty()
        prop.SetColor(*rgb(part.color));prop.SetOpacity(part.alpha);prop.SetInterpolationToPhong();prop.SetAmbient(.18);prop.SetDiffuse(.78);prop.SetSpecular(.20);prop.SetSpecularPower(28)
        renderer.AddActor(actor)
    verts=np.concatenate([p.vertices for p in parts]);center=(verts.min(0)+verts.max(0))/2 if focus is None else np.array(focus)
    cam=renderer.GetActiveCamera();direction=unit(item['camera']);cam.SetPosition(*(center+direction*16));cam.SetFocalPoint(*center);cam.SetViewUp(0,0,1);cam.ParallelProjectionOn()
    renderer.ResetCamera()
    # ResetCamera changes the focal point; restore the deliberately chosen crop.
    cam.SetFocalPoint(*center);cam.SetPosition(*(center+direction*16))
    cam.SetParallelScale(float(scale if scale is not None else max(verts.max(0)-verts.min(0))*.56))
    renderer.ResetCameraClippingRange();win.Render()
    capture=vtk.vtkWindowToImageFilter();capture.SetInput(win);capture.SetInputBufferTypeToRGB();capture.ReadFrontBufferOff();capture.Update()
    arr=vtk_to_numpy(capture.GetOutput().GetPointData().GetScalars()).reshape(size[1],size[0],3)[::-1].copy()
    marks=[]
    for point in item['points']:
        renderer.SetWorldPoint(*point,1);renderer.WorldToDisplay();x,y,_=renderer.GetDisplayPoint();marks.append((x,size[1]-y))
    win.Finalize();return Image.fromarray(arr),marks


def export_glb(parts,path,item,mode):
    model=trimesh.Scene()
    for i,p in enumerate(parts):
        # Convert local Z-up modeling coordinates to glTF Y-up without reflection.
        vv=np.c_[p.vertices[:,0],p.vertices[:,2],-p.vertices[:,1]]
        mesh=trimesh.Trimesh(vertices=vv,faces=p.faces,process=False)
        rgba=[int(round(x*255)) for x in rgb(p.color)]+[int(round(p.alpha*255))]
        mat=trimesh.visual.material.PBRMaterial(name=p.name,baseColorFactor=rgba,metallicFactor=0,roughnessFactor=.54,alphaMode='BLEND' if p.alpha<1 else 'OPAQUE',doubleSided=True)
        mesh.visual=trimesh.visual.TextureVisuals(material=mat)
        model.add_geometry(mesh,node_name=p.name,geom_name=f'{i:02d}-{p.name}')
    model.metadata={'reviewStatus':'needs-clinician-review','anatomicalAccuracy':'simplified-conceptual','units':'arbitrary-not-for-measurement','region':item['id'],'probeAxis':mode,'syntheticSonogram':False}
    path.write_bytes(model.export(file_type='glb'))


def text(x,y,s,size=24,color='#e8eff1',weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{html.escape(s)}</text>'


def embed(im,x,y,w,h):
    b=io.BytesIO();im.save(b,format='PNG',optimize=True)
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}"/>'


def card(item,index,base,marks,long,short):
    title=f"{item['name']}超音波｜{item['target']}"
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1800" height="1200" viewBox="0 0 1800 1200" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(item["summary"])} 長短軸探頭位置由同一組三維網格渲染；非病人影像，待醫師審閱。</desc>',f'<rect width="1800" height="1200" fill="#071721"/><g font-family="{FONT}">']
    s.extend([text(60,62,'DOCTOR HAO  /  MSK ULTRASOUND ATLAS',20,'#86b8c8',600),text(60,132,item['name']+'超音波',53,weight=700),text(60,186,item['target'],28,'#b6d4dd'),text(1510,72,f'{index:02d} / 06',27,'#b6d4dd'),text(1490,125,item['english'],25,'#86b8c8',600)])
    s.append('<path d="M60 215H1740" stroke="#355562"/><rect x="50" y="240" width="800" height="705" rx="20" fill="#102733"/><rect x="880" y="240" width="870" height="705" rx="20" fill="#102733"/>')
    s.extend([text(76,281,'A  關鍵解剖・立體透視示意',24,'#c9e2e7',600),text(906,281,'B  探頭位置・同一視窗的兩個切面',24,'#c9e2e7',600),embed(base,65,295,770,630)])
    used=[]
    for i,((x,y),label) in enumerate(zip(marks,item['labels'])):
        xx=65+x*770/base.width; yy=295+y*630/base.height
        dx,dy=[(25,30),(65,0),(38,-30),(-55,-40)][i];bx,by=xx+dx,yy+dy
        for a,b in used:
            if math.hypot(bx-a,by-b)<48: bx+=48;by-=18
        used.append((bx,by))
        s.append(f'<path d="M{xx:.1f} {yy:.1f}L{bx:.1f} {by:.1f}" stroke="#f5d5a3" stroke-width="2"/><circle cx="{bx:.1f}" cy="{by:.1f}" r="16" fill="#071721" stroke="#f5d5a3" stroke-width="2"/>')
        s.append(text(round(bx-6),round(by+7),str(i+1),20,'#f5d5a3',600))
    s.extend([text(906,326,'長軸  LONG AXIS',25,'#f5d5a3',600),text(1332,326,'短軸  SHORT AXIS',25,'#f5d5a3',600),embed(long,898,341,405,356),embed(short,1324,341,405,356)])
    s.extend([text(911,730,'探頭長邊平行'+item['axis'],21),text(1337,730,'探頭長邊垂直'+item['axis'],21),text(911,765,'標記：'+item['long_marker'],22,'#9cbfca'),text(1337,765,'標記：'+item['short_marker'],22,'#9cbfca')])
    s.append('<path d="M909 795H1720" stroke="#355562"/>')
    s.append(text(910,831,'病人擺位',23,'#c9e2e7',600))
    for i,line in enumerate(item['position']):s.append(text(910,870+i*35,line,24))
    for i,label in enumerate(item['labels']):s.append(text(75+(i%2)*395,986+(i//2)*41,f'{i+1:02d}  {label}',24,'#d6e6e9'))
    s.append(text(904,985,'定位提醒',22,'#f5d5a3',600))
    for i,line in enumerate(item['caution']):s.append(text(904,1019+i*32,line,19,'#bed1d8'))
    s.append('<path d="M60 1080H1740" stroke="#355562"/>')
    s.extend([text(60,1114,'教育用概念模型・非比例・非診斷影像・待醫師審閱',23,'#f5d5a3',600),text(60,1147,'青色為切面示意，並非聲學模擬；僅保留局部皮膚接觸片。方向標記為本系列約定，須與設備設定核對。',20,'#9cbfca'),text(60,1180,f'參考：ESSR {item["english"].title()} Technical Guidelines；AIUM 2023  |  {DATE}  |  {item["id"]}',18,'#8aaab6')])
    return ''.join(s)+'</g></svg>\n'


def write_json(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--only',choices=[x['id'] for x in ITEMS]);parser.add_argument('--no-integrate',action='store_true');args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True);ARCHIVE.mkdir(parents=True,exist_ok=True)
    records=[]
    for index,item in enumerate(ITEMS,1):
        if args.only and item['id']!=args.only:continue
        print('Rendering',item['id'],flush=True);parts=scene(item['id'])
        base,marks=render(parts,item,(1000,820))
        views={};modelnames={}
        for mode in ['long','short']:
            pp=with_probe(parts,item,mode);view,_=render(pp,item,(680,598),focus=np.asarray(item['focus'])+.26*np.asarray(item['normal']),scale=1.31 if item['id']!='hip' else 1.50)
            views[mode]=view
            glb=f'{item["id"]}-{mode}.glb';export_glb(pp,OUT/glb,item,mode);modelnames[mode]=glb
            poster,_=render(pp,item,(1100,825));poster.save(OUT/f'{item["id"]}-{mode}-poster.webp','WEBP',quality=85,method=6)
        svg=card(item,index,base,marks,views['long'],views['short']);name=item['id']+'-anatomy-probe'
        (OUT/(name+'.svg')).write_text(svg,encoding='utf-8');shutil.copy2(OUT/(name+'.svg'),ARCHIVE/(name+'.svg'))
        png=cairosvg.svg2png(bytestring=svg.encode());(OUT/(name+'.png')).write_bytes(png)
        Image.open(io.BytesIO(png)).convert('RGB').save(OUT/(name+'.webp'),'WEBP',quality=90,method=6)
        camera=item['camera'];orbit=[round(math.atan2(camera[0],-camera[1]),5),round(math.atan2(camera[2],math.hypot(camera[0],camera[1])),5)]
        files=[name+'.svg',name+'.png',name+'.webp']+[f'{item["id"]}-{m}{s}' for m in ['long','short'] for s in ['.glb','-poster.webp']]
        records.append({'id':item['id'],'name':item['name'],'target':item['target'],'alt':item['summary'],'position':item['position'],'windows':item['windows'],'caution':item['caution'],'models':modelnames,'camera':orbit,'image':name+'.webp','svg':name+'.svg','png':name+'.png','reviewStatus':'needs-clinician-review','references':[{'url':ESSR+item['id']+'.pdf','locator':item['reference_pages']},{'url':AIUM,'year':2023}],'files':[{'path':f,'sha256':sha(OUT/f),'bytes':(OUT/f).stat().st_size} for f in files]})
    if not args.only:
        manifest={'schemaVersion':1,'created':DATE,'scope':'Six adult regions, one representative window per region, long and short axes. Not a complete clinical examination.','clinicalReview':{'status':'needs-clinician-review','reviewedBy':None},'imageSize':[1800,1200],'containsPatientData':False,'containsSyntheticSonograms':False,'items':records}
        write_json(OUT/'manifest.json',manifest)
        from publish import publish
        publish(ROOT,OUT,ARCHIVE,manifest,integrate=not args.no_integrate)
        print('Built 6 cards, 12 GLB models, 12 posters, metadata and article integration.',flush=True)

if __name__=='__main__':main()
