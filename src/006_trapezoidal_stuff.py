import bmesh
import numpy as np

import bpy

# Clear all objects from the current collection except cameras and lights
for obj in bpy.context.collection.objects:
    if obj.type not in {"CAMERA", "LIGHT"}:
        bpy.data.objects.remove(obj, do_unlink=True)


# -----------------------------
# PARAMÈTRES
# -----------------------------
COUNT_X = 20
COUNT_Y = 20
SPACING = 2.5

HEIGHT = 2.0
WIDTH_BOTTOM = 2.0
WIDTH_TOP = 1.0
DEPTH = 1.5


# -----------------------------
# GÉOMÉTRIE DE BASE (NUMPY)
# -----------------------------
def trapezoidal_prism_vertices(h, w1, w2, d):
    bottom = np.array(
        [
            [-w1 / 2, -d / 2, 0],
            [w1 / 2, -d / 2, 0],
            [w1 / 2, d / 2, 0],
            [-w1 / 2, d / 2, 0],
        ]
    )

    top = np.array(
        [
            [-w2 / 2, -d / 2, h],
            [w2 / 2, -d / 2, h],
            [w2 / 2, d / 2, h],
            [-w2 / 2, d / 2, h],
        ]
    )

    return np.vstack((bottom, top))


FACES = [
    (0, 1, 2, 3),  # bottom
    (4, 5, 6, 7),  # top
    (0, 1, 5, 4),
    (1, 2, 6, 5),
    (2, 3, 7, 6),
    (3, 0, 4, 7),
]


# -----------------------------
# CRÉATION DU MESH
# -----------------------------
mesh = bpy.data.meshes.new("TrapezoidalPrisms")
obj = bpy.data.objects.new(mesh.name, mesh)
bpy.context.collection.objects.link(obj)

bm = bmesh.new()

base_verts = trapezoidal_prism_vertices(HEIGHT, WIDTH_BOTTOM, WIDTH_TOP, DEPTH)

for x in range(COUNT_X):
    for y in range(COUNT_Y):
        offset = np.array([x * SPACING, y * SPACING, 0])
        coords = base_verts + offset

        v_start = len(bm.verts)
        for co in coords:
            bm.verts.new(co)

        bm.verts.ensure_lookup_table()

        for f in FACES:
            bm.faces.new([bm.verts[v_start + i] for i in f])


# -----------------------------
# FINALISATION
# -----------------------------
bm.normal_update()
bm.to_mesh(mesh)
bm.free()

obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.object.modifier_add(type="SUBSURF")
bpy.context.object.modifiers["Subdivision"].levels = 3


mesh.update()
