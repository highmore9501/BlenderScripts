import bpy


class RemoveMatOperator(bpy.types.Operator):
    bl_idname = 'opr.object_remove_mat_operator'
    bl_label = 'Object RemoveMat'

    def execute(self, context):

        for ob in bpy.context.selected_editable_objects:
            ob.active_material_index = 0
            for i in range(len(ob.material_slots)):
                bpy.ops.object.material_slot_remove({'object': ob})
