import numpy as np, trimesh, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
t=trimesh.load('Batteriehalter_v1.stl')
use=t.copy(); use.apply_transform(np.linalg.inv(np.array([[0,0,-1,0],[0,1,0,0],[1,0,0,0],[0,0,0,1]])))
def draw(ax,m,elev,azim,title):
    v=m.vertices[m.faces]; n=m.face_normals
    sh=0.35+0.65*np.clip(n@np.array([0.4,-0.5,0.8])/np.linalg.norm([0.4,-0.5,0.8]),0,1)
    ax.add_collection3d(Poly3DCollection(v,facecolors=np.c_[sh*0.95,sh*0.95,sh*0.9,np.ones(len(sh))],edgecolor='none'))
    lo,hi=m.bounds; c=(lo+hi)/2; r=(hi-lo).max()/2
    ax.set_xlim(c[0]-r,c[0]+r);ax.set_ylim(c[1]-r,c[1]+r);ax.set_zlim(c[2]-r,c[2]+r)
    ax.view_init(elev,azim); ax.set_title(title,fontsize=11); ax.set_axis_off()
f=plt.figure(figsize=(15,5.5))
draw(f.add_subplot(131,projection='3d'),use,20,-60,'Einbaulage (Raumseite)')
draw(f.add_subplot(132,projection='3d'),use,15,150,'Einbaulage (Fensterseite / Klemme)')
draw(f.add_subplot(133,projection='3d'),t,25,-50,'Drucklage (stehend, ohne Stuetzen)')
plt.tight_layout(); plt.savefig('Batteriehalter_v1_Vorschau.png',dpi=110)
