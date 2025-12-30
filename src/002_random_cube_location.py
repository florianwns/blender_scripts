import random

import bpy


def create_random_cube():
    """Create a cube at a random location within a specified range."""

    # Generate random coordinates
    # Adjust the range (-10, 10) as needed for your scene scale
    x = random.uniform(-10, 10)
    y = random.uniform(-10, 10)
    z = random.uniform(0, 10)

    # Add the cube to the scene
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=(x, y, z))

    print(f"Created cube at location: ({x:.2f}, {y:.2f}, {z:.2f})")


create_random_cube()
