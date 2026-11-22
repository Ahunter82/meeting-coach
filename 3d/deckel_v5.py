# Glatte Einschubplatte: volle Innenhoehe der Huelse (58 mm), deckt Fenster von innen ab
import trimesh
H=58-0.4      # Innenhoehe minus Spiel
LEN=123       # von der Rueckwand bis 5 mm ueber das Fensterende hinaus
T=0.8         # 4 Schichten a 0,2 mm
t=trimesh.creation.box(extents=[LEN,H,T]); t.apply_translation(-t.bounds[0])
print('watertight',t.is_watertight,t.extents)
t.export('Deckel_v5_Platte.stl')
