import bpy


# 脚本目标，移除物体中名字不叫Bake的UVmap.使用前要谨慎！！！！！

class RemoveOtherUVOperator(bpy.types.Operator):
    bl_idname = 'opr.object_remove_other_uv_operator'
    bl_label = 'Object RemoveUnBakeUV'

    def execute(self, context):
        RestUVmap = context.scene.RestUVMap

        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH' and RestUVmap in obj.data.uv_layers:
                for uv_layer in obj.data.uv_layers:
                    if uv_layer.name != RestUVmap and uv_layer.name != "NGon Face-Vertex":
                        obj.data.uv_layers.remove(uv_layer)

        return {'FINISHED'}
