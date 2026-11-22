import numpy as np, trimesh
from PIL import Image, ImageDraw, ImageFont
R=np.array([[0,0,-1,0],[0,1,0,0],[1,0,0,0],[0,0,0,1]])
t=trimesh.load('Batteriehalter_v10.stl')
use=t.copy(); use.apply_transform(np.linalg.inv(R))
# Dummy-Batteriebox (dunkel), halb eingeschoben, + Fenster-Stueck (blau)
box=trimesh.creation.box(extents=[84,24,55]); box.apply_translation([2.4+44+44,2.4+1.5+12,-29])
sash=trimesh.creation.box(extents=[160,18,60]); sash.apply_translation([64,-9.2,-30])
def render(meshes,elev,azim,W=600,H=480):
    a,e=np.radians(azim),np.radians(elev)
    fwd=np.array([np.cos(e)*np.cos(a),np.cos(e)*np.sin(a),np.sin(e)])
    right=np.cross([0,0,1],fwd); right/=np.linalg.norm(right); up=np.cross(fwd,right)
    allv=np.vstack([m.vertices for m,_ in meshes]); P=allv@np.c_[right,up]
    lo,hi=P.min(0),P.max(0); s=0.85*min(W/(hi-lo)[0],H/(hi-lo)[1]); c=(lo+hi)/2
    img=np.ones((H,W,3))*1.0; zb=np.full((H,W),-1e9)
    light=np.array([0.3,-0.4,0.85]); light/=np.linalg.norm(light)
    for m,col in meshes:
        V=m.vertices; sx=(V@right-c[0])*s+W/2; sy=H/2-(V@up-c[1])*s; sz=V@fwd
        for f,n in zip(m.faces,m.face_normals):
            if n@fwd<=0: continue
            sh=0.45+0.55*abs(n@light)
            x=sx[f];y=sy[f];z=sz[f]
            x0,x1=int(max(0,x.min())),int(min(W-1,x.max()+1)); y0,y1=int(max(0,y.min())),int(min(H-1,y.max()+1))
            if x1<x0 or y1<y0: continue
            X,Y=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
            d=(y[1]-y[2])*(x[0]-x[2])+(x[2]-x[1])*(y[0]-y[2])
            if abs(d)<1e-9: continue
            l0=((y[1]-y[2])*(X-x[2])+(x[2]-x[1])*(Y-y[2]))/d; l1=((y[2]-y[0])*(X-x[2])+(x[0]-x[2])*(Y-y[2]))/d; l2=1-l0-l1
            ins=(l0>=-1e-6)&(l1>=-1e-6)&(l2>=-1e-6); Z=l0*z[0]+l1*z[1]+l2*z[2]
            sub=zb[y0:y1+1,x0:x1+1]; upd=ins&(Z>sub); sub[upd]=Z[upd]
            img[y0:y1+1,x0:x1+1][upd]=np.array(col)*sh
    return Image.fromarray((img*255).astype(np.uint8))
H=(use,(0.95,0.95,0.92)); Bx=(box,(0.25,0.25,0.27)); S=(sash,(0.6,0.75,0.95))
views=[(render([H,Bx,S],25,50),'Am Fenster, Box eingeschoben (Raumseite)'),
       (render([H],25,-125),'Fensterseite: Klemme fuer 18 mm'),
       (render([H,Bx],8,8),'Stirnansicht: Huelse, Kabelfach, Haken'),
       (render([(t,(0.95,0.95,0.92))],30,-130),'Drucklage: stehend, ohne Stuetzen')]
out=Image.new('RGB',(1200,1000),'white'); d=ImageDraw.Draw(out)
try: fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
except: fnt=ImageFont.load_default()
for i,(im,tt) in enumerate(views):
    x,y=(i%2)*600,(i//2)*500; out.paste(im,(x,y+20)); d.text((x+20,y+5),tt,fill='black',font=fnt)
out.save('Batteriehalter_v10_Vorschau.png')
