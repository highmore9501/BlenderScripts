import bpy

from ..operators.ChangeMaterial import ChangerMatOperator  # 修改材质属性


class ChangeMatPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_CHANGE_MAT'
    bl_label = '批量修改材质属性'
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

        layout.label(text='修改材质')
        col = layout.column()
        row = col.row()
        row.prop(context.scene,"ChangeColor")
        row.prop(context.scene,"BaseColor")
        row = col.row()
        row.prop(context.scene,"ChangeRoughness")
        row.prop(context.scene,"Roughness")
        row = col.row()
        row.prop(context.scene,"ChangeMetalness")
        row.prop(context.scene,"Metalness")
        row = col.row()
        row.prop(context.scene,"ChangeEmitColor")
        row.prop(context.scene,"EmitColor")
        row = col.row()
        row.prop(context.scene,"ChangeEmitStrength")
        row.prop(context.scene,"EmitStrength")
        row = col.row()
        row.operator(ChangerMatOperator.bl_idname,text='批量修改材质属性',icon='NODE_MATERIAL')
        