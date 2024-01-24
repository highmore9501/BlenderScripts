# 先选中要导出的组件，然后再选中对应的骨骼，然后导出glb文件，参数是只导出选中的部分，导出动画导出蒙皮，按jpg导出

import bpy
import os

collectionNames = ['HEAD']  # 这里是要导出的文件夹的列表
armatureName = 'AvatarRoot'  # 骨骼的名字

for collection in collectionNames:
    for obj in bpy.data.collections.get(collection).all_objects:
        bpy.ops.object.select_all(action='DESELECT')

        bpy.data.objects[armatureName].select_set(True)
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        file_path = bpy.path.abspath("//export\\{}.glb".format(obj.name))
        try:
            bpy.ops.export_scene.gltf(
                filepath=file_path,
                use_selection=True,
                export_image_format='JPEG',
                export_colors=False,
                export_tangents=True
            )
        except:
            pass
