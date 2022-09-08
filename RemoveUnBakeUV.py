import bpy


# 脚本目标，移除物体中名字不叫Bake的UVmap.使用前要谨慎！！！！！


for obj in bpy.context.selected_objects:
    if obj.type == 'MESH' and "Bake" in obj.data.uv_layers:
        for uv_layer in obj.data.uv_layers:
            if uv_layer.name != "Bake" and uv_layer.name != "NGon Face-Vertex":
                obj.data.uv_layers.remove(uv_layer)
