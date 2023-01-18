import bpy


class RemoveUnusedMatOperator(bpy.types.Operator):  # 移除所选物体中无用的材料
    bl_idname = 'opr.object_remove_unused_mat_operator'
    bl_label = 'Object RemoveUnusedMat'

    def execute(self, context):
        for obj in [o for o in bpy.context.selected_objects if o.type=='MESH']:
            used_mats = set(obj.material_slots[f.material_index].material.name
                        for f in obj.data.polygons)
        
            print(used_mats)

            for i in reversed(range(len(obj.material_slots))):
                obj.active_material_index = i
                if obj.material_slots[i].name not in used_mats:
                    bpy.ops.object.material_slot_remove()

        return {'FINISHED'}