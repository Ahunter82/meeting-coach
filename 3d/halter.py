import numpy as np, trimesh
from manifold3d import Manifold
L=90.0
def B(x,y,z): return Manifold.cube([x[1]-x[0],y[1]-y[0],z[1]-z[0]]).translate([x[0],y[0],z[0]])
X=(0,L)
parts=[
 B(X,(-21.4,32.4),(0,3)),            # Deckel: Klemmen-Steg + Huelsen-Decke
 B(X,(-21.4,-18.4),(-25,3)),         # Klemmschenkel aussen (Fensterseite)
 B(X,(-18.4,-18.1),(-25,-21)),       # Klemmnase aussen
 B(X,(-0.3,0),(-25,-21)),            # Klemmnase innen
 B(X,(0,3),(-50.4,3)),               # Huelsen-Rueckwand = Klemmschenkel innen
 B(X,(30,32.4),(-50.4,3)),           # Huelsen-Vorderwand
 B(X,(0,50.8),(-50.4,-48)),          # Boden (Huelse + Kabelfach)
 B(X,(48.4,50.8),(-50.4,-26)),       # Kabelfach Vorderwand
 B((0,2),(30,50.8),(-50.4,-26)),     # Kabelfach Stirnwand
 B((L-2,L),(30,50.8),(-50.4,-26)),   # Kabelfach Stirnwand
 B((0,2),(0,32.4),(-50.4,3)) - B((0,2),(7,26),(-44,-4)),  # Anschlag hinten
 B((0,10),(40,44),(-62,-50.4)),      # Haken Steg
 B((0,10),(40,54),(-65,-62)),        # Haken Bogen
 B((0,10),(50,54),(-65,-57)),        # Haken Spitze
]
m=parts[0]
for p in parts[1:]: m=m+p
m=m-B((12,80),(29,33),(-23,-4))     # Fenster fuer Taster / Rausschieben
mesh=m.to_mesh()
t=trimesh.Trimesh(mesh.vert_properties[:,:3],mesh.tri_verts)
t.apply_transform(np.array([[0,0,-1,0],[0,1,0,0],[1,0,0,0],[0,0,0,1]]))  # Laengsachse nach oben
t.apply_translation(-t.bounds[0])
print('watertight',t.is_watertight,'bounds',t.extents.round(1),'vol cm3',round(t.volume/1000,1))
t.export('Batteriehalter_v1.stl')
