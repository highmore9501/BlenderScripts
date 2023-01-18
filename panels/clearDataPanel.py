import bpy

from ..operators.RemoveConstraints import RemoveConstraintsOperator  # 一键清除所有约束
from ..operators.RemoveMat import RemoveMatOperator  # 删除所有材质
from ..operators.RemoveZero import RemoveZeroGroupOperator  # 删除空顶点组

class ClearDataPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_CLEAR_DATA'
    bl_label = '清理数据'
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

        layout.label(text='清空数据')
        row = layout.row()
        col = row.column()
        col.operator(RemoveConstraintsOperator.bl_idname, text='约束器', icon='CONSTRAINT')

        col = row.column()
        col.operator(RemoveZeroGroupOperator.bl_idname, text='空顶点组', icon='GROUP_VERTEX')

        col = row.column()
        col.operator(RemoveMatOperator.bl_idname, text='材质', icon='SHADING_SOLID')
