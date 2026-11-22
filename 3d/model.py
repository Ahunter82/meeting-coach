import trimesh, numpy as np
from shapely.geometry import Polygon, Point, box as sbox
from shapely.ops import unary_union
def B(x0,x1,y0,y1,z0,z1):
    b=trimesh.creation.box(extents=[x1-x0,y1-y0,z1-z0]); b.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return b
W,H,L,t=56,27,88,2          # Innenmaß Hülse (Box 54x25x84 + Luft)
OX,OY,OZ=W+2*t,H+2*t,L+t     # 60 x 31 x 90
TRAY=22                      # Kabelfach-Tiefe
GAP=18.5                     # Fensterdicke 18 + Luft
LEG=16
parts=[]
sleeve=B(0,OX,0,OY,0,OZ).difference(B(t,OX-t,t,OY-t,t,OZ+1)).difference(B(15,45,8,20,-1,t+1))
parts.append(sleeve)
y1=OY+TRAY
parts += [B(0,t,OY-t,y1,0,OZ), B(OX-t,OX,OY-t,y1,0,OZ), B(0,OX,OY-t,y1,0,t), B(0,OX,OY-t,OY+10,OZ-t,OZ)]
c=OX/2; a=c-GAP/2; b=c+GAP/2
parts += [B(a-2.5,a,-LEG,t,0,OZ), B(b,b+2.5,-LEG,t,0,OZ), B(a,a+0.5,-LEG+1,-LEG+3,0,OZ), B(b-0.5,b,-LEG+1,-LEG+3,0,OZ)]
# Haken (flach, liegt beim Druck auf dem Bett)
cx,cy=c+4,y1+18
stem=sbox(c-4,y1-2,c+0,cy)
ring=Point(cx,cy).buffer(8,64).difference(Point(cx,cy).buffer(4,64)).intersection(sbox(cx-9,cy,cx+9,cy+9))
tip=sbox(cx+4,cy-6,cx+8,cy).union(Point(cx+6,cy-6).buffer(2,32))
base=sbox(c-12,y1-2,c+8,y1+3)
hk=unary_union([stem,ring,tip,base]).buffer(0.8).buffer(-0.8)
parts.append(trimesh.creation.extrude_polygon(hk,5))
m=trimesh.boolean.union(parts,engine='manifold')
print(m.is_watertight, m.bounds, m.volume/1000,'cm3')
m.export('Batteriehalter_Fenster_v1.stl')
