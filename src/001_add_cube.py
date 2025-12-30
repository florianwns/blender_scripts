import bpy


def ensure_cube(name: str = "Cube", location=(0, 0, 0)) -> bpy.types.Object:
    """Check if an object named `name` exists — otherwise create and position it."""
    cube_obj = bpy.data.objects.get(name)
    if cube_obj is None:
        bpy.ops.mesh.primitive_cube_add(
            size=2,
            enter_editmode=False,
            align="WORLD",
            location=location,
            scale=(1, 1, 1),
        )

        cube_obj = bpy.context.active_object
        if cube_obj is None:
            raise RuntimeError("Failed to create cube object")

    # Rename explicitly to ensure the requested name
    cube_obj.name = name
    cube_obj.location.z += 1.0
    print(f"Object '{name}' created and moved to {cube_obj.location}")
    return cube_obj


ensure_cube()
