# v2: Prinzip der Vorlage (Huelse an U-Klemme), Huelse verlaengert um Kabelkammer
import numpy as np, trimesh
from manifold3d import Manifold
W=1.8                 # Wandstaerke (4 Linien a 0,45)
GAP=18.4; NUB=0.3; CLW=2.0   # Klemmschenkel Fensterseite 2 mm (vorher 3)     # Fensterfluegel ~18 mm, Klemmnasen
DEPTH=25              # Klemmtiefe
IY,IZ=27,58           # Huelse innen: Dicke (Box 24) x Hoehe (Box mit Klappen 55)
BOX=84; LOOP=12; CABLE=32
IL=BOX+LOOP+CABLE     # Innenlaenge 126
L=IL+W                # Rueckwand bei X=0
def B(x,y,z): return Manifold.cube([x[1]-x[0],y[1]-y[0],z[1]-z[0]]).translate([x[0],y[0],z[0]])
X=(0,L); Yf=W+IY      # Innenseite Vorderwand
P=[B(X,(-GAP-CLW,Yf+W),(0,3)),                 # Steg oben
   B(X,(-GAP-CLW,-GAP),(-DEPTH,3)),            # Klemmschenkel Fensterseite
   B(X,(-GAP,-GAP+NUB),(-DEPTH,-DEPTH+4)),   # Klemmnase
   B(X,(-NUB,0),(-DEPTH,-DEPTH+4)),          # Klemmnase
   B(X,(0,W),(-IZ-W,3)),                     # Rueckwand = Klemmschenkel innen
   B(X,(Yf,Yf+W),(-IZ-W,3)),                 # Vorderwand (Raumseite)
   B(X,(0,Yf+W),(-IZ-W,-IZ)),                # Boden
   B((0,W),(0,Yf+W),(-IZ-W,3)),              # Rueckwand Stirnseite (geschlossen)
]
# Haken v7: kraeftiger Fuss mit Keil an der Vorderwand, Haken selbst schlank (2,4 mm)
from manifold3d import CrossSection
HX=22                      # Breite des Hakens (in Drucklage = Hoehe)
zb0=-IZ-W; zb=zb0-5; yo=Yf+W   # Unterkante Huelse, Unterkante Fuss, Aussenseite Vorderwand
s0=yo+3
prof=[[(0,zb),(yo+9,zb),(yo+9,zb0+0.01),(0,zb0+0.01)],                              # Fuss 5 mm unter ganzem Boden
      [(yo-0.01,zb0-0.01),(yo+9,zb0-0.01),(yo-0.01,zb0+12)],                         # Keil an Vorderwand 9x12
      [(s0-2,zb+0.01),(s0,zb-4),(s0,zb-11),(s0+10,zb-11),(s0+10,zb-4),(s0+7.6,zb-4),(s0+7.6,zb-8.6),(s0+2.4,zb-8.6),(s0+2.4,zb-4),(s0+6.5,zb+0.01)]]  # J-Haken 2,4 mm, Wurzel verbreitert
hook=Manifold()
for i,p in enumerate(prof):
    e=Manifold.extrude(CrossSection([p]),8)   # Haken, Fuss und Keil 8 mm breit (auf dem Bett, keine Stuetzen)
    hook=hook+e.transform([[0,0,1,0],[1,0,0,0],[0,1,0,0]])
P.append(hook)
m=P[0]
for p in P[1:]: m=m+p
cuts=[B((W+8,L-10),(-NUB-1,W+1),(-IZ+6,-8)),   # grosses Fenster hinten (Fensterseite, unsichtbar) spart Material
      B((L-12,L+1),(W+8,Yf-8),(-IZ-W-1,-IZ+1)),  # Kabelauslass vorne unten
      B((-1,W+1),(W+9,Yf-9),(-IZ+12,-12))]       # Durchlass Rueckwand (Kabel/Oese)
for c in cuts: m=m-c
mesh=m.to_mesh(); t=trimesh.Trimesh(mesh.vert_properties[:,:3],mesh.tri_verts)
t.apply_transform(np.array([[0,0,-1,0],[0,1,0,0],[1,0,0,0],[0,0,0,1]]))
t.apply_translation(-t.bounds[0])
print('watertight',t.is_watertight,'Masse',t.extents.round(1),'cm3',round(t.volume/1000,1))
t.export('Batteriehalter_v10.stl')
