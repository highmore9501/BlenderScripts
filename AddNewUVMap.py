import bpy


# 脚本目标，将所有选中的物体新增一个UVmap，给它命名为Bake,同时激活它


for obj in bpy.context.selected_objects:
    if obj.type == 'MESH' and "Bake" not in obj.data.uv_layers:
        obj.data.uv_layers.new(name="Bake")
        obj.data.uv_layers["Bake"].active_render = True
