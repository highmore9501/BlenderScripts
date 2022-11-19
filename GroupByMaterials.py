import bpy


# 脚本目标，将所有选中的物体按材料分组，如果该物体上有多个材料，就不管它直接跳过
# 首先，检测所有在组里的特体，是否mesh; 如果是mesh，则检测上面是否有材料；有材料就返回材料名，并且试图移动它到同材料名的组里。如果不成功，就新建同材料名的组，然后再移动。


class SortByMatOperator(bpy.types.Operator):
    bl_idname = 'opr.object_sort_by_mat_operator'
    bl_label = 'Object SortByMat'

    def move2Collection(self, obj, Collection):  # 移动目标到指定的Collection
        for col in obj.users_collection:
            # Unlink the object
            col.objects.unlink(obj)
            # Link each object to the target collection
        Collection.objects.link(obj)

    def execute(self, context):

        for item in bpy.context.selected_objects:
            if item.type == "MESH":
                if len(item.data.materials) == 1:  # 有且只有一种材料
                    materialName = str(item.material_slots[0].material.name)  # 拿到材料名
                    colCounter = 0  # 笨办法，用这个值来计算有多少同名的Collections
                    for col in bpy.data.collections:
                        if col.name == materialName:
                            colCounter += 1

                    if colCounter == 1:
                        self.move2Collection(item, bpy.data.collections[materialName])
                    else:  # 材料名不在所有的Collection组里 ，新建组，然后移动物体过去
                        newCollection = bpy.data.collections.new(name=materialName)
                        bpy.context.scene.collection.children.link(newCollection)
                        self.move2Collection(item, newCollection)

        return {'FINISHED'}
