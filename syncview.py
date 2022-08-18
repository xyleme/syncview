# -*- coding:utf-8 -*-

#  ***** GPL LICENSE *****
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#  ***** GPL LICENSE *****


bl_info = {
    "name": "Sync View",
    "description": "Enables twin 3D View navigation synchronization, mainly for photogrammetric support purpose",
    "author": "Vincent Bain - Toraval",
    "version": (2, 0, 0),
    "blender": (3, 00, 0),
    "location": "3D View > UI Region > SyncView",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}


import bpy
from bpy.props import IntProperty, FloatProperty


class StvPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_stvPanel"
    bl_label = "Syncview settings"
    bl_category = 'SyncView'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
        row = layout.row()
        row.label(text="Cameras :")
        layout.prop(scene, "LeftCam",icon='OUTLINER_OB_CAMERA', text="Left cam")
        layout.prop(scene, "RightCam",icon='CAMERA_DATA', text="Right cam")
        row.operator('opr.camera_catcher_operator', text="Catch cams")
        layout.prop(scene, "PanRatio", text="Pan ratio")
        layout.prop(context.space_data.region_3d, "lock_rotation", text="Lock View Rotation")
        layout.operator('custom.stv_reset_zoom_op', text='Auto align view')
        layout.label(text="Area info:")
        layout.prop(context.area, "width")


def scene_mycam_poll(self, object):
    return object.type == 'CAMERA'


class StvResetZoomOperator(bpy.types.Operator):
    bl_idname = 'custom.stv_reset_zoom_op'
    bl_label = 'Stv Reset Zoom Op'
    bl_options = {'INTERNAL'}
    bl_description = "Tries to reset a correct stereoscopic setup"

    def execute(self, context):
        if bpy.context.space_data.camera.name == bpy.context.scene.RightCam.name:
            bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.RightCamIndex].spaces[0].region_3d.view_camera_zoom = bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.LeftCamIndex].spaces[0].region_3d.view_camera_zoom
            bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.RightCamIndex].spaces[0].region_3d.view_camera_offset[0] = bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.LeftCamIndex].spaces[0].region_3d.view_camera_offset[0]
            bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.RightCamIndex].spaces[0].region_3d.view_camera_offset[1] = bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.LeftCamIndex].spaces[0].region_3d.view_camera_offset[1]
            self.report({'INFO'}, "Right view was successfully aligned to left view!")
        if bpy.context.space_data.camera.name == bpy.context.scene.LeftCam.name:
            bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.LeftCamIndex].spaces[0].region_3d.view_camera_zoom = bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.RightCamIndex].spaces[0].region_3d.view_camera_zoom
            bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.LeftCamIndex].spaces[0].region_3d.view_camera_offset[0] = bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.RightCamIndex].spaces[0].region_3d.view_camera_offset[0]
            bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.LeftCamIndex].spaces[0].region_3d.view_camera_offset[1] = bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.RightCamIndex].spaces[0].region_3d.view_camera_offset[1]
            self.report({'INFO'}, "Left view was successfully aligned to right view!")
        
        return {'FINISHED'}


def update_cams(self, context):
    list = [0,0]
    k=0
    l=0
    for area in bpy.data.window_managers[0].windows[0].screen.areas:
        if area.type == 'VIEW_3D':
            if area.spaces[0].camera.name == bpy.context.scene.LeftCam.name:
                list[0]=k
        k += 1
    
    for area in bpy.data.window_managers[0].windows[0].screen.areas:
        if area.type == 'VIEW_3D':
            if area.spaces[0].camera.name == bpy.context.scene.RightCam.name:
                list[1]=l
        l += 1
    
    bpy.context.scene.LeftCamIndex = list[0]
    bpy.context.scene.RightCamIndex = list[1]
    
    bpy.context.scene.LeftCamIndex
    bpy.context.scene.RightCamIndex



class CatchCams(bpy.types.Operator):
    bl_idname = 'opr.camera_catcher_operator'
    bl_label = 'Camera catcher'
    bl_description = 'Select both stereo cameras for grabbing/rotating'
    
    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        for i in (bpy.context.scene.LeftCam.name, bpy.context.scene.RightCam.name):
            obj = bpy.context.scene.objects.get(i)
            if obj: obj.select_set(True)
        bpy.data.scenes["Scene"].tool_settings.transform_pivot_point = "CURSOR"
        self.report({"INFO"}, "Stereo Cams selected, ready to transform")
        return {'FINISHED'}



class ModalSyncPanOperator(bpy.types.Operator):
    """synchronously pan 3d view with mouse"""
    bl_idname = "object.pan_modal_operator"
    bl_label = "Simple Modal Operator"

    init_mouse_x = IntProperty()
    init_mouse_y = IntProperty()

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            deltax = self.init_mouse_x - event.mouse_x
            deltay = self.init_mouse_y - event.mouse_y
            fact = 0.01 * bpy.context.scene.PanRatio/(bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.LeftCamIndex].spaces[0].region_3d.view_camera_zoom+31)
            bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.LeftCamIndex].spaces[0].region_3d.view_camera_offset[0] += deltax * fact
            bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.LeftCamIndex].spaces[0].region_3d.view_camera_offset[1] += deltay * fact
            
            bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.RightCamIndex].spaces[0].region_3d.view_camera_offset[0] += deltax * fact
            bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.RightCamIndex].spaces[0].region_3d.view_camera_offset[1] += deltay * fact
            
            self.init_mouse_x = event.mouse_x
            self.init_mouse_y = event.mouse_y

        elif event.value == 'RELEASE':
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.init_mouse_x = event.mouse_x
        self.init_mouse_y = event.mouse_y
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class ModalSyncZoomOperator(bpy.types.Operator):
    """synchronously zoom 3d view with mouse"""
    bl_idname = "object.zoom_modal_operator"
    bl_label = "Simple Modal Operator"

    init_mouse_x = IntProperty()
    init_mouse_y = IntProperty()

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            deltax = self.init_mouse_x - event.mouse_x
            deltay = self.init_mouse_y - event.mouse_y
            bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.LeftCamIndex].spaces[0].region_3d.view_camera_zoom -= deltay * 0.3
            bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.RightCamIndex].spaces[0].region_3d.view_camera_zoom -= deltay * 0.3
            
            fact = 0.01 * bpy.context.scene.PanRatio/(bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.LeftCamIndex].spaces[0].region_3d.view_camera_zoom+31)
            bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.LeftCamIndex].spaces[0].region_3d.view_camera_offset[0] -= deltax * fact
            bpy.data.window_managers[0].windows[0].screen.areas[bpy.context.scene.RightCamIndex].spaces[0].region_3d.view_camera_offset[0] += deltax * fact
            
            self.init_mouse_x = event.mouse_x
            self.init_mouse_y = event.mouse_y
            

        elif event.value == 'RELEASE':
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.init_mouse_x = event.mouse_x
        self.init_mouse_y = event.mouse_y

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


addon_keymaps = []

def register():
    
    bpy.utils.register_class(StvPanel)
    bpy.utils.register_class(ModalSyncPanOperator)
    bpy.utils.register_class(ModalSyncZoomOperator)
    bpy.utils.register_class(StvResetZoomOperator)
    bpy.utils.register_class(CatchCams)
    
    bpy.types.Scene.LeftCam = bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=scene_mycam_poll,
        update=update_cams,
        description="Camera used for left view frame"
    )
    bpy.types.Scene.RightCam = bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=scene_mycam_poll,
        update=update_cams,
        description="Camera used for right view frame"
    )
    bpy.types.Scene.PanRatio = bpy.props.FloatProperty(
        name="pan ratio",default=1,
        description = "Panning factor"
    )
    
    bpy.types.Scene.LeftCamIndex = bpy.props.IntProperty(name="Left view index", default=1)
    bpy.types.Scene.RightCamIndex = bpy.props.IntProperty(name="Right view index", default=2)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmp = km.keymap_items.new(ModalSyncPanOperator.bl_idname, type='MIDDLEMOUSE', value='PRESS', alt=True, shift=True, ctrl=False)
        kmz = km.keymap_items.new(ModalSyncZoomOperator.bl_idname, type='MIDDLEMOUSE', value='PRESS', alt=True, shift=False, ctrl=True)
        addon_keymaps.append((km, kmp, kmz))


def unregister():
    for km, kmp, kmz in addon_keymaps:
        km.keymap_items.remove(kmp)
        km.keymap_items.remove(kmz)
        addon_keymaps.clear()
    
    bpy.utils.unregister_class(ModalSyncPanOperator)
    bpy.utils.unregister_class(ModalSyncZoomOperator)
    bpy.utils.unregister_class(StvResetZoomOperator)
    bpy.utils.unregister_class(StvPanel)
    bpy.utils.unregister_class(CatchCams)

    del bpy.types.Scene.LeftCam
    del bpy.types.Scene.RightCam


if __name__ == "__main__":
    register()
