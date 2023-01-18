import bpy

from ..operators.ParticleToAnimationRebuild import ParticleToAnimationOperator # 粒子动画

class ParticleAnimatePanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_PARTICLE_ANIMATE'
    bl_label = '粒子动画'
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

        layout.label(text='粒子动画')
        col = layout.column()
        row = col.row()
        row.prop_search(context.scene, "ps_obj", bpy.data, "objects", icon='OBJECT_DATA')
        row = col.row()
        row.prop_search(context.scene, "Obj", bpy.data, "objects",  icon='OBJECT_DATA')
        row = col.row()
        row.operator(ParticleToAnimationOperator.bl_idname, text='生成粒子动画', icon='RENDER_ANIMATION')
        