import bpy


class RemoveUnusedMatOperator(bpy.types.Operator):  # 移除所选物体中无用的材料
    bl_idname = 'opr.object_remove_unused_mat_operator'
    bl_label = 'Object RemoveUnusedMat'

    def execute(self, context):
        for obj in [o for o in context.selected_objects if o.type=='MESH']:
            mat_list = set(ms.material for ms in obj.material_slots)
            used_mats = set(obj.material_slots[f.material_index].material
                             for f in obj.data.polygons)

            unused_mats = mat_list - used_mats

            print(obj.name, unused_mats)

            for ms in obj.material_slots:
                if ms.material in unused_mats:
                    ms.material = None

        return {'FINISHED'}