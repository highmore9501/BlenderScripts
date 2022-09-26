import bpy

#remove constraints
for ob in bpy.context.selected_objects:
    if ob != None:
        cl = len(ob.constraints)
        if cl != 0:
            # Remove existing constraints.
            for c in ob.constraints:
                ob.constraints.remove(c)