"""Original parametric teaching models. Not patient-specific or biomechanical models.

Coordinates: X transverse, Y posterior, Z superior. Art is deliberately simplified.
No anatomy scans, third-party meshes, logos, photographs, or reference-video pixels.
"""
from dataclasses import dataclass, field
from functools import lru_cache
import math
import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk, vtk_to_numpy

BONE = '#eee5d3'
TEAL = '#49bdb4'
DEEP = '#258985'
MUSCLE = '#bb7564'
TENDON = '#c7ddd2'
ORANGE = '#f2a066'
NERVE = '#edc877'
BLUE = '#5596b7'
INK = '#203c48'
WHITE = '#f8f1e4'

@dataclass
class Part:
    name: str
    vertices: np.ndarray
    faces: np.ndarray
    color: str = BONE
    group: str = 'static'

@dataclass
class Scene:
    name: str
    parts: list = field(default_factory=list)
    structures: list = field(default_factory=list)
    camera: tuple = (7, -13, 5)
    notes: str = '結構經簡化與放大，比例不供量測。'
    def add(self, name, mesh, color=BONE, group='static'):
        v, f = cleaned(*mesh)
        self.parts.append(Part(name, np.asarray(v, dtype=np.float32), np.asarray(f, dtype=np.uint32), color, group))
    def bounds(self):
        v = np.concatenate([p.vertices for p in self.parts])
        return np.array([v.min(0), v.max(0)])

def unit(v):
    v = np.asarray(v, float)
    return v / max(float(np.linalg.norm(v)), 1e-9)

def color_rgb(c):
    return np.array([int(c[i:i+2], 16) / 255 for i in (1, 3, 5)])

def uv_surface(fun, nu=40, nv=28, u=(0, 2*math.pi), v=(0, math.pi)):
    us, vs = np.linspace(*u, nu+1), np.linspace(*v, nv+1)
    vertices = np.array([fun(a,b) for a in us for b in vs])
    faces = []
    for i in range(nu):
        for j in range(nv):
            k=i*(nv+1)+j
            faces.extend([[k,k+nv+1,k+1],[k+1,k+nv+1,k+nv+2]])
    return vertices, np.array(faces, np.uint32)

def ellipsoid(center, radius, detail=32, axis=None, ripple=0):
    c, r = np.array(center), np.array(radius)
    def fun(u,v):
        k=1+ripple*(math.sin(9*u+3*math.cos(5*v))*math.sin(7*v))
        return [r[0]*math.cos(u)*math.sin(v)*k, r[1]*math.sin(u)*math.sin(v)*k, r[2]*math.cos(v)*k]
    verts, faces=uv_surface(fun, detail, max(16,detail//2))
    # Reverse the UV grid winding to make the outer surface front-facing.
    faces=faces[:,[0,2,1]]
    if axis is not None:
        z=unit(axis); x=unit(np.cross([0,1,0] if abs(z[1])<.9 else [1,0,0],z)); y=np.cross(z,x)
        verts=verts @ np.array([x,y,z])
    return verts+c, faces

def tube(points, radius, sides=16, smooth=True, elliptical=1):
    pts=np.asarray(points,float)
    rad=np.full(len(pts),radius) if np.isscalar(radius) else np.asarray(radius,float)
    if smooth and len(pts)>2:
        pp=np.vstack([pts[0],pts,pts[-1]]); rr=np.r_[rad[0],rad,rad[-1]]
        out=[]; rout=[]
        for i in range(1,len(pp)-2):
            for t in np.linspace(0,1,9,endpoint=False):
                p0,p1,p2,p3=pp[i-1:i+3]
                out.append(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t**3))
                rout.append((1-t)*rr[i]+t*rr[i+1])
        pts=np.vstack([out,pts[-1]]);rad=np.r_[rout,rad[-1]]
    vertices=[]; tangents=np.gradient(pts,axis=0)
    lastx=None
    for p,t,r in zip(pts,tangents,rad):
        z=unit(t)
        ref=[0,0,1] if abs(z[2])<.9 else [0,1,0]
        x=unit(np.cross(z,ref)) if lastx is None else unit(lastx-z*np.dot(z,lastx))
        if np.linalg.norm(x)<.1: x=unit(np.cross(z,ref))
        y=np.cross(z,x);lastx=x
        for a in np.linspace(0,2*np.pi,sides,endpoint=False):
            vertices.append(p+r*(np.cos(a)*x+elliptical*np.sin(a)*y))
    faces=[]
    for j in range(len(pts)-1):
        for k in range(sides):
            a=j*sides+k;b=j*sides+(k+1)%sides
            faces.extend([[a,b,a+sides],[b,b+sides,a+sides]])
    vertices.extend([pts[0],pts[-1]]); a,b=len(vertices)-2,len(vertices)-1
    for k in range(sides):
        faces.extend([[a,(k+1)%sides,k],[b,(len(pts)-1)*sides+k,(len(pts)-1)*sides+(k+1)%sides]])
    return np.array(vertices),np.array(faces,np.uint32)

def torus(center, radii, thickness, start=0, end=2*np.pi):
    c=np.array(center)
    points=[c+np.array([radii[0]*np.cos(t),radii[1]*np.sin(t),0]) for t in np.linspace(start,end,49)]
    return tube(points,thickness,smooth=False,elliptical=.65)

def meniscus_wedge(center,radii,start,end):
    c=np.array(center);verts=[];N=56
    # Thin inner edge, thicker peripheral rim, tapered horns; not a torus.
    profile=[(.52,.018),(1.0,.018),(1.0,.145),(.55,.040)]
    for i,t in enumerate(np.linspace(start,end,N+1)):
        taper=.20+.80*math.sin(math.pi*i/N)**.4
        for radius,z in profile:
            rr=1-(1-radius)*taper
            verts.append(c+[radii[0]*rr*math.cos(t),radii[1]*rr*math.sin(t),z*taper])
    faces=[]
    for i in range(N):
        for k in range(4):
            a=i*4+k;b=i*4+(k+1)%4
            faces.extend([[a,b,a+4],[b,b+4,a+4]])
    faces.extend([[0,2,1],[0,3,2],[N*4,N*4+1,N*4+2],[N*4,N*4+2,N*4+3]])
    return np.array(verts),np.array(faces,np.uint32)

def box(center, size):
    c=np.array(center);s=np.array(size)/2
    v=np.array([[x,y,z] for x in (-1,1) for y in (-1,1) for z in (-1,1)])*s+c
    f=np.array([[0,1,3],[0,3,2],[4,6,7],[4,7,5],[0,4,5],[0,5,1],[2,3,7],[2,7,6],[0,2,6],[0,6,4],[1,5,7],[1,7,3]])
    return v,f

def transform(mesh, scale=1, offset=(0,0,0), angle=0, axis='z'):
    v,f=mesh;v=np.array(v)*scale
    c,s=np.cos(angle),np.sin(angle)
    M={'x':[[1,0,0],[0,c,-s],[0,s,c]],'y':[[c,0,s],[0,1,0],[-s,0,c]],'z':[[c,-s,0],[s,c,0],[0,0,1]]}[axis]
    return v@np.array(M).T+np.array(offset),f

def poly_mesh(v,f):
    poly=vtk.vtkPolyData();points=vtk.vtkPoints();points.SetData(numpy_to_vtk(np.asarray(v,dtype=np.float32),deep=True));poly.SetPoints(points)
    cells=vtk.vtkCellArray();arr=np.column_stack([np.full(len(f),3),f]).astype(np.int64).ravel();cells.SetCells(len(f),numpy_to_vtk(arr,deep=True,array_type=vtk.VTK_ID_TYPE));poly.SetPolys(cells)
    return poly

def cleaned(vertices,faces):
    v=np.asarray(vertices,dtype=np.float32);f=np.asarray(faces,dtype=np.int64)
    # Weld the UV seam/poles before computing glTF vertex normals.
    v,inv=np.unique(np.round(v,6),axis=0,return_inverse=True);f=inv[f]
    area=np.linalg.norm(np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]]),axis=1)
    f=f[area>1e-10]
    ids,inv=np.unique(f,return_inverse=True);v=v[ids];f=inv.reshape(-1,3)
    n=vtk.vtkPolyDataNormals();n.SetInputData(poly_mesh(v,f));n.SplittingOff();n.ConsistencyOn();n.AutoOrientNormalsOn();n.Update()
    poly=n.GetOutput()
    return vtk_to_numpy(poly.GetPoints().GetData()).copy(),vtk_to_numpy(poly.GetPolys().GetData()).reshape(-1,4)[:,1:].copy()

def normals(v,f):
    n=vtk.vtkPolyDataNormals();n.SetInputData(poly_mesh(v,f));n.SplittingOff();n.ConsistencyOn();n.AutoOrientNormalsOn();n.Update()
    return vtk_to_numpy(n.GetOutput().GetPointData().GetNormals()).astype(np.float32)

@lru_cache(maxsize=32)
def organic(spec, subtract=()):
    """Smooth union of ellipsoidal signed-distance primitives, with optional notch."""
    centers=np.array([e[:3] for e in spec]);radii=np.array([e[3:] for e in spec])
    lo=np.min(centers-radii,0)-.12;hi=np.max(centers+radii,0)+.12
    spacing=max(hi-lo)/100
    dims=np.ceil((hi-lo)/spacing).astype(int)+1
    xyz=np.stack(np.meshgrid(*[lo[i]+np.arange(dims[i])*spacing for i in range(3)],indexing='ij'),-1)
    field=None
    for e in spec:
        c=np.array(e[:3]);r=np.array(e[3:]);d=(np.linalg.norm((xyz-c)/r,axis=-1)-1)*min(r)
        field=d if field is None else -.055*np.logaddexp(-field/.055,-d/.055)
    for e in subtract:
        c=np.array(e[:3]);r=np.array(e[3:]);d=(np.linalg.norm((xyz-c)/r,axis=-1)-1)*min(r)
        field=np.maximum(field,-d)
    image=vtk.vtkImageData();image.SetDimensions(*map(int,dims));image.SetOrigin(*lo);image.SetSpacing(spacing,spacing,spacing)
    image.GetPointData().SetScalars(numpy_to_vtk(field.ravel(order='F').astype(np.float32),deep=True))
    contour=vtk.vtkFlyingEdges3D();contour.SetInputData(image);contour.SetValue(0,0);contour.Update()
    dec=vtk.vtkDecimatePro();dec.SetInputConnection(contour.GetOutputPort());dec.SetTargetReduction(.72);dec.PreserveTopologyOn();dec.Update()
    smooth=vtk.vtkWindowedSincPolyDataFilter();smooth.SetInputConnection(dec.GetOutputPort());smooth.SetNumberOfIterations(22);smooth.SetPassBand(.075);smooth.Update()
    p=smooth.GetOutput();v=vtk_to_numpy(p.GetPoints().GetData()).copy();f=vtk_to_numpy(p.GetPolys().GetData()).reshape(-1,4)[:,1:].copy()
    return v,f

def muscle(scene,name,start,end,width,color=MUSCLE, fibers=9):
    start,end=np.array(start,float),np.array(end,float);center=(start+end)/2;axis=end-start
    scene.add(name,ellipsoid(center,(width,width*.65,np.linalg.norm(axis)/2),32,axis),color)
    z=unit(axis);x=unit(np.cross(z,[0,1,0]));y=np.cross(z,x)
    for i in range(fibers):
        angle=2*np.pi*i/fibers
        points=[]
        for t in np.linspace(.05,.95,17):
            off=(x*np.cos(angle)+y*.65*np.sin(angle))*width*np.sin(np.pi*t)*1.012
            points.append(start+(end-start)*t+off)
        scene.add(name+' / fiber '+str(i+1),tube(points,.009,sides=5,smooth=False),TENDON if color==MUSCLE else TEAL)

def add_knee(s,variant):
    s.camera=(7,-13,4)
    s.structures=[['股骨・脛骨・腓骨',BONE],['關節軟骨・半月板',TEAL],['關注區（非分級）',ORANGE]]
    femur=organic(((0,.07,2.45,.34,.34,1.7),(0,.01,1.18,.54,.43,.75),(-.48,.08,.52,.46,.62,.48),(.48,.08,.52,.45,.59,.47)),((0,.36,.25,.19,.72,.37),))
    tibia=organic(((0,.07,-2.25,.3,.3,1.6),(0,.04,-.69,.55,.47,.6),(-.42,.01,-.38,.43,.53,.2),(.42,.01,-.38,.42,.51,.2)))
    fibula=organic(((.96,.14,-.74,.17,.21,.26),(.88,.16,-2.2,.105,.12,1.38)))
    s.add('Femur',femur);s.add('Tibia',tibia,group='lower-leg');s.add('Fibula',fibula,group='lower-leg')
    for side in (-1,1):
        x=side*.47
        # Separate thin tibial surface and crescent meniscus, not a single "cartilage disc".
        s.add(('Medial' if side<0 else 'Lateral')+' tibial articular surface',ellipsoid((x,0,-.18),(.43,.49,.045)),TEAL,'lower-leg')
        start,end=(.50,2*np.pi-.50) if side<0 else (-2.70,2.70)
        ring=meniscus_wedge((x,0,-.08),(.41,.49),start,end)
        s.add(('Medial' if side<0 else 'Lateral')+' meniscus',ring,ORANGE if variant=='meniscus' and side<0 else DEEP,'lower-leg')
        # Inferior condylar cartilage patch, curved rather than a cylinder.
        patch=uv_surface(lambda u,v:[x+.47*np.cos(u)*np.sin(v),.08+.62*np.sin(u)*np.sin(v),.52+.49*np.cos(v)],32,12,v=(np.pi*.56,np.pi))
        s.add('Femoral condyle cartilage '+str(side),(patch[0],patch[1][:,[0,2,1]]),ORANGE if variant=='oa' and side<0 else TEAL)
    exploded=variant in ('acl','meniscus','overview','mcl','pes')
    py=-1.28 if exploded else -.76
    s.add('Patella'+(' (displaced for visibility)' if exploded else ''),ellipsoid((0,py,.58),(.31,.19,.39)),BONE)
    s.add('Patellar tendon',tube([(0,py,.25),(0,-.69,-.45),(0,-.44,-1)], [.13,.13,.08],elliptical=.22),ORANGE if variant=='patellar' else TENDON)
    if variant!='motion':
        s.add('Anterior cruciate ligament',tube([(.24,.30,.66),(.07,.03,.28),(-.16,-.18,-.15)],[.09,.075,.095]),ORANGE if variant=='acl' else TENDON)
        s.add('Posterior cruciate ligament',tube([(-.18,-.12,.6),(-.07,.23,.23),(.12,.32,-.2)], [.08,.07,.08]),DEEP)
        s.add('Medial collateral ligament',tube([(-.89,.0,.73),(-.98,-.02,-.20),(-.67,-.08,-1.0)],[.13,.15,.12],elliptical=.3),ORANGE if variant=='mcl' else TENDON)
        s.add('Lateral collateral ligament',tube([(.87,.04,.63),(.97,.12,-.7)],.055),TENDON)
    if variant=='pes':
        s.add('Pes anserine bursa (enlarged)',ellipsoid((-.64,-.43,-1.12),(.26,.08,.19)),ORANGE,'lower-leg')
        for i,name in enumerate(['Sartorius tendon','Gracilis tendon','Semitendinosus tendon']):
            s.add(name,tube([(-1.02-.16*i,.24+.17*i,1.65),(-1.11-.10*i,.13,-.25),(-.75,-.49,-.9),(-.47,-.51,-1.19-i*.04)],.034),TENDON)
    if variant=='oa':
        for i in range(6):
            a=i*.7
            s.add('Illustrative marginal bone change '+str(i),ellipsoid((-.49+.46*np.cos(a),.52*np.sin(a),-.27),(.10,.10,.10),20),BONE,'lower-leg')
    s.notes='為看清關節內部，髕骨在部分模型中移開；軟骨與間隙放大。不是病人影像。'
    if variant=='motion':
        s.notes='僅為 0–72° 剛性鉸鏈教學動畫；省略十字韌帶與肌肉，不模擬真實滾滑或髕骨軌跡。'
        # Patella and tendon are intentionally omitted in this motion-only model.
        s.parts=[p for p in s.parts if not p.name.startswith(('Patella','Patellar'))]

def add_shoulder(s,variant):
    s.camera=(8,-14,5);s.structures=[['肩胛骨・肱骨',BONE],['肌腱／關節囊',TEAL],['關注區（非分級）',ORANGE]]
    # Scapular blade with separate acromion and glenoid; teaching proportions only.
    v=[[-1.45,.32,2.0],[-1.70,.28,-.20],[.05,.12,1.08],[-1.40,.53,2.0],[-1.64,.48,-.15],[.07,.34,1.08]]
    f=[[0,2,1],[3,4,5],[0,3,5],[0,5,2],[2,5,4],[2,4,1],[1,4,3],[1,3,0]]
    s.add('Scapular blade', (v,f));s.add('Glenoid',ellipsoid((.06,.18,1.13),(.14,.36,.48)),TEAL)
    s.add('Humerus',organic(((.65,.10,1.08,.54,.52,.53),(.88,.05,.46,.31,.29,.6),(.95,.02,-.82,.24,.25,1.12))))
    s.add('Acromion',tube([(-1.15,.45,1.7),(-.35,.25,1.99),(.40,.16,1.92),(.78,-.10,1.7)],[.10,.13,.16,.18],elliptical=.60))
    s.add('Clavicle (partial)',tube([(-1.7,-.48,1.91),(-.85,-.53,2.04),(-.10,-.26,2.02),(.45,-.20,1.88)],.10))
    paths=[('Supraspinatus tendon',[(-1.05,.19,1.65),(-.17,.09,1.68),(.58,.02,1.68),(.94,-.04,1.34)]),('Subscapularis tendon',[(-1.2,-.05,.91),(-.18,-.30,1.10),(.46,-.47,1.0)]),('Infraspinatus tendon',[(-1.18,.49,1.0),(-.11,.51,1.15),(.58,.59,1.01)]),('Teres minor tendon',[(-.76,.42,.5),(-.06,.48,.74),(.65,.56,.72)])]
    for i,(name,p) in enumerate(paths):
        s.add(name,tube(p,[.17,.15,.13,.11] if len(p)==4 else [.19,.16,.12],elliptical=.24),ORANGE if i==0 and variant!='capsule' else TEAL)
    if variant=='capsule':
        # Open bands suggest the capsule; not mistaken for a solid extra bone.
        for i in range(11):
            a=i*np.pi*2/11
            points=[(.04,.18+.25*np.cos(a),1.1+.35*np.sin(a)),(.47,.12+.6*np.cos(a),1.1+.6*np.sin(a)),(.89,.08+.32*np.cos(a),.76+.27*np.sin(a))]
            s.add('Joint capsule band '+str(i),tube(points,.035),ORANGE)
    s.notes='肩胛骨與軟組織採開放式、簡化呈現；色彩只標出閱讀焦點。'

def foot(s,variant,short=False):
    s.camera=(8,-12,5);s.structures=[['脛骨・腓骨・足骨',BONE],['肌腱／筋膜',TEAL],['關注區（非分級）',ORANGE]]
    h=2 if short else 4
    s.add('Tibia',organic(((0,.05,h/2+.8,.28,.30,h/2),(-.13,.01,.89,.35,.35,.32))))
    s.add('Fibula',tube([(.64,.16,h+.7),(.59,.14,1.3),(.56,.05,.66)],[.10,.10,.16]))
    s.add('Talus',ellipsoid((0,-.02,.55),(.40,.44,.30)))
    s.add('Calcaneus',ellipsoid((-.04,.37,.20),(.35,.61,.29)))
    # Tarsals, metatarsals and phalanges: five rays, hallux with two phalanges.
    for i in range(3):
        s.add('Midfoot bone '+str(i+1),ellipsoid((-.36+i*.32,-.52,.35),(.22,.30,.20)))
    ends=[]
    for i in range(5):
        x=-.51+i*.24;end=np.array([x,-1.57+(abs(i-1)*.12),.16]);ends.append(end)
        s.add('Metatarsal '+str(i+1),tube([(x*.75,-.68,.29),end],[.085 if i==0 else .055,.08 if i==0 else .055]))
        q=end.copy()
        for j in range(2 if i==0 else 3):
            r=q+np.array([-.03 if i==0 else .015,-.22 if j==0 else -.16,-.025]);s.add('Toe '+str(i+1)+' phalanx '+str(j+1),tube([q,r],.065 if i==0 else .045));q=r
    if variant=='plantar-fascia':
        for i,end in enumerate(ends):
            s.add('Plantar fascia slip '+str(i+1),tube([(-.13,.25,-.06),(-.1+i*.045,-.45,-.035),(end[0],end[1],-.03)],[.045,.05,.022]),TEAL)
        s.add('Calcaneal attachment emphasis',ellipsoid((-.13,.21,-.04),(.15,.20,.055)),ORANGE)
    else:
        s.add('Anterior talofibular ligament',tube([(.57,.02,.65),(.43,-.30,.41)],.045),ORANGE)
        s.add('Calcaneofibular ligament',tube([(.58,.1,.65),(.35,.42,.16)],.04),TEAL)
    if variant in ('achilles','calf-tear'):
        muscle(s,'Gastrocnemius medial head',(-.31,.38,4.54),(-.19,.73,2.32),.39)
        muscle(s,'Gastrocnemius lateral head',(.32,.43,4.40),(.19,.75,2.33),.32)
        muscle(s,'Soleus (simplified)',(.03,.45,3.59),(.01,.67,1.80),.35,TEAL)
        s.add('Achilles tendon',tube([(0,.70,2.58),(0,.83,1.50),(0,.78,.52),(-.01,.59,.27)],[.13,.11,.10,.14]),ORANGE if variant=='achilles' else TENDON)
        if variant=='calf-tear':s.add('Musculotendinous region of interest',ellipsoid((-.20,.93,2.5),(.18,.08,.20)),ORANGE)
        s.camera=(7,12,3.7)
    elif variant=='plantar-fascia':s.camera=(8,-10,-4.5)
    s.notes='足部為開放式結構示意；骨形、筋膜厚度與附著範圍經簡化。'

def pelvis(s,glutes=False):
    s.camera=(7,13,4);s.structures=[['骨盆・股骨',BONE],['肌群／肌腱',TEAL],['關注肌群',ORANGE]]
    for side in (-1,1):
        s.add('Iliac wing '+str(side),ellipsoid((side*.68,.1,2.66),(.49,.30,.65)))
        s.add('Pelvic ring '+str(side),torus((side*.44,-.1,1.98),(.39,.42),.13))
        s.add('Femur '+str(side),organic(((side*.70,.05,1.94,.27,.29,.26),(side*.94,.07,1.66,.29,.27,.29),(side*.97,.07,.44,.20,.21,1.1))))
    s.add('Sacrum',ellipsoid((0,.39,2.43),(.31,.24,.51)))
    if glutes:
        for side in (-1,1):
            muscle(s,'Gluteus maximus '+str(side),(side*.27,.54,2.78),(side*.95,.49,1.66),.42,ORANGE)
            muscle(s,'Gluteus medius region '+str(side),(side*.78,.1,3.12),(side*1.03,.08,2.04),.25,TEAL)
    else:
        for side in (-1,1):
            for i in range(3):
                muscle(s,'Hamstring group '+str(side)+'-'+str(i),(side*(.58+i*.13),.51,1.82),(side*(.72+i*.16),.39,-.45),.15,ORANGE if side<0 and i==1 else MUSCLE,6)
            s.add('Proximal tibia '+str(side),ellipsoid((side*.99,.01,-.68),(.30,.32,.2)))
    s.notes='肌群以分層概念呈現；不是完整的肌肉起止點圖，也不是個人的撕裂影像。'

def upper_limb(s,variant):
    s.camera=(6,-14,4);s.structures=[['骨骼',BONE],['肌腱／韌帶',TEAL],['神經或關注區',NERVE if variant=='elbow-ulnar' else ORANGE]]
    if variant=='wrist-load':
        s.add('Radius (distal)',organic(((-.30,.03,1.39,.13,.15,1.15),(-.29,-.01,.42,.25,.25,.28))))
        s.add('Ulna (distal)',tube([(.30,.08,2.5),(.30,.08,.45)],[.12,.10]))
        for row in range(2):
            for i in range(4):s.add('Carpal schematic '+str(row*4+i+1),ellipsoid((-.38+i*.24,0,.15-row*.24),(.14,.19,.13),20))
        for i in range(5):
            x=-.58+i*.26;start=(x*.72,0,-.16);end=(x,0,-.96+abs(i-2)*.09)
            if i==0:end=(-.94,-.02,-.53)
            s.add('Metacarpal '+str(i+1),tube([start,end],.065))
            a=np.array(end)
            for j in range(2 if i==0 else 3):
                b=a+np.array([-.19 if i==0 else .02,0,-.20 if i==0 else -.23]);s.add('Finger '+str(i+1)+'-'+str(j),tube([a,b],.047));a=b
        s.add('Wrist region emphasis',tube([(-.6,-.25,.32),(0,-.29,.28),(.51,-.23,.29)],.035),ORANGE)
    else:
        s.add('Humerus (distal)',organic(((0,0,1.45,.23,.25,1.5),(-.30,.02,.12,.26,.33,.28),(.30,.03,.12,.24,.3,.24))))
        s.add('Ulna',tube([(-.17,.15,.28),(-.24,.27,-.10),(-.25,.08,-1.20),(-.19,-.08,-2.37)],[.17,.18,.11,.085]))
        s.add('Radius',tube([(.36,-.10,-.16),(.44,-.02,-.65),(.39,-.01,-2.38)],[.14,.11,.17]))
        s.add('Radial head',ellipsoid((.37,-.09,-.17),(.2,.20,.10)),TEAL)
        if variant=='elbow-ulnar':
            s.add('Ulnar nerve',tube([(-.41,.05,1.4),(-.53,.13,.33),(-.47,.33,.04),(-.39,.22,-.46),(-.35,.14,-2.3)],.047),NERVE)
            s.add('Cubital region emphasis',tube([(-.58,.28,.36),(-.6,.40,.04),(-.43,.36,-.18)],.028),ORANGE)
        else:
            muscle(s,'Forearm extensor group',(.50,-.13,-.20),(.47,-.15,-1.98),.24,TEAL)
            s.add('Common extensor tendon region',tube([(.53,-.04,.13),(.58,-.08,-.26),(.55,-.10,-.50)],.068),ORANGE)
    s.notes='神經與軟組織為放大的走向示意；不提供注射或手術定位。'

def muscle_bundle(s,trigger=False):
    s.camera=(7,-14,5);s.structures=[['肌束',MUSCLE],['肌腱連接',TENDON],['關注區（非可見病灶）',ORANGE]]
    for i in range(11):
        a=2*np.pi*i/11;x=.43*np.cos(a);y=.43*np.sin(a)
        muscle(s,'Muscle fascicle '+str(i+1),(x*.25,y*.25,-1.70),(x*.25,y*.25,1.75),.18,MUSCLE,5)
        # Spread selected bundles laterally to make fascicular structure readable.
        for p in s.parts[-6:]:p.vertices[:,:2]+=np.array([x,y])
    for z in (-2.0,2.0):s.add('Tendon '+str(z),tube([(0,0,z*.82),(0,0,z*1.23)],[.34,.20]),TENDON)
    if trigger:s.add('Illustrative focus, not a lesion',ellipsoid((.35,-.43,.21),(.17,.14,.26)),ORANGE)
    else:
        for i in range(3):s.add('Separated fascicle '+str(i),tube([(1.0+i*.18,0,-.1),(1.35+i*.17,0,.6),(1.62+i*.16,0,1.2)],.055),TEAL)
    s.notes='放大肌束概念模型；激痛點不是本圖所能顯示或確診的可見腫塊。'

def brain(s,offset=(0,0,0),scale=1):
    o=np.array(offset)
    for side in (-1,1):
        mesh=ellipsoid((side*.55,0,.2),(.59,.84,.72),56,ripple=.055)
        s.add('Brain hemisphere '+str(side),transform(mesh,scale,o),BONE)
    s.add('Brainstem (simplified)',transform(tube([(0,.28,-.26),(0,.38,-.75)],[.17,.12]),scale,o),TEAL)
    s.add('Cerebellum (simplified)',transform(ellipsoid((0,.59,-.36),(.50,.31,.25),32,ripple=.04),scale,o),TENDON)

def vein(s,clot=False):
    s.camera=(8,-14,4);s.structures=[['靜脈壁',BLUE],['瓣膜示意',TEAL],['血塊／回流關注區',MUSCLE]]
    # A longitudinal open vessel wall: opening faces the camera, contents stay visible.
    mesh=uv_surface(lambda u,z:[.61*np.cos(u),.61*np.sin(u),z],50,24,u=(-.12,np.pi+ .12),v=(-2.1,2.1))
    s.add('Vein wall (cutaway)',mesh,BLUE)
    for z in (-1.1,.9):
        s.add('Vessel cutaway edge '+str(z),torus((0,0,z),(.60,.60),.035,0,np.pi),BLUE)
    for side in (-1,1):
        s.add('Valve leaflet '+str(side),tube([(side*.56,.10,.08),(side*.32,-.1,.30),(side*.05,-.08,.55)],[.05,.13,.025],elliptical=.55),TEAL)
    for z in (-1.50,-.70,1.45):
        for x in (-.20,.15):s.add('Illustrative red blood cell',ellipsoid((x,.04,z),(.10,.07,.04),18),MUSCLE)
    if clot:
        for i,(x,y,z) in enumerate([(-.27,.19,-.62),(-.18,.12,-.4),(-.31,.18,-.23),(-.04,.17,-.3)]):s.add('Thrombus schematic '+str(i),ellipsoid((x,y,z),(.23,.24,.22),24,ripple=.09),MUSCLE)
    else:
        for x in (-1.12,1.12):muscle(s,'Adjacent calf muscle (concept)',(x,0,-1.7),(x,0,1.8),.3,MUSCLE,6)
    s.notes='血管為縱向剖開與放大示意；不表示血流速度、血栓大小或個人的病況。'

def dumbbell(s,offset=(0,0,0),scale=1):
    o=np.array(offset)
    s.add('Dumbbell grip',transform(tube([(-.6,0,0),(.6,0,0)],.09),scale,o),BONE)
    for x in (-.64,.64):s.add('Dumbbell weight',transform(ellipsoid((x,0,0),(.19,.38,.38),24),scale,o),TEAL)

def mannequin(s,pose='stand',offset=(0,0,0),scale=1,tint=BONE):
    o=np.array(offset)
    def add(name,mesh,col=tint):s.add(name,transform(mesh,scale,o),col)
    hip=np.array([0,.12,2.13]);shoulder=np.array([0,0,3.48]);head=np.array([0,-.025,4.05])
    knees=[[-.40,-.01,1.15],[.40,-.01,1.15]];ankles=[[-.40,0,.22],[.40,0,.22]]
    if pose in ('squat','hinge'):
        hip=np.array([0,.65,1.83 if pose=='squat' else 2.08]);shoulder=np.array([0,-.13,2.99 if pose=='squat' else 2.95]);head=shoulder+np.array([0,-.20,.58]);knees=[[-.49,-.35,1.03],[.49,-.35,1.03]]
    if pose in ('step','running','agility'):
        knees=[[-.40,-.66,1.62],[.4,.25,1.17]];ankles=[[-.40,-.77,.85],[.4,.47,.23]]
    add('Torso',ellipsoid((hip+shoulder)/2,(.55,.27,np.linalg.norm(shoulder-hip)*.60),32,shoulder-hip),tint)
    add('Pelvis',ellipsoid(hip,(.50,.30,.36)),INK)
    add('Neck',tube([shoulder+[0,0,.20],head-[0,0,.29]],.13));add('Head (neutral mannequin)',ellipsoid(head,(.25,.23,.31)))
    for side in (-1,1):
        i=0 if side<0 else 1;h=hip+np.array([side*.32,0,-.14]);k=np.array(knees[i]);a=np.array(ankles[i])
        add('Thigh '+str(side),ellipsoid((h+k)/2,(.20,.20,np.linalg.norm(h-k)/2),32,k-h),TEAL if pose in ('squat','step','running') else tint)
        add('Knee '+str(side),ellipsoid(k,(.18,.18,.18)),ORANGE if pose=='squat' else TENDON)
        add('Shin '+str(side),ellipsoid((a+k)/2,(.145,.14,np.linalg.norm(a-k)/2),32,k-a));add('Ankle '+str(side),ellipsoid(a,(.12,.12,.14)))
        add('Foot '+str(side),ellipsoid(a+[0,-.16,-.12],(.16,.32,.115)))
        sh=shoulder+np.array([side*.51,0,0]);el=sh+[side*.1,-.1,-.63];hand=el+[0,-.12,-.60]
        if pose=='squat':el=sh+[side*.08,-.52,-.35];hand=el+[-side*.17,-.44,.08]
        if pose=='hinge':el=sh+[side*.06,-.11,-.70];hand=el+[0,-.08,-.64]
        if pose in ('running','agility'):el=sh+[side*.10,side*.30,-.56];hand=el+[0,-.35,.16]
        add('Upper arm '+str(side),tube([sh,el],[.16,.12]));add('Elbow '+str(side),ellipsoid(el,(.13,.13,.13)));add('Forearm '+str(side),tube([el,hand],[.115,.07]));add('Hand '+str(side),ellipsoid(hand,(.09,.075,.14)))
    if pose=='hinge':
        add('Training bar',tube([(-1.35,-.42,1.55),(1.35,-.42,1.55)],.055),TENDON)
        for x in (-1.12,1.12):add('Training plate',ellipsoid((x,-.42,1.55),(.12,.38,.38)),TEAL)
    if pose=='step':add('Step platform',box((-.4,-.77,.34),(.95,.90,.64)),INK)

def nutrition(s,variant):
    s.camera=(7,-12,10);s.structures=[['食物／器具示意',BONE],['飲食與生活',TEAL],['閱讀關注區',ORANGE]]
    if variant in ('supplements',):
        for x,h,col in [(-.85,1.7,TEAL),(.65,1.34,ORANGE)]:
            s.add('Unbranded supplement container',tube([(x,0,.13),(x,0,h)],[.39,.39],sides=48),col)
            s.add('Container cap',tube([(x,0,h),(x,0,h+.16)],[.41,.41],sides=48),BONE)
            s.add('Blank label panel',box((x,-.365,h*.55),(.51,.025,.50)),BONE)
        for i in range(4):s.add('Generic capsule '+str(i),ellipsoid((-.5+i*.3,-.71,.13),(.10,.22,.09),24),ORANGE if i%2 else TENDON)
        s.notes='容器與膠囊均無品牌、無劑量，僅代表補充品類別。'
        return
    if variant=='alcohol':
        s.add('Unbranded drinking glass',tube([(0,0,.45),(0,0,1.60)],[.31,.43],sides=48),TENDON)
        s.add('Beverage surface (symbolic)',ellipsoid((0,0,1.52),(.41,.41,.035)),ORANGE)
        s.add('Glass stem',tube([(0,0,.04),(0,0,.44)],.052),TENDON);s.add('Glass base',ellipsoid((0,0,.02),(.38,.38,.04)),TENDON)
        s.add('Record card',box((1.05,0,.6),(.65,.12,1.13)),TEAL)
        for z in (.30,.55,.80):s.add('Record line',tube([(.85,-.09,z),(1.25,-.09,z)],.018),BONE)
        s.notes='杯子是酒精飲品概念，不代表建議杯量、種類或健康效益。';return
    s.add('Plate',ellipsoid((0,0,.0),(1.65,1.48,.085),48),BONE)
    s.add('Plate rim',torus((0,0,.04),(1.60,1.44),.055),TENDON)
    # Broccoli-like vegetables, neutral protein pieces and rice-like grains.
    for j,(x,y) in enumerate([(-.8,-.34),(-.72,.24),(-.37,.61),(-1.01,.33)]):
        s.add('Vegetable stalk '+str(j),tube([(x,y,.09),(x,y,.31)],.065),TEAL)
        for k in range(4):
            a=k*2*np.pi/4;s.add('Vegetable crown',ellipsoid((x+.12*np.cos(a),y+.12*np.sin(a),.36),(.20,.20,.18),20,ripple=.06),DEEP if k%2 else TEAL)
    for j in range(3):s.add('Protein food portion '+str(j),transform(box((0,0,0),(.57,.3,.23)),offset=(.56,.43+j*.16,.16),angle=-.25),ORANGE)
    rng=np.random.default_rng(70435)
    for i in range(70):
        x,y=rng.normal(.45,.23),rng.normal(-.53,.19)
        s.add('Grain '+str(i),ellipsoid((x,y,.11+rng.random()*.11),(.075,.028,.025),12),WHITE)
    s.add('Drinking water (symbolic)',tube([(2.11,.49,.05),(2.11,.49,1.1)],[.23,.28],sides=32),BLUE)
    if variant=='recovery':dumbbell(s,(-1.02,1.86,.25),.55)
    if variant=='mood':
        # No causal arrow from food to brain; separate symbolic sphere, explicitly non-diagnostic.
        brain(s,(2.5,-.7,.55),.46)
    s.notes='餐盤為食物類別示意；沒有代表固定熱量、份量或營養比例。'

def safety(s,variant):
    s.camera=(8,-14,6);s.structures=[['藥品／資料概念',BONE],['核對資訊',TEAL],['需要留意',ORANGE]]
    s.add('Review card',box((.36,.18,1.36),(1.67,.16,2.34)),BONE)
    s.add('Card header',box((.36,.075,2.08),(1.24,.025,.26)),TEAL)
    for z in (1.56,1.15,.74):
        s.add('Checklist row',tube([(-.04,.045,z),(.94,.045,z)],.022),INK)
        s.add('Checklist marker',ellipsoid((-.24,.032,z),(.07,.022,.07),20),TEAL)
    if variant=='weightpills':
        s.add('Unlabelled medicine bag',box((-1.07,-.12,.71),(.84,.24,1.22)),TENDON)
        for i in range(3):s.add('Unknown medicine symbol '+str(i),ellipsoid((-1.08+(i%2)*.18,-.27,.48+i*.19),(.12,.045,.07),24),ORANGE)
    else:
        for i in range(2):s.add('Unbranded tablet '+str(i),ellipsoid((-1.02+i*.16,-.25,.40+i*.40),(.23,.12,.20),32),ORANGE if i else TEAL)
    s.notes='藥品外觀純屬概念，不對應真實品項、劑量或使用方式。'

def metabolism(s,variant):
    s.camera=(7,-14,6);s.structures=[['器官／身體概念',BONE],['生活與調節',TEAL],['閱讀關注區',ORANGE]]
    if variant=='appetite':
        brain(s,(0,0,2.0),.8)
        stomach=organic(((-.10,0,.16,.50,.28,.68),(.25,.0,-.16,.38,.27,.45),(-.2,0,.70,.16,.18,.43)))
        s.add('Stomach (separated concept)',stomach,TEAL)
        s.add('Pyloric outlet (simplified)',tube([(.20,0,-.39),(.59,0,-.39),(.69,0,-.10)],[.13,.12,.09]),TEAL)
        for i in range(7):s.add('Conceptual signalling pathway '+str(i),ellipsoid((1.12+.12*np.sin(i),0,.15+i*.3),(.044,.044,.07),16),ORANGE)
        s.notes='器官分離排列以表達訊號概念；並非真實相對位置、比例或完整生理路徑。'
    elif variant=='body':
        mannequin(s,offset=(0,0,0),scale=.8)
        s.add('Body-composition platform',box((0,0,-.04),(1.43,1.15,.16)),TEAL)
        dumbbell(s,(1.44,0,.36),.58)
        for i in range(3):s.add('Health record bar (no numerical scale)',box((-1.1-i*.22,.0,.4+i*.28),(.12,.13,.4+i*.22)),ORANGE if i==2 else TEAL)
        s.notes='中性人偶與健康紀錄為概念圖，沒有理想體型、前後對照或量測值。'
    elif variant=='diabetes':
        nutrition(s,'order')
        s.add('Blank glucose log',box((-2.28,.5,.68),(.74,.16,1.22)),TEAL)
        for z in (.30,.60,.9):s.add('Log line',tube([(-2.53,.38,z),(-2.02,.38,z)],.018),BONE)
        s.notes='飲食、活動與追蹤的概念組合；不是血糖讀值或保證療效。'
    else:
        mannequin(s,offset=(-.75,0,0),scale=.62)
        dumbbell(s,(1.03,0,.37),.75)
        s.add('Follow-up record',box((1.0,.45,1.45),(.86,.13,1.35)),BONE)
        for z in (1.10,1.45,1.80):s.add('Follow-up line',tube([(.72,.35,z),(1.28,.35,z)],.024),TEAL)
        s.notes='生活照護概念圖；不顯示注射方式、劑量或停藥時程。'

def make_scene(key):
    s=Scene(key)
    if key.startswith('knee-'):add_knee(s,key[5:])
    elif key.startswith('shoulder-'):add_shoulder(s,key[9:])
    elif key in ('achilles','calf-tear','ankle-lateral','plantar-fascia'):foot(s,key,short=key in ('ankle-lateral','plantar-fascia'))
    elif key in ('hip-glutes','hamstrings'):pelvis(s,key=='hip-glutes')
    elif key in ('elbow-tendon','elbow-ulnar','wrist-load'):upper_limb(s,key)
    elif key.startswith('muscle-'):muscle_bundle(s,key=='muscle-trigger')
    elif key.startswith('vein-'):vein(s,key=='vein-clot')
    elif key=='brain-concussion':
        brain(s);s.camera=(7,-12,6);s.structures=[['大腦半球示意',BONE],['腦幹示意',TEAL],['小腦示意',TENDON]];s.notes='腦部結構高度簡化；沒有病灶、出血或可供诊斷的影像特徵。'
    elif key.startswith('nutrition-'):nutrition(s,key[10:])
    elif key.startswith('safety-'):safety(s,key[7:])
    elif key.startswith('metabolism-'):metabolism(s,key[11:])
    elif key.startswith('movement-'):
        pose=key[9:];pose=pose if pose in ('squat','hinge','step','running','agility') else 'stand'
        mannequin(s,pose);s.camera=(8,-12,4)
        if key=='movement-coach':mannequin(s,'stand',offset=(1.54,.6,0),scale=.92,tint=TEAL)
        if key in ('movement-week','movement-training'):dumbbell(s,(1.25,-.5,.48),.8)
        if key=='movement-agility':
            for i in range(3):s.add('Training marker '+str(i),ellipsoid((1.14+i*.45,-.7,.08),(.17,.17,.09)),ORANGE)
        s.structures=[['中性訓練人偶',BONE],['訓練／肌群重點',TEAL],['動作關注区',ORANGE]];s.notes='人偶是動作概念而非處方；關節角度、肌肉外形與器材比例經簡化。'
    elif key=='assessment-ultrasound':
        s.add('Tissue block',box((0,0,.33),(3,1.65,.66)),MUSCLE)
        s.add('Superficial tissue layer',box((0,0,.72),(3,1.65,.12)),TENDON)
        s.add('Linear probe',box((0,0,1.5),(1.15,.49,.80)),BONE)
        s.add('Probe footprint',box((0,0,1.07),(1.2,.53,.08)),TEAL)
        for x in np.linspace(-.49,.49,9):s.add('Simulated ultrasound beam',tube([(x,0,1.02),(x,0,.17)],.012),TEAL)
        s.add('Probe cable',tube([(0,0,1.93),(.3,.12,2.4),(1.30,.15,2.36)],.045),INK)
        s.structures=[['探頭',BONE],['模擬聲束',TEAL],['組織層示意',MUSCLE]];s.notes='模擬聲束與組織剖面，完全不是超音波掃描畫面。'
    elif key=='assessment-abcde':
        mannequin(s,'stand',scale=.8)
        for i in range(5):s.add('ABCDE conceptual checkpoint '+str(i),ellipsoid((1.11,0,3.05-i*.57),(.16,.16,.16)),TEAL if i<3 else ORANGE)
        s.structures=[['評估人偶',BONE],['呼吸循環等初評',TEAL],['持續再評估',ORANGE]];s.notes='供受訓團隊理解系統性評估概念，非完整急救演算法或徒手操作指南。'
    else:raise ValueError('Unknown scene '+key)
    s.notes=s.notes.replace('诊','診').replace('区','區')
    if not s.parts:raise ValueError('Empty scene '+key)
    return s
