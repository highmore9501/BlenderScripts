import bpy

from ..operators.AddNewUVMap import AddNewUVOperator  # 一键新增UV
from ..operators.RemoveBakeUV import RemoveUVOperator  # 一键删除UV
from ..operators.RemoveUnBakeUV import RemoveOtherUVOperator  # 一键删除其它UV


class UVDataPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_UV_DATA'
    bl_label = 'UV操作'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HippoTools'

    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj is not None:
            if obj.mode == "OBJECT":
                return True

        return False

    def draw(self, context):

        layout = self.layout  
        
        layout.label(text='新增UV')
        col = layout.column()
        row = col.row()
        row.prop(context.scene, 'NewUVMap')
        row = col.row()
        row.operator(AddNewUVOperator.bl_idname, text='一键新增UV', icon='FILE_NEW')

        layout.label(text='删除UV')
        col = layout.column()
        row = col.row()
        row.prop(context.scene, 'RemoveUVMap')
        row = col.row()
        row.operator(RemoveUVOperator.bl_idname, text='一键删除UV', icon='REMOVE')

        layout.label(text='删除其它UV')
        col = layout.column()
        row = col.row()
        row.prop(context.scene, 'RestUVMap')
        row = col.row()
        row.operator(RemoveOtherUVOperator.bl_idname, text='一键删除其它UV', icon='PINNED')
        