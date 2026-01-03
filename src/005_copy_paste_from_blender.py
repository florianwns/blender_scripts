"""
This script clears the scene and creates a vertical stack of objects: a cube,
a cylinder, and Suzanne (the monkey).
It uses vertex-based calculations to ensure perfect stacking regardless of
rotation, applies funny names, adds Subdivision Surface modifiers,
and scales the result.
"""

import bpy


def get_top(obj):
    """Return the highest Z coordinate of any vertex in world space."""
    bpy.context.view_layer.update()
    matrix = obj.matrix_world
    # Find the maximum Z coordinate across all vertices transformed to world space
    return max((matrix @ v.co).z for v in obj.data.vertices)


def get_bottom(obj):
    """Return the lowest Z coordinate of any vertex in world space."""
    bpy.context.view_layer.update()
    matrix = obj.matrix_world
    # Find the minimum Z coordinate across all vertices transformed to world space
    return min((matrix @ v.co).z for v in obj.data.vertices)


# Clear the scene
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

# Define names in variables
cube_name = "Le Pavé Suprême"
cylinder_name = "Le Tuyau Magique"
monkey_name = "Suzanne la Cascadeuse"

# Create the cube
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1))
cube = bpy.context.view_layer.objects.active
cube.name = cube_name

# Position the cylinder on top of the cube
cylinder_height = 2.0
cylinder_z = get_top(cube) + (cylinder_height / 2)
bpy.ops.mesh.primitive_cylinder_add(depth=cylinder_height, location=(0, 0, cylinder_z))
cylinder = bpy.context.view_layer.objects.active
cylinder.name = cylinder_name

# Create the monkey with rotation first (at default location)
monkey_rotation = (-0.600393, 0, 0)
bpy.ops.mesh.primitive_monkey_add(rotation=monkey_rotation)
monkey = bpy.context.view_layer.objects.active
monkey.name = monkey_name

# Calculate the perfect position so the monkey is just above the cylinder
cylinder_top = get_top(cylinder)
monkey_bottom = get_bottom(monkey)

# Move the monkey so its bottom matches the cylinder's top
monkey.location.z = cylinder_top - monkey_bottom

# Display the monkey's bounds
monkey.show_bounds = True

# Deselect all objects
bpy.ops.object.select_all(action="DESELECT")

# Loop through objects and add Subdivision Surface modifier
for obj in [cube, cylinder, monkey]:
    # Select objects for the subsequent scaling, excluding the cylinder
    if obj != cylinder:
        obj.select_set(True)

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_add(type="SUBSURF")

# Scale all selected objects by 2
bpy.ops.transform.resize(value=(2, 2, 2))
