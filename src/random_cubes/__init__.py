# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
import random

from . import auto_load

bl_info = {
    "name": "Random Cubes",
    "author": "Florian",
    "description": "Add random cubes with random size and position",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "View3D > Sidebar > Random Cubes",
    "warning": "",
    "category": "Object",
}

auto_load.init()


class OBJECT_OT_add_random_cube(bpy.types.Operator):
    """Add a cube with random size and position"""
    bl_idname = "object.add_random_cube"
    bl_label = "Add Random Cube"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Add a cube at default position
        bpy.ops.mesh.primitive_cube_add()

        # Get the newly created object
        obj = bpy.context.active_object

        # Set random position between -10 and 10
        obj.location = (
            random.uniform(-10, 10),
            random.uniform(-10, 10),
            random.uniform(-10, 10)
        )

        # Set random scale (size) between 0.1 and 2.0
        scale_factor = random.uniform(0.1, 2.0)
        obj.scale = (scale_factor, scale_factor, scale_factor)

        return {'FINISHED'}


class VIEW3D_PT_random_cubes_panel(bpy.types.Panel):
    """Creates a Panel in the View3D sidebar"""
    bl_label = "Random Cubes"
    bl_idname = "VIEW3D_PT_random_cubes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Random Cubes'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.add_random_cube")


def register():
    bpy.utils.register_class(OBJECT_OT_add_random_cube)
    bpy.utils.register_class(VIEW3D_PT_random_cubes_panel)
    auto_load.register()


def unregister():
    auto_load.unregister()
    bpy.utils.unregister_class(VIEW3D_PT_random_cubes_panel)
    bpy.utils.unregister_class(OBJECT_OT_add_random_cube)
