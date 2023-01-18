import bpy


# remove constraints


class RemoveConstraintsOperator(bpy.types.Operator):
    bl_idname = 'opr.object_remove_constraints_operator'
    bl_label = 'Object RemoveConstraints'

    def execute(self, context):
        for ob in bpy.context.selected_objects:
            if ob != None:
                cl = len(ob.constraints)
                if cl != 0:
                    # Remove existing constraints.
                    for c in ob.constraints:
                        ob.constraints.remove(c)

        return {'FINISHED'}
