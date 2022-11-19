import bpy


# 脚本目标，将所有选中的物体新增一个UVmap，给它命名为Bake,同时激活它


class AddNewUVOperator(bpy.types.Operator):
    bl_idname = 'opr.object_add_new_uv_operator'
    bl_label = 'Object AddNewUV'

    newUVmap = bpy.context.scene.NewUVMap

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH' and self.newUVmap not in obj.data.uv_layers:
                obj.data.uv_layers.new(name=self.newUVmap)
            obj.data.uv_layers[self.newUVmap].active = True
