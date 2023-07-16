# 为所选的的物体添加hubs里的点光源

import bpy

def main():
    for obj in bpy.context.selected_objects:
        # 将obj设置为当前激活的物体
        bpy.context.view_layer.objects.active = obj
        # 添加hubs的点光源
        bpy.ops.wm.add_hubs_component(panel_type="object", component_name="point-light")
        # 设置点光源的强度
        bpy.context.object.hubs_component_point_light.intensity = 100
        # 设置点光源的范围
        bpy.context.object.hubs_component_point_light.range = 10
        # 设置点光源的阴影偏移
        bpy.context.object.hubs_component_point_light.shadowBias = -1.9e-05
        # 取消obj的选中状态
        obj.select_set(False)


main()



