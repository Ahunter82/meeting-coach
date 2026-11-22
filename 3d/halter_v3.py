# v2: Prinzip der Vorlage (Huelse an U-Klemme), Huelse verlaengert um Kabelkammer
import numpy as np, trimesh
from manifold3d import Manifold
W=2.4                 # Wandstaerke
GAP=18.4; NUB=0.3     # Fensterfluegel ~18 mm, Klemmnasen
DEPTH=25              # Klemmtiefe
IY,IZ=27,58           # Huelse innen: Dicke (Box 24) x Hoehe (Box mit Klappen 55)
BOX=84; LOOP=12; CABLE=32
IL=BOX+LOOP+CABLE     # Innenlaenge 126
L=IL+W                # Rueckwand bei X=0
def B(x,y,z): return Manifold.cube([x[1]-x[0],y[1]-y[0],z[1]-z[0]]).translate([x[0],y[0],z[0]])
X=(0,L); Yf=W+IY      # Innenseite Vorderwand
P=[B(X,(-GAP-3,Yf+W),(0,3)),                 # Steg oben
   B(X,(-GAP-3,-GAP),(-DEPTH,3)),            # Klemmschenkel Fensterseite
   B(X,(-GAP,-GAP+NUB),(-DEPTH,-DEPTH+4)),   # Klemmnase
   B(X,(-NUB,0),(-DEPTH,-DEPTH+4)),          # Klemmnase
   B(X,(0,W),(-IZ-W,3)),                     # Rueckwand = Klemmschenkel innen
   B(X,(Yf,Yf+W),(-IZ-W,3)),                 # Vorderwand (Raumseite)
   B(X,(0,Yf+W),(-IZ-W,-IZ)),                # Boden
   B((0,W),(0,Yf+W),(-IZ-W,3)),              # Rueckwand Stirnseite (geschlossen)
   B((0,10),(Yf,Yf+12),(-IZ-W-1,-IZ-W+0.01)),# Haken-Fuss
   B((0,10),(Yf+8,Yf+12),(-IZ-14,-IZ-W)),    # Haken Steg
   B((0,10),(Yf+8,Yf+22),(-IZ-17,-IZ-14)),   # Haken Bogen
   B((0,10),(Yf+18,Yf+22),(-IZ-17,-IZ-10)),  # Haken Spitze
]
m=P[0]
for p in P[1:]: m=m+p
cuts=[B((W+8,L-10),(Yf-1,Yf+W+1),(-IZ+10,-8)),   # grosses Fenster: Taster, Kabel reinstopfen, Box rausschieben
      B((L-12,L+1),(W+8,Yf-8),(-IZ-W-1,-IZ+1)),  # Kabelauslass vorne unten
      B((-1,W+1),(W+9,Yf-9),(-IZ+12,-12))]       # Durchlass Rueckwand (Kabel/Oese)
for c in cuts: m=m-c
mesh=m.to_mesh(); t=trimesh.Trimesh(mesh.vert_properties[:,:3],mesh.tri_verts)
t.apply_transform(np.array([[0,0,-1,0],[0,1,0,0],[1,0,0,0],[0,0,0,1]]))
t.apply_translation(-t.bounds[0])
print('watertight',t.is_watertight,'Masse',t.extents.round(1),'cm3',round(t.volume/1000,1))
t.export('Batteriehalter_v3.stl')
