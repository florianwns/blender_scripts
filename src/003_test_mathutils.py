import math

import mathutils

vec = mathutils.Vector((1.0, 2.0, 3.0))

mat_rot = mathutils.Matrix.Rotation(math.radians(90.0), 4, "X")
mat_trans = mathutils.Matrix.Translation(vec)

mat = mat_trans @ mat_rot
mat.invert()

mat3 = mat.to_3x3()
quat1 = mat.to_quaternion()
quat2 = mat3.to_quaternion()

quat_diff = quat1.rotation_difference(quat2)

print(quat_diff.angle)
print("radians(90.0)", math.radians(90.0))
print(mat_rot)


# Color values are represented as RGB values from 0 - 1, this is blue.
col = mathutils.Color((0.0, 0.0, 1.0))

# As well as r/g/b attribute access you can adjust them by h/s/v.
col.s *= 0.5

# You can access its components by attribute or index.
print("Color R:", col.r)
print("Color G:", col[1])
print("Color B:", col[-1])
print("Color HSV: {:.2f}, {:.2f}, {:.2f}".format(*col))


# Components of an existing color can be set.
col[:] = 0.0, 0.5, 1.0

# Components of an existing color can use slice notation to get a tuple.
print("Values: {:f}, {:f}, {:f}".format(*col))

# Colors can be added and subtracted.
col += mathutils.Color((0.25, 0.0, 0.0))

# Color can be multiplied, in this example color is scaled to 0-255
# can printed as integers.
print("Color: {:d}, {:d}, {:d}".format(*(int(c) for c in (col * 255.0))))

# This example prints the color as hexadecimal.
print(
    f"Hexadecimal: {int(col.r * 255):02x}{int(col.g * 255):02x}{int(col.b * 255):02x}"
)

# Direct buffer access is supported.
print(memoryview(col).tobytes())
