#!BPY

# Copyright (c) 2020 SuperTuxKart author(s)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from . import stk_panel, stk_material, stk_kart, stk_track, stk_shaders, stk_props
import bpy
from bpy.app.handlers import persistent
from nodeitems_builtins import ShaderNodeCategory, world_shader_nodes_poll, object_eevee_cycles_shader_nodes_poll
from nodeitems_utils import NodeItem, register_node_categories, unregister_node_categories

bl_info = {
    'name': "SuperTuxKart Exporter Tools",
    'description': "Export various items to SuperTuxKart objects (karts, tracks, and materials)",
    'author': "Jean-Manuel Clemencon, Joerg Henrichs, Marianne Gagnon, Richard Qian",
    'version': (4, 0),
    'blender': (2, 80, 0),
    'location': "File > Import-Export",
    'warning': "",  # used for warning icon and text in addons panel
    'wiki_url': "https://supertuxkart.net/Community",
    'tracker_url': "https://github.com/supertuxkart/stk-blender/issues",
    'category': "Import-Export"
}


def menu_func_export_stk_material(self, context):
    self.layout.operator(
        stk_material.STK_Material_Export_Operator.bl_idname, text="STK Materials")


def menu_func_export_stk_kart(self, context):
    self.layout.operator(
        stk_kart.STK_Kart_Export_Operator.bl_idname, text="STK Kart")


def menu_func_export_stk_track(self, context):
    self.layout.operator(
        stk_track.STK_Track_Export_Operator.bl_idname, text="STK Track")


def menu_func_add_stk_object(self, context):
    self.layout.operator_menu_enum(
        "scene.stk_add_object", property="value", text="STK", icon='AUTO')


@persistent
def load_handler(arg):
    # Reaload object properties for new scene
    bpy.ops.stk.reload_object_properties()


classes = (
    stk_panel.STK_TypeUnset,
    stk_panel.STK_MissingProps_Object,
    stk_panel.STK_MissingProps_Scene,
    stk_panel.STK_MissingProps_Material,
    stk_panel.StkPanelAddonPreferences,
    stk_panel.STK_PT_Object_Panel,
    stk_panel.STK_PT_Scene_Panel,
    stk_panel.STK_OT_Add_Object,
    stk_panel.STK_FolderPicker_Operator,
    stk_panel.STK_PT_Quick_Export_Panel,
    stk_material.ANTARCTICA_PT_properties,
    stk_material.STK_Material_Export_Operator,
    stk_kart.STK_Kart_Export_Operator,
    stk_track.STK_Track_Export_Operator,

    stk_shaders.AntarcticaSolidPBR,
    stk_shaders.AntarcticaCutoutPBR,
    stk_shaders.AntarcticaTransparent,
    stk_shaders.AntarcticaTransparentAdditive,
    stk_shaders.AntarcticaUnlit,
    stk_shaders.AntarcticaCustom,
    stk_shaders.AntarcticaBackground,
    stk_shaders.AntarcticaSkybox,

    stk_panel.STK_PT_SceneProperties,
    stk_panel.STK_PT_ObjectProperties,
    stk_panel.STK_PT_LightProperties,
    stk_panel.STK_PT_CameraProperties,
    stk_panel.STK_PT_MaterialProperties,
)


def register():
    from bpy.utils import register_class
    from bpy.app.handlers import load_post

    for cls in classes:
        register_class(cls)

    shcat = [ShaderNodeCategory("SH_ANTARCTICA", "SuperTuxKart", items=[
        NodeItem("AntarcticaSolidPBR", poll=object_eevee_cycles_shader_nodes_poll),
        NodeItem("AntarcticaCutoutPBR", poll=object_eevee_cycles_shader_nodes_poll),
        NodeItem("AntarcticaTransparent", poll=object_eevee_cycles_shader_nodes_poll),
        NodeItem("AntarcticaTransparentAdditive", poll=object_eevee_cycles_shader_nodes_poll),
        NodeItem("AntarcticaUnlit", poll=object_eevee_cycles_shader_nodes_poll),
        NodeItem("AntarcticaCustom", poll=object_eevee_cycles_shader_nodes_poll),
        NodeItem("AntarcticaBackground", poll=world_shader_nodes_poll),
        NodeItem("AntarcticaSkybox", poll=world_shader_nodes_poll),
    ])]

    register_node_categories("SH_ANTARCTICA", shcat)

    load_post.append(load_handler)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_stk_material)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_stk_kart)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_stk_track)
    bpy.types.VIEW3D_MT_add.append(menu_func_add_stk_object)


def unregister():
    from bpy.utils import unregister_class
    from bpy.app.handlers import load_post

    bpy.types.VIEW3D_MT_add.remove(menu_func_add_stk_object)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_stk_material)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_stk_kart)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_stk_track)

    load_post.remove(load_handler)

    unregister_node_categories("SH_ANTARCTICA")

    for cls in classes:
        unregister_class(cls)


if __name__ == "__main__":
    register()
