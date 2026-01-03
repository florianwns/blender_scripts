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

# Create the cube
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1))
cube = bpy.context.active_object

# Position the cylinder on top of the cube
cylinder_height = 2.0
cylinder_z = get_top(cube) + (cylinder_height / 2)
bpy.ops.mesh.primitive_cylinder_add(depth=cylinder_height, location=(0, 0, cylinder_z))
cylinder = bpy.context.active_object

# Create the monkey with rotation first (at default location)
monkey_rotation = (-0.600393, 0, 0)
bpy.ops.mesh.primitive_monkey_add(rotation=monkey_rotation)
monkey = bpy.context.active_object

# Calculate the perfect position so the monkey is just above the cylinder
cylinder_top = get_top(cylinder)
monkey_bottom = get_bottom(monkey)

# Move the monkey so its bottom matches the cylinder's top
monkey.location.z = cylinder_top - monkey_bottom

# Display the monkey's bounds
monkey.show_bounds = True
