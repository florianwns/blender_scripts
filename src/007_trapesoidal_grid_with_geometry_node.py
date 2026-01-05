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
# OBJET SUPPORT
# -----------------------------
mesh = bpy.data.meshes.new("GN_Prism_Base")
obj = bpy.data.objects.new("GN_Prism", mesh)
bpy.context.collection.objects.link(obj)

modifier = obj.modifiers.new(name="GeometryNodes", type="NODES")

tree = bpy.data.node_groups.new("TrapezoidalPrisms_GN", "GeometryNodeTree")
modifier.node_group = tree

nodes = tree.nodes
links = tree.links
nodes.clear()


# -----------------------------
# NODES ESSENTIELS
# -----------------------------
input_node = nodes.new("NodeGroupInput")
output_node = nodes.new("NodeGroupOutput")

# Handle Blender 4.0+ interface or older inputs/outputs
if hasattr(tree, "interface"):
    # Clear existing if any (should be clear anyway after nodes.clear() but tree.interface is separate)
    for i in range(len(tree.interface.items_tree) - 1, -1, -1):
        tree.interface.remove(tree.interface.items_tree[i])

    tree.interface.new_socket(
        name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    tree.interface.new_socket(
        name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
    )
else:
    if "Geometry" not in tree.inputs:
        tree.inputs.new("NodeSocketGeometry", "Geometry")
    if "Geometry" not in tree.outputs:
        tree.outputs.new("NodeSocketGeometry", "Geometry")

input_node.location = (-800, 0)
output_node.location = (1000, 0)


# Grid
grid = nodes.new("GeometryNodeMeshGrid")
grid.inputs["Size X"].default_value = (COUNT_X - 1) * SPACING
grid.inputs["Size Y"].default_value = (COUNT_Y - 1) * SPACING
grid.inputs["Vertices X"].default_value = COUNT_X
grid.inputs["Vertices Y"].default_value = COUNT_Y
grid.location = (-600, 200)


# Mesh to Points
points = nodes.new("GeometryNodeMeshToPoints")
points.location = (-400, 200)


# Cube (base prism)
cube = nodes.new("GeometryNodeMeshCube")
cube.location = (-600, -200)
cube.inputs["Size"].default_value = (WIDTH_BOTTOM, DEPTH, HEIGHT)

# Move up so base is at Z=0
transform = nodes.new("GeometryNodeTransform")
transform.location = (-400, -200)
transform.inputs["Translation"].default_value = (0, 0, HEIGHT / 2)

# Taper Logic (Set Position)
sep_xyz = nodes.new("ShaderNodeSeparateXYZ")
sep_xyz.location = (-200, -400)

compare = nodes.new("FunctionNodeCompare")
compare.location = (0, -400)
compare.data_type = "FLOAT"
compare.operation = "GREATER_THAN"
compare.inputs[1].default_value = HEIGHT * 0.9

set_pos = nodes.new("GeometryNodeSetPosition")
set_pos.location = (200, -200)

comb_xyz = nodes.new("ShaderNodeCombineXYZ")
comb_xyz.location = (0, -600)

math_mul = nodes.new("ShaderNodeMath")
math_mul.operation = "MULTIPLY"
math_mul.inputs[1].default_value = WIDTH_TOP / WIDTH_BOTTOM
math_mul.location = (-200, -600)

pos_input = nodes.new("GeometryNodeInputPosition")
pos_input.location = (-400, -600)

# Connect Taper Logic
links.new(pos_input.outputs["Position"], sep_xyz.inputs["Vector"])
links.new(sep_xyz.outputs["Z"], compare.inputs[0])
links.new(compare.outputs["Result"], set_pos.inputs["Selection"])

links.new(sep_xyz.outputs["X"], math_mul.inputs[0])
links.new(math_mul.outputs[0], comb_xyz.inputs["X"])
links.new(sep_xyz.outputs["Y"], comb_xyz.inputs["Y"])
links.new(sep_xyz.outputs["Z"], comb_xyz.inputs["Z"])
links.new(comb_xyz.outputs["Vector"], set_pos.inputs["Position"])


# Instance on Points
instance = nodes.new("GeometryNodeInstanceOnPoints")
instance.location = (400, 0)

# Realize Instances
realize = nodes.new("GeometryNodeRealizeInstances")
realize.location = (600, 0)


# Main Links
links.new(grid.outputs["Mesh"], points.inputs["Mesh"])
links.new(cube.outputs["Mesh"], transform.inputs["Geometry"])
links.new(transform.outputs["Geometry"], set_pos.inputs["Geometry"])

links.new(points.outputs["Points"], instance.inputs["Points"])
links.new(set_pos.outputs["Geometry"], instance.inputs["Instance"])

links.new(instance.outputs["Instances"], realize.inputs["Geometry"])
links.new(realize.outputs["Geometry"], output_node.inputs["Geometry"])


# Finalize Object
obj.select_set(True)
bpy.context.view_layer.objects.active = obj

# Optional: Smooth Shading
bpy.ops.object.shade_smooth()
