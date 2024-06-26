import bpy

from ..operators.GroupByMaterials import SortByMatOperator  # 按材质分类
from ..operators.changeGlassBlendMode import ChangeGlassBlendeModeOperator, DisableGlassBlendeModeOperator  # 修改玻璃混合模式

class ClearMatPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_MAT_DATA'
    bl_label = '清理材质'
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

        layout.label(text='材质处理')
        row = layout.row()
        col = row.column()
        col.operator(SortByMatOperator.bl_idname, text='材质分类', icon='SHADING_SOLID')

        col = row.column()
        col.operator(ChangeGlassBlendeModeOperator.bl_idname, text='玻璃处理', icon='SHADING_RENDERED')

        col = row.column()
        col.operator(DisableGlassBlendeModeOperator.bl_idname, text='取消透明', icon='SHADING_SOLID')
