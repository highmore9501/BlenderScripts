import bpy

for ob in bpy.context.selected_editable_objects:
    ob.active_material_index = 0
    for i in range(len(ob.material_slots)):
        bpy.ops.object.material_slot_remove({'object': ob})