import bpy


# 脚本目标，在3d浮标处生成一个大小为1*1，方向符合spoke默认方向的平面，以参考放入图片


class AddReferencePlaneOperator(bpy.types.Operator):
    bl_idname = 'opr.object_add_reference_plane_operator'
    bl_label = 'Object AddReferencePlane'

    def execute(self, context):     

        bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=bpy.context.scene.cursor.location, scale=(1, 1, 1))
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.resize(value=(0.5, 0.5, 0.5), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        return {'FINISHED'}