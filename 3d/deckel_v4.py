# Deckel fuer das Fenster von Batteriehalter v4 (Fenster 110 x 40 mm, Wand 1.8 mm)
import trimesh
from manifold3d import Manifold
WX,WZ=110.0,40.0        # Fensteroeffnung
CL=0.25                 # Spiel je Seite
PLATE=1.2               # Platte innen (Spalt Box/Wand ist 3 mm)
PLUG=1.7                # Zapfen, Wand ist 1.8 -> 0.1 mm zurueck
OV=4.0                  # Ueberlappung der Platte rund ums Fenster
def B(x,y,z,dx=0,dy=0): return Manifold.cube([x,y,z]).translate([dx,dy,0])
plate=B(WX+2*OV,WZ+2*OV,PLATE)
plug=Manifold.cube([WX-2*CL,WZ-2*CL,PLUG]).translate([OV+CL,OV+CL,PLATE])
m=(plate+plug).to_mesh(); t=trimesh.Trimesh(m.vert_properties[:,:3],m.tri_verts)
print('watertight',t.is_watertight,'Masse',t.extents.round(2))
t.export('Deckel_v4.stl')
