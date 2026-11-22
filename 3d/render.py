import trimesh, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
m=trimesh.load('Batteriehalter_Fenster_v1.stl')
# Montage-Ansicht: Y=oben -> plotte (x, z, y)
V=m.vertices[:,[0,2,1]]; F=m.faces
fig=plt.figure(figsize=(16,8))
light=np.array([0.4,-0.6,0.8]);light/=np.linalg.norm(light)
for i,(el,az,title) in enumerate([(25,-55,'Rückseite (Kabelschlitz, Haken)'),(20,125,'Vorderseite (Box reinschieben)')]):
    ax=fig.add_subplot(1,3,i+1,projection='3d')
    tri=V[F]; n=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]); n/=np.linalg.norm(n,axis=1)[:,None]+1e-9
    s=0.35+0.65*np.abs(n@light)
    pc=Poly3DCollection(tri,facecolors=np.c_[s*0.95,s*0.95,s*0.9,np.ones_like(s)],edgecolor='none'); ax.add_collection3d(pc)
    ax.set_xlim(-10,70);ax.set_ylim(0,90);ax.set_zlim(-20,80);ax.set_box_aspect((80,90,100))
    ax.view_init(el,az);ax.set_axis_off();ax.set_title(title)
# Querschnitt
ax=fig.add_subplot(1,3,3)
sec=m.section(plane_origin=[0,0,45],plane_normal=[0,0,1]); p,_=sec.to_planar(to_2D=np.eye(4))
for e in p.discrete: ax.fill(e[:,0],e[:,1],color='#bbb',ec='k')
ax.plot([],[])
for x,y,txt in [(30,15.5,'Batteriebox\n56 x 27 innen'),(30,42,'Kabelfach\n56 x 22, oben offen'),(30,-9,'Fenster\n18,5')]: ax.text(x,y,txt,ha='center',va='center',fontsize=9)
ax.set_aspect('equal');ax.set_title('Querschnitt (mm), Länge 90');ax.grid(alpha=.3)
ax.set_xlim(-5,65);ax.set_ylim(-20,60)
plt.tight_layout();plt.savefig('Batteriehalter_Fenster_v1_Vorschau.png',dpi=110)
