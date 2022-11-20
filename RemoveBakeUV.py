import bpy


# 脚本目标，移除物体中名字叫Bake的UVmap.主要是Bake玩脱了需要删掉BakeUV时使用，使用前要谨慎！！！！！


class RemoveUVOperator(bpy.types.Operator):
    bl_idname = 'opr.object_remove_bake_uv_operator'
    bl_label = 'Object RemoveBakeUV'

    def execute(self, context):
        removeUVmap = context.scene.RemoveUVMap

        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH' and removeUVmap in obj.data.uv_layers:
                for uv_layer in obj.data.uv_layers:
                    if uv_layer.name == removeUVmap:
                        obj.data.uv_layers.remove(uv_layer)

        return {'FINISHED'}
