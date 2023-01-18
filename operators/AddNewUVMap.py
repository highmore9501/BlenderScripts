import bpy


# 脚本目标，将所有选中的物体新增一个UVmap，给它命名为Bake,同时激活它


class AddNewUVOperator(bpy.types.Operator):
    bl_idname = 'opr.object_add_new_uv_operator'
    bl_label = 'Object AddNewUV'
    bl_info = "将所有选中的物体新增一个UVmap，给它命名为Bake, 同时激活它"

    def execute(self, context):
        newUVmap = context.scene.NewUVMap

        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH' and newUVmap not in obj.data.uv_layers:
                obj.data.uv_layers.new(name=newUVmap)
                obj.data.uv_layers[newUVmap].active = True
            elif obj.type == 'MESH':
                obj.data.uv_layers[newUVmap].active = True

        return {'FINISHED'}
